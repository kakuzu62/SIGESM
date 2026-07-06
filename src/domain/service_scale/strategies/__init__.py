"""Scale generation strategies."""

from domain.service_scale.strategies.black_scale_strategy import BlackScaleStrategy
from domain.service_scale.strategies.red_scale_strategy import RedScaleStrategy
from domain.service_scale.strategies.scale_strategy import ScaleStrategy

__all__ = ["BlackScaleStrategy", "RedScaleStrategy", "ScaleStrategy"]
