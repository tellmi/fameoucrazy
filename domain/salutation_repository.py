# domain/salutation_repository.py
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List

class SalutationRepository(ABC):
    """
    Interface for providing salutations from a data source (DB, API, etc).
    """

    @abstractmethod
    def get_salutations(self, language: str) -> List[str]:
        """
        Returns a list of salutations for the requested language.
        May raise an exception if the source is unavailable.
        """
        pass
