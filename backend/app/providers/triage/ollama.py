"""Ollama offline triage through its local-network chat API."""

import os
from collections.abc import Callable
from typing import Any
from urllib.request import urlopen

from app.providers.triage.base import MalformedOutputError, TriageResult
from app.providers.triage.llm import (
    RESULT_SCHEMA,
    SYSTEM_PROMPT,
    parse_result,
    post_json,
    untrusted_message,
)

DEFAULT_OLLAMA_URL = "http://ollama:11434"
DEFAULT_OLLAMA_MODEL = "gemma3:1b"


class OllamaTriage:
    name = "llm:ollama"

    def __init__(
        self,
        base_url: str = DEFAULT_OLLAMA_URL,
        model: str = DEFAULT_OLLAMA_MODEL,
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        self._url = base_url.rstrip("/") + "/api/chat"
        self._model = model
        self._opener = opener

    @classmethod
    def from_environment(cls) -> "OllamaTriage":
        return cls(
            os.environ.get("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL),
            os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL),
        )

    def triage(self, text: str, location: str) -> TriageResult:
        response = post_json(
            self._url,
            {
                "model": self._model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": untrusted_message(text, location)},
                ],
                "format": RESULT_SCHEMA,
                "stream": False,
            },
            {},
            self._opener,
        )
        message = response.get("message")
        if not isinstance(message, dict):
            raise MalformedOutputError("provider returned no message")
        return parse_result(message.get("content"))
