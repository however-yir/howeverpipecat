import pytest

from pipecat.services.ollama.llm import OLLamaLLMService, OllamaLLMService
from pipecat.services.openai.llm import OpenAILLMService


def test_ollama_base_url_comes_from_env(monkeypatch):
    captured = {}

    def fake_init(self, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(OpenAILLMService, "__init__", fake_init)
    monkeypatch.setenv("PIPECAT_OLLAMA_BASE_URL", "http://ollama.internal.example:11434/v1")

    OllamaLLMService()
    assert captured["base_url"] == "http://ollama.internal.example:11434/v1"
    assert captured["api_key"] == "ollama"


def test_legacy_ollama_class_alias_emits_warning(monkeypatch):
    def fake_init(self, **kwargs):
        return None

    monkeypatch.setattr(OpenAILLMService, "__init__", fake_init)

    with pytest.warns(DeprecationWarning):
        OLLamaLLMService()
