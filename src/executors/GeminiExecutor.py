"""
Google Gemini Executor: Sends data to Google's API and returns AI analysis.
"""

import os
import sys
import base64
import json
import requests
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.CapGemini.src.utils.response import build_response_gemini
from components.CapGemini.src.models.PackageModel import PackageModel


MODELS_SUPPORTING_THINKING = [
    "gemini-3.1-pro-preview",
    "gemini-3-pro-preview",
    "gemini-3-flash-preview",
]


class GeminiExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.task_type = self.request.get_param("taskType")
        self.prompt = self.request.get_param("inputPrompt")
        self.classes = self.request.get_param("inputClasses")
        self.api_key = self.request.get_param("inputApiKey")
        print(f"[DEBUG] Full api_key received: '{self.api_key}'")
        print(f"[DEBUG] api_key length: {len(self.api_key) if self.api_key else 0}")
        self.model_version = self.request.get_param("inputModelVersion")
        self.thinking_level = self.request.get_param("thinkingLevel")
        self.temperature = self.request.get_param("inputTemperature")
        self.max_tokens = self.request.get_param("maxTokens")
        self.code_execution = self.request.get_param("codeExecution")
        self.max_concurrent_requests = self.request.get_param("maxConcurrentRequests")
        self.image_selector = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _build_generation_config(self, response_mime_type="text/plain"):
        config = {
            "response_mime_type": response_mime_type,
            "candidate_count": 1,
        }
        if self.max_tokens:
            config["max_output_tokens"] = self.max_tokens

        supports_thinking = self.model_version in MODELS_SUPPORTING_THINKING

        if self.thinking_level and supports_thinking:
            config["thinking_config"] = {"thinking_level": self.thinking_level}

        if self.temperature is not None and not supports_thinking:
            config["temperature"] = self.temperature

        return config

    def _build_payload(self, base64_image):
        serialised_classes = ", ".join(self.classes) if isinstance(self.classes, list) else (self.classes or "")

        if self.task_type == "unconstrained":
            return {
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": self.prompt},
                    ],
                },
                "generationConfig": self._build_generation_config(),
            }


        elif self.task_type == "visual-question-answering":
            return {
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": "You act as Visual Question Answering model. Answer the question about the image. "
                                       "For open questions answer with a few sentences. For ABCD questions return only the letter."}],
                },
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": f"Question: {self.prompt}"},
                    ],
                },
                "generationConfig": self._build_generation_config(),
            }


        elif self.task_type == "ocr":
            return {
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": "You act as an OCR model. Read all text from the image and return it "
                                       "in paragraphs matching the layout. Return only the recognised text."}],
                },
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": "Read the text"},
                    ],
                },
                "generationConfig": self._build_generation_config(),
            }

        elif self.task_type == "caption":
            return {
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": "You act as an image caption model. Provide a short description of the image."}],
                },
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": "Caption the image"},
                    ],
                },
                "generationConfig": self._build_generation_config(),
            }


        elif self.task_type == "detailed-caption":
            return {
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": "You act as an image caption model. Provide an extensive and detailed description of the image."}],
                },
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": "Caption the image in detail"},
                    ],
                },
                "generationConfig": self._build_generation_config(),
            }


        elif self.task_type == "classification":
            return {
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": 'You act as a single-class classification model. Return only a JSON object: '
                                       '{"class_name": "class-name", "confidence": 0.9}. '
                                       "class-name must be one of the user-defined classes. Return a single JSON object only."}],
                },
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": f"List of classes: {serialised_classes}"},
                    ],
                },
                "generationConfig": self._build_generation_config(response_mime_type="application/json"),
            }

 
        elif self.task_type == "multi-label-classification":
            return {
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": 'You act as a multi-label classification model. Return only a JSON object: '
                                       '{"predicted_classes": [{"class": "class-name-1", "confidence": 0.9}]}. '
                                       "Only include classes that are visible in the image."}],
                },
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": f"List of classes: {serialised_classes}"},
                    ],
                },
                "generationConfig": self._build_generation_config(response_mime_type="application/json"),
            }

        elif self.task_type == "object-detection":
            return {
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": 'You act as an object-detection model. Return only a JSON object: '
                                       '{"detections": [{"x_min": 0.1, "y_min": 0.2, "x_max": 0.3, "y_max": 0.4, '
                                       '"class_name": "my-class", "confidence": 0.7}]}. '
                                       "All coordinates must be 0.0-1.0 as a proportion of image dimensions."}],
                },
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": f"List of classes: {serialised_classes}"},
                    ],
                },
                "generationConfig": self._build_generation_config(response_mime_type="application/json"),
            }


        elif self.task_type == "structured-answering":
            return {
                "systemInstruction": {
                    "role": "system",
                    "parts": [{"text": "You produce responses in JSON. The user provides a dictionary where keys are "
                                       "field names and values are descriptions. Return only a JSON object with those keys."}],
                },
                "contents": {
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": f"Output field specifications:\n{self.prompt}"},
                    ],
                },
                "generationConfig": self._build_generation_config(response_mime_type="application/json"),
            }

        else:
            raise ValueError(f"Unsupported task_type: {self.task_type}")

    def run(self):
        img = Image.get_frame(img=self.image_selector, redis_db=self.redis_db)

        success, encoded_image = cv2.imencode('.jpg', img.value)
        if not success:
            raise RuntimeError("Failed to encode image for API")

        base64_image = base64.b64encode(encoded_image).decode('utf-8')

        payload = self._build_payload(base64_image)

        if self.code_execution:
            payload["tools"] = [{"code_execution": {}}]

        try:
            if not self.api_key.startswith("AIza"):
                payload["model"] = self.model_version
                payload["google_api_key"] = "rf_key:account"
                url = "https://api.roboflow.com/apiproxy/gemini"
                response = requests.post(
                    url,
                    params={"api_key": self.api_key},
                    json=payload
                )
            else:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_version}:generateContent"
                response = requests.post(url, params={"key": self.api_key}, json=payload)

            print(f"[DEBUG] Status: {response.status_code}")
            print(f"[DEBUG] Response: {response.text[:500]}")

            response.raise_for_status()
            data = response.json()

            parts = (
                data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [])
            )
            self.gemini_text = next((p["text"] for p in parts if "text" in p), "")
            self.gemini_classes = self.classes if self.classes else []

        except requests.exceptions.HTTPError as e:
            self.gemini_text = f"HTTP Error {response.status_code}: {response.text}"
            self.gemini_classes = []
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            self.gemini_text = f"API Error: {str(e)}"
            self.gemini_classes = []

        return build_response_gemini(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
