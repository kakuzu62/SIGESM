"""Military value objects."""

from domain.military.value_objects.cpf import CPF
from domain.military.value_objects.full_name import FullName
from domain.military.value_objects.military_id import MilitaryId
from domain.military.value_objects.military_status import MilitaryStatus
from domain.military.value_objects.phone import Phone
from domain.military.value_objects.rank import Rank

__all__ = ["CPF", "FullName", "MilitaryId", "MilitaryStatus", "Phone", "Rank"]
