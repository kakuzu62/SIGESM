from __future__ import annotations

from dataclasses import dataclass

from presentation.framework.mvvm import ViewModel


@dataclass(frozen=True, slots=True)
class DashboardMetric:
    """Dashboard metric displayed in an initial card."""

    title: str
    value: str


class DashboardViewModel(ViewModel):
    """View model for the initial dashboard."""

    @property
    def metrics(self) -> tuple[DashboardMetric, ...]:
        """Return initial dashboard metrics."""
        return (
            DashboardMetric("Militares", "0"),
            DashboardMetric("Escalas", "0"),
            DashboardMetric("Organizacoes", "0"),
            DashboardMetric("Pendencias", "0"),
            DashboardMetric("Auditoria", "0"),
        )
