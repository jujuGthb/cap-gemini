from sdks.novavision.src.helper.package import PackageHelper
from components.CapGemini.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    GeminiExecutor,
    GeminiResponse,
    GeminiOutputs,
    OutputText,
    OutputClasses
)
def build_response_gemini(context):
   
    outputText = OutputText(value=context.output_text)
    outputClasses = OutputClasses(value=context.output_classes)

    geminiOutputs = GeminiOutputs(outputText=outputText,outputClasses=outputClasses)
    geminiResponse = GeminiResponse(outputs=geminiOutputs)
    geminiExecutor = GeminiExecutor(value=geminiResponse)
    executor = ConfigExecutor(value=geminiExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)

   
    packageModel = package.build_model(context)

    return packageModel
