"""Language configuration utilities for Nok PDF Translator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Tuple

import re
import textwrap

from .textwrap_japanese import fw_fill


@dataclass(frozen=True)
class LanguageConfig:
    """Configuration for a supported target language."""

    code: str
    label: str
    model_name: str
    tokenizer_name: str
    wrap_text: Callable[[str, int], str]
    min_length: int = 0
    skip_prefixes: Tuple[str, ...] = ()
    validator: Callable[[str], bool] | None = None
    max_length: int = 512


def _wrap_japanese(text: str, width: int) -> str:
    """Wrap Japanese text respecting full-width characters."""

    return fw_fill(text=text, width=max(width, 1))


def _wrap_latin(text: str, width: int) -> str:
    """Wrap Latin-based text."""

    return textwrap.fill(text, width=max(width, 1))


_JAPANESE_EXCLUSION_PATTERN = re.compile(
    r"[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3400-\u4DBF\uFF66-\uFF9F]"
)


def _is_mostly_japanese(text: str) -> bool:
    """Return True when the text is primarily composed of Japanese characters."""

    stripped = text.strip()
    if not stripped:
        return False
    non_japanese = len(_JAPANESE_EXCLUSION_PATTERN.findall(stripped))
    return non_japanese <= 0.8 * len(stripped)


LANGUAGE_CONFIGS: Dict[str, LanguageConfig] = {
    "ja": LanguageConfig(
        code="ja",
        label="Japanese",
        model_name="staka/fugumt-en-ja",
        tokenizer_name="staka/fugumt-en-ja",
        wrap_text=_wrap_japanese,
        min_length=20,
        skip_prefixes=("「この版",),
        validator=_is_mostly_japanese,
    ),
    "pt-br": LanguageConfig(
        code="pt-br",
        label="Portuguese (Brazil)",
        model_name="Helsinki-NLP/opus-mt-en-pt",
        tokenizer_name="Helsinki-NLP/opus-mt-en-pt",
        wrap_text=_wrap_latin,
        min_length=5,
    ),
}

DEFAULT_LANGUAGE_CODE = "ja"


def get_language_config(code: str) -> LanguageConfig:
    """Return the configuration for a target language."""

    normalized_code = normalize_language_code(code)
    return LANGUAGE_CONFIGS[normalized_code]


def normalize_language_code(code: str) -> str:
    """Normalize and validate a target language code."""

    normalized = code.lower()
    if normalized not in LANGUAGE_CONFIGS:
        supported = ", ".join(sorted(LANGUAGE_CONFIGS))
        raise ValueError(
            f"Unsupported target language '{code}'. Supported languages: {supported}."
        )
    return normalized


def supported_language_codes() -> Iterable[str]:
    """Return an iterable with all supported language codes."""

    return LANGUAGE_CONFIGS.keys()


def language_help_text() -> str:
    """Return a human readable description of the supported languages."""

    return ", ".join(
        f"{config.code} ({config.label})" for config in LANGUAGE_CONFIGS.values()
    )


__all__ = [
    "LanguageConfig",
    "LANGUAGE_CONFIGS",
    "DEFAULT_LANGUAGE_CODE",
    "get_language_config",
    "normalize_language_code",
    "supported_language_codes",
    "language_help_text",
]
