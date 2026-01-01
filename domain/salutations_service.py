# domain/salutations_service.py
# -*- coding: utf-8 -*-

# domain/salutation_service.py
# -*- coding: utf-8 -*-

from typing import List, Optional
from constants.salutations import DEFAULT_SALUTATIONS


class SalutationService:
    """
    Provides valid salutations for the application.

    Responsibility:
    - Always return a usable list of salutations
    - Prefer database-backed values if available
    - Fall back to static defaults if the database is unavailable
    - Prepare for future multi-language support

    This service contains business logic only.
    It has no knowledge of UI, database connections, or persistence.
    """

    def __init__(self, salutation_repository=None, language: str = "de"):
        """
        :param salutation_repository:
            Optional repository providing salutations from a database.
            Must implement: get_salutations(language) -> list[str]

        :param language:
            ISO language code (currently only 'de' supported).
        """
        self._repo = salutation_repository
        self._language = language

    def get_salutations(self) -> List[str]:
        """
        Returns a list of salutations.

        Database values take precedence.
        Falls back to static defaults if no data source is available.
        """
        # Try database first
        if self._repo:
            try:
                values = self._repo.get_salutations(self._language)
                if values:
                    return values
            except Exception:
                # Domain decision: DB failure must not break the app
                pass

        # Fallback: static defaults
        return self._get_fallback_salutations()

    def _get_fallback_salutations(self) -> List[str]:
        """
        Returns static fallback salutations.
        """
        return DEFAULT_SALUTATIONS.get(self._language, [])
