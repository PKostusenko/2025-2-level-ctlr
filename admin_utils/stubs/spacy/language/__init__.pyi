from typing import Protocol, runtime_checkable

from spacy.tokens import Doc

@runtime_checkable
class Language(Protocol):
    def analyze_pipes(self) -> dict | None: ...
    def __call__(self, text: str) -> Doc: ...
