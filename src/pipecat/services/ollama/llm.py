#
# Copyright (c) 2024-2026, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Ollama LLM service implementation for the Pipecat framework."""

from dataclasses import dataclass
import os
from typing import Optional
import warnings

from loguru import logger

from pipecat.services.openai.base_llm import BaseOpenAILLMService
from pipecat.services.openai.llm import OpenAILLMService


@dataclass
class OllamaLLMSettings(BaseOpenAILLMService.Settings):
    """Settings for OllamaLLMService."""

    pass


class OllamaLLMService(OpenAILLMService):
    """Ollama LLM service that provides local language model capabilities.

    This service extends OpenAILLMService to work with locally hosted Ollama models,
    providing a compatible interface for running large language models locally.
    """

    # Ollama doesn't support the "developer" message role (it seems to quietly
    # ignore "developer" messages).
    # This value is used by BaseOpenAILLMService when calling the adapter.
    supports_developer_role = False

    Settings = OllamaLLMSettings
    _settings: Settings

    def __init__(
        self,
        *,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        settings: Optional[Settings] = None,
        **kwargs,
    ):
        """Initialize Ollama LLM service.

        Args:
            model: The Ollama model to use. Defaults to ``llama2``.

                .. deprecated:: 0.0.105
                    Use ``settings=OllamaLLMService.Settings(model=...)`` instead.

            base_url: The base URL for the Ollama API endpoint. If omitted,
                reads ``PIPECAT_OLLAMA_BASE_URL`` and then falls back to
                ``http://127.0.0.1:11434/v1``.
            settings: Runtime-updatable settings. When provided alongside deprecated
                parameters, ``settings`` values take precedence.
            **kwargs: Additional keyword arguments passed to OpenAILLMService.
        """
        # 1. Initialize default_settings with hardcoded defaults
        default_settings = self.Settings(model="llama2")

        # 2. Apply direct init arg overrides (deprecated)
        if model is not None:
            self._warn_init_param_moved_to_settings("model", "model")
            default_settings.model = model

        # 3. (No step 3, as there's no params object to apply)

        # 4. Apply settings delta (canonical API, always wins)
        if settings is not None:
            default_settings.apply_update(settings)

        resolved_base_url = (
            base_url or os.getenv("PIPECAT_OLLAMA_BASE_URL") or "http://127.0.0.1:11434/v1"
        )
        super().__init__(
            base_url=resolved_base_url,
            api_key="ollama",
            settings=default_settings,
            **kwargs,
        )

    def create_client(self, base_url=None, **kwargs):
        """Create OpenAI-compatible client for Ollama.

        Args:
            base_url: The base URL for the API. If None, uses instance base_url.
            **kwargs: Additional keyword arguments passed to the parent create_client method.

        Returns:
            An OpenAI-compatible client configured for Ollama.
        """
        logger.debug(f"Creating Ollama client with api {base_url}")
        return super().create_client(base_url=base_url, **kwargs)


class OLLamaLLMService(OllamaLLMService):
    """Deprecated alias for :class:`OllamaLLMService`."""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "OLLamaLLMService is deprecated; use OllamaLLMService instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
