from pydantic import validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Outputs, Configs, Response, Request, Output, Input, Config
)




class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Image"


class InputPrompt(Input):
    name: Literal["inputPrompt"] = "inputPrompt"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Prompt"


class InputClasses(Input):
    name: Literal["inputClasses"] = "inputClasses"
    value: Union[List[str], str]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Classes"


class InputApiKey(Input):
    name: Literal["inputApiKey"] = "inputApiKey"
    value: str = "rf_key:account"
    type: Literal["string"] = "string"

    class Config:
        title = "API Key"


class InputModelVersion(Input):
    name: Literal["inputModelVersion"] = "inputModelVersion"
    value: str = "gemini-3-pro-preview"
    type: Literal["string"] = "string"

    class Config:
        title = "Model Version"


class InputTemperature(Input):
    name: Literal["inputTemperature"] = "inputTemperature"
    value: float = 1.0
    type: Literal["number"] = "number"

    class Config:
        title = "Temperature"



class OutputText(Output):
    name: Literal["outputText"] = "outputText"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Output Text"


class OutputClasses(Output):
    name: Literal["outputClasses"] = "outputClasses"
    value: Union[List[str], str]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Output Classes"




class MaxTokens(Config):
    name: Literal["maxTokens"] = "maxTokens"
    value: int = 1024
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["e.g. 1024"] = "e.g. 1024"

    class Config:
        title = "Max Tokens"


class MaxConcurrentRequests(Config):
    name: Literal["maxConcurrentRequests"] = "maxConcurrentRequests"
    value: int = 4
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["e.g. 4"] = "e.g. 4"

    class Config:
        title = "Max Concurrent Requests"


class ThinkingLevel(Config):
    name: Literal["thinkingLevel"] = "thinkingLevel"
    value: str = "high"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["low or high"] = "low or high"

    class Config:
        title = "Thinking Level"


class CodeExecutionTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class CodeExecutionFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class CodeExecution(Config):
    name: Literal["codeExecution"] = "codeExecution"
    value: Union[CodeExecutionFalse, CodeExecutionTrue]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Code Execution"



class UnconstrainedModeConfigs(Configs):
    inputPrompt: InputPrompt
    inputTemperature: InputTemperature
    thinkingLevel: ThinkingLevel
    codeExecution: CodeExecution
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeUnconstrained(Config):
    name: Literal["unconstrained"] = "unconstrained"
    value: Literal["unconstrained"] = "unconstrained"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: UnconstrainedModeConfigs

    class Config:
        title = "Open Prompt"


class OCRModeConfigs(Configs):
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeOCR(Config):
    name: Literal["ocr"] = "ocr"
    value: Literal["ocr"] = "ocr"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: OCRModeConfigs

    class Config:
        title = "Text Recognition (OCR)"




class VQAModeConfigs(Configs):
    inputPrompt: InputPrompt
    inputTemperature: InputTemperature
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeVQA(Config):
    name: Literal["visual-question-answering"] = "visual-question-answering"
    value: Literal["visual-question-answering"] = "visual-question-answering"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: VQAModeConfigs

    class Config:
        title = "Visual Question Answering"



class CaptionModeConfigs(Configs):
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeCaption(Config):
    name: Literal["caption"] = "caption"
    value: Literal["caption"] = "caption"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: CaptionModeConfigs

    class Config:
        title = "Captioning (Short)"




class DetailedCaptionModeConfigs(Configs):
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeDetailedCaption(Config):
    name: Literal["detailed-caption"] = "detailed-caption"
    value: Literal["detailed-caption"] = "detailed-caption"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: DetailedCaptionModeConfigs

    class Config:
        title = "Captioning (Detailed)"


class ClassificationModeConfigs(Configs):
    inputClasses: InputClasses
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeClassification(Config):
    name: Literal["classification"] = "classification"
    value: Literal["classification"] = "classification"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: ClassificationModeConfigs

    class Config:
        title = "Single-Label Classification"


class MultiLabelClassificationModeConfigs(Configs):
    inputClasses: InputClasses
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeMultiLabelClassification(Config):
    name: Literal["multi-label-classification"] = "multi-label-classification"
    value: Literal["multi-label-classification"] = "multi-label-classification"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: MultiLabelClassificationModeConfigs

    class Config:
        title = "Multi-Label Classification"



class ObjectDetectionModeConfigs(Configs):
    inputClasses: InputClasses
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeObjectDetection(Config):
    name: Literal["object-detection"] = "object-detection"
    value: Literal["object-detection"] = "object-detection"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: ObjectDetectionModeConfigs

    class Config:
        title = "Unprompted Object Detection"




class StructuredAnsweringModeConfigs(Configs):
    inputPrompt: InputPrompt
    maxTokens: MaxTokens
    maxConcurrentRequests: MaxConcurrentRequests


class ModeStructuredAnswering(Config):
    name: Literal["structured-answering"] = "structured-answering"
    value: Literal["structured-answering"] = "structured-answering"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    configs: StructuredAnsweringModeConfigs

    class Config:
        title = "Structured Output Generation"

class TaskType(Config):
    name: Literal["taskType"] = "taskType"
    value: Union[
        ModeUnconstrained,
        ModeOCR,
        ModeVQA,
        ModeCaption,
        ModeDetailedCaption,
        ModeClassification,
        ModeMultiLabelClassification,
        ModeObjectDetection,
        ModeStructuredAnswering,
    ]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task Type"



class GeminiInputs(Inputs):
    inputImage: InputImage
    inputApiKey: InputApiKey
    inputModelVersion: InputModelVersion


class GeminiConfigs(Configs):
    taskType: TaskType


class GeminiOutputs(Outputs):
    outputText: OutputText
    outputClasses: OutputClasses


class GeminiRequest(Request):
    inputs: Optional[GeminiInputs]
    configs: Optional[GeminiConfigs]

    class Config:
        json_schema_extra = {"target": "configs"}


class GeminiResponse(Response):
    outputs: GeminiOutputs


class GeminiExecutor(Config):
    name: Literal["GeminiExecutor"] = "GeminiExecutor"
    value: Union[GeminiRequest, GeminiResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Google Gemini"
        json_schema_extra = {"target": {"value": 0}}




class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GeminiExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        



class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    name: Literal["GoogleGemini"] = "GoogleGemini"
    configs: PackageConfigs
    type: Literal["component"] = "component"