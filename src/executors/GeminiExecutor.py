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
        self.api_key = self.request.get_param("inputApiKey")
        self.model_version = self.request.get_param("inputModelVersion")
        self.max_tokens = self.request.get_param("maxTokens")
        self.temperature = self.request.get_param("inputTemperature")
        
      
        self.prompt = self.request.get_param("inputPrompt")
        self.classes = self.request.get_param("inputClasses")
        
        self.image_selector = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        img_obj = Image.get_frame(img=self.image_selector, redis_db=self.redis_db)
        
        success, encoded_image = cv2.imencode('.jpg', img_obj.value)
        base64_image = base64.b64encode(encoded_image).decode('utf-8')
        
        if not success: raise RuntimeError("Failed to encode image for API")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_version}:generateContent"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": self.prompt if self.prompt else "Describe this image"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}}
                ]
            }],
            "generationConfig": {
                "maxOutputTokens": self.max_tokens,
                "temperature": self.temperature
            }
        }

        try:
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