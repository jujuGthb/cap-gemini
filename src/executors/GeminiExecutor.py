"""
Google Gemini Executor: Sends data to Google's API and returns AI analysis.
"""

import os
import sys
import base64
import requests
import cv2


sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.CapGemini.src.utils.response import build_response_gemini
from components.CapGemini.src.models.PackageModel import PackageModel

class GeminiExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.task_type = self.request.get_param("taskType")
        self.prompt = self.request.get_param("inputPrompt")
        self.classes = self.request.get_param("inputClasses")
        self.api_key = self.request.get_param("inputApiKey")
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

    def run(self):
        img_obj = Image.get_frame(img=self.image_selector, redis_db=self.redis_db)
        
        success, encoded_image = cv2.imencode('.jpg', img_obj.value)
        
        if not success:
            raise RuntimeError("Failed to encode image for API")
        
        base64_image = base64.b64encode(encoded_image).decode('utf-8')


        
        
        parts = []
        
        if self.prompt:
            parts.append({"text": self.prompt})
            
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64_image
            }
        })
        
        if self.classes and self.task_type in ["classification", "multi-label-classification", "object-detection"]:
            class_str = ", ".join(self.classes) if isinstance(self.classes, list) else self.classes
            parts.append({"text": f"\nList of classes to recognize: {class_str}"})
            
        gen_config = {
            "max_output_tokens": self.max_tokens,
            "temperature": self.temperature if self.temperature is not None else 1.0
        }
        
        if self.thinking_level:
            gen_config["thinking_config"] = {"thinking_level": self.thinking_level}
            
        
        payload = {
            "model": self.model_version,
            "google_api_key": self.api_key,
            "contents": [{"parts": parts}],
            "generationConfig": gen_config
        }
        
        if self.code_execution:
            payload["tools"] = [{"code_execution": {}}]
            
        url = "https://api.roboflow.com/apiproxy/gemini"
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.post(url, params={"key": self.api_key}, json=payload)
            response.raise_for_status()
            data = response.json()
            
            self.output_text = data["candidates"][0]["content"]["parts"][0]["text"]
            self.output_classes = self.classes if self.classes else []
            
        except Exception as e:
            self.output_text = f"API Error: {str(e)}"
            self.output_classes = []

        return build_response_gemini(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
