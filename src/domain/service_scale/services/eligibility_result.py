from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from domain.service_scale.services.eligibility_reason import EligibilityReason


@dataclass(frozen=True, slots=True)
class EligibilityResult:
    """Immutable result returned by service scale eligibility evaluation."""

    eligible: bool
    reasons: tuple[EligibilityReason, ...]
    warnings: tuple[str, ...]
    metadata: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        reasons: tuple[EligibilityReason, ...],
        warnings: tuple[str, ...] = (),
        metadata: Mapping[str, Any] | None = None,
    ) -> EligibilityResult:
        """Create an immutable eligibility result."""
        return cls(
            eligible=len(reasons) == 0,
            reasons=reasons,
            warnings=warnings,
            metadata=MappingProxyType(dict(metadata or {})),
        )
