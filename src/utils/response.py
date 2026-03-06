from sdks.novavision.src.helper.package import PackageHelper
from components.CapGemini.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    GeminiExecutor,
    GeminiResponse,
    GeminiOutputs,
    OutputText,
    Classes
)
def build_response_gemini(context):
    
    print(f"[DEBUG] build_response_gemini called")
    print(f"[DEBUG] gemini_text: {context.gemini_text[:100]}")
   
    output = OutputText(value=context.gemini_text)
    classes = Classes(value=context.gemini_classes if context.gemini_classes else [])
    
    

    geminiOutputs = GeminiOutputs(output=output, classes=classes)
    geminiResponse = GeminiResponse(outputs=geminiOutputs)
    geminiExecutor = GeminiExecutor(value=geminiResponse)
    executor = ConfigExecutor(value=geminiExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    
    return package.build_model(context)
