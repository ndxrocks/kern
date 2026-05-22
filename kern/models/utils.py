from typing import Optional, Union

from kern.models.base import Model


def _get_model_class(model_id: str, model_provider: str) -> Model:
    if model_provider == "aimlapi":
        from kern.models.aimlapi import AIMLAPI

        return AIMLAPI(id=model_id)

    elif model_provider == "anthropic":
        from kern.models.anthropic import Claude

        return Claude(id=model_id)

    elif model_provider == "aws-bedrock":
        from kern.models.aws import AwsBedrock

        return AwsBedrock(id=model_id)

    elif model_provider == "aws-claude":
        from kern.models.aws import Claude as AWSClaude

        return AWSClaude(id=model_id)

    elif model_provider == "azure-ai-foundry":
        from kern.models.azure import AzureAIFoundry

        return AzureAIFoundry(id=model_id)

    elif model_provider == "azure-openai":
        from kern.models.azure import AzureOpenAI

        return AzureOpenAI(id=model_id)

    elif model_provider == "cerebras":
        from kern.models.cerebras import Cerebras

        return Cerebras(id=model_id)

    elif model_provider == "cerebras-openai":
        from kern.models.cerebras import CerebrasOpenAI

        return CerebrasOpenAI(id=model_id)

    elif model_provider == "cohere":
        from kern.models.cohere import Cohere

        return Cohere(id=model_id)

    elif model_provider == "cometapi":
        from kern.models.cometapi import CometAPI

        return CometAPI(id=model_id)

    elif model_provider == "dashscope":
        from kern.models.dashscope import DashScope

        return DashScope(id=model_id)

    elif model_provider == "deepinfra":
        from kern.models.deepinfra import DeepInfra

        return DeepInfra(id=model_id)

    elif model_provider == "deepseek":
        from kern.models.deepseek import DeepSeek

        return DeepSeek(id=model_id)

    elif model_provider == "fireworks":
        from kern.models.fireworks import Fireworks

        return Fireworks(id=model_id)

    elif model_provider == "google":
        from kern.models.google import Gemini

        return Gemini(id=model_id)

    elif model_provider == "groq":
        from kern.models.groq import Groq

        return Groq(id=model_id)

    elif model_provider == "huggingface":
        from kern.models.huggingface import HuggingFace

        return HuggingFace(id=model_id)

    elif model_provider == "ibm":
        from kern.models.ibm import WatsonX

        return WatsonX(id=model_id)

    elif model_provider == "internlm":
        from kern.models.internlm import InternLM

        return InternLM(id=model_id)

    elif model_provider == "langdb":
        from kern.models.langdb import LangDB

        return LangDB(id=model_id)

    elif model_provider == "litellm":
        from kern.models.litellm import LiteLLM

        return LiteLLM(id=model_id)

    elif model_provider == "litellm-openai":
        from kern.models.litellm import LiteLLMOpenAI

        return LiteLLMOpenAI(id=model_id)

    elif model_provider == "llama-cpp":
        from kern.models.llama_cpp import LlamaCpp

        return LlamaCpp(id=model_id)

    elif model_provider == "llama-openai":
        from kern.models.meta import LlamaOpenAI

        return LlamaOpenAI(id=model_id)

    elif model_provider == "lmstudio":
        from kern.models.lmstudio import LMStudio

        return LMStudio(id=model_id)

    elif model_provider == "meta":
        from kern.models.meta import Llama

        return Llama(id=model_id)

    elif model_provider == "mistral":
        from kern.models.mistral import MistralChat

        return MistralChat(id=model_id)

    elif model_provider == "moonshot":
        from kern.models.moonshot import MoonShot

        return MoonShot(id=model_id)

    elif model_provider == "nebius":
        from kern.models.nebius import Nebius

        return Nebius(id=model_id)

    elif model_provider == "neosantara":
        from kern.models.neosantara import Neosantara

        return Neosantara(id=model_id)

    elif model_provider == "nexus":
        from kern.models.nexus import Nexus

        return Nexus(id=model_id)

    elif model_provider == "nvidia":
        from kern.models.nvidia import Nvidia

        return Nvidia(id=model_id)

    elif model_provider == "ollama":
        from kern.models.ollama import Ollama

        return Ollama(id=model_id)

    elif model_provider == "openai":
        from kern.models.openai import OpenAIChat

        return OpenAIChat(id=model_id)

    elif model_provider == "openai-responses":
        from kern.models.openai import OpenAIResponses

        return OpenAIResponses(id=model_id)

    elif model_provider == "openrouter":
        from kern.models.openrouter import OpenRouter

        return OpenRouter(id=model_id)

    elif model_provider == "perplexity":
        from kern.models.perplexity import Perplexity

        return Perplexity(id=model_id)

    elif model_provider == "portkey":
        from kern.models.portkey import Portkey

        return Portkey(id=model_id)

    elif model_provider == "requesty":
        from kern.models.requesty import Requesty

        return Requesty(id=model_id)

    elif model_provider == "sambanova":
        from kern.models.sambanova import Sambanova

        return Sambanova(id=model_id)

    elif model_provider == "siliconflow":
        from kern.models.siliconflow import Siliconflow

        return Siliconflow(id=model_id)

    elif model_provider == "together":
        from kern.models.together import Together

        return Together(id=model_id)

    elif model_provider == "vercel":
        from kern.models.vercel import V0

        return V0(id=model_id)

    elif model_provider == "vertexai-claude":
        from kern.models.vertexai.claude import Claude as VertexAIClaude

        return VertexAIClaude(id=model_id)

    elif model_provider == "vllm":
        from kern.models.vllm import VLLM

        return VLLM(id=model_id)

    elif model_provider == "xai":
        from kern.models.xai import xAI

        return xAI(id=model_id)

    else:
        raise ValueError(f"Model provider '{model_provider}' is not supported.")


def _parse_model_string(model_string: str) -> Model:
    if not model_string or not isinstance(model_string, str):
        raise ValueError(f"Model string must be a non-empty string, got: {model_string}")

    if ":" not in model_string:
        raise ValueError(
            f"Invalid model string format: '{model_string}'. Model strings should be in format '<provider>:<model_id>' e.g. 'openai:gpt-4o'"
        )

    parts = model_string.split(":", 1)
    if len(parts) != 2:
        raise ValueError(
            f"Invalid model string format: '{model_string}'. Model strings should be in format '<provider>:<model_id>' e.g. 'openai:gpt-4o'"
        )

    model_provider, model_id = parts
    model_provider = model_provider.strip().lower()
    model_id = model_id.strip()

    if not model_provider or not model_id:
        raise ValueError(
            f"Invalid model string format: '{model_string}'. Model strings should be in format '<provider>:<model_id>' e.g. 'openai:gpt-4o'"
        )

    return _get_model_class(model_id, model_provider)


def get_model(model: Union[Model, str, None]) -> Optional[Model]:
    if model is None:
        return None
    elif isinstance(model, Model):
        return model
    elif isinstance(model, str):
        return _parse_model_string(model)
    else:
        raise ValueError("Model must be a Model instance, string, or None")
