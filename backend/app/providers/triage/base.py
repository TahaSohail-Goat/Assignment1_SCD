"""The triage interface of assignment section 2.5: the result model, the provider protocol
and the errors a provider may raise.

Every provider, hosted or not, is used through ``TriageProvider``. The orchestration in
``app/services/triage.py`` treats model output as untrusted: it validates the result against
``TriageResult`` again, whatever the provider claims to have done.
"""

from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain import AI_SUMMARY_MAX, Category, Priority


class TriageResult(BaseModel):
    """What a provider returns (assignment section 2.5, "The interface")."""

    # Instances are validated again on use, so a result built without validation
    # (for example ``model_construct``) cannot slip past the orchestration.
    model_config = ConfigDict(extra="forbid", revalidate_instances="always")

    category: Category
    priority: Priority
    summary: str = Field(min_length=1, max_length=AI_SUMMARY_MAX)
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("summary")
    @classmethod
    def _one_line(cls, value: str) -> str:
        value = value.strip()
        if not value or "\n" in value or "\r" in value:
            raise ValueError("the summary must be one non-empty line")
        return value


class TriageProvider(Protocol):
    name: str

    def triage(self, text: str, location: str) -> TriageResult: ...


class TriageProviderError(Exception):
    """A provider failed. ``retryable`` follows assignment section 2.5, item 3: retry once,
    with jitter, on a timeout, a 429 or a 5xx; never retry a 400."""

    retryable = False


class ProviderTimeoutError(TriageProviderError):
    retryable = True


class ProviderRateLimitedError(TriageProviderError):
    """The provider answered 429."""

    retryable = True


class ProviderServerError(TriageProviderError):
    """The provider answered 5xx."""

    retryable = True


class ProviderRequestError(TriageProviderError):
    """The provider answered 400: the request was wrong and will be wrong again."""

    retryable = False


class MalformedOutputError(TriageProviderError):
    """The provider's output was not a valid ``TriageResult`` (prose, a code fence, a category
    outside the enum, an over-long summary)."""

    retryable = False
