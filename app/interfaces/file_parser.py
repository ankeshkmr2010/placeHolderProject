from abc import ABC, abstractmethod

from fastapi import File


class Fileparser(ABC):
    """
    Abstract base class for file parsing.

    This class defines the interface for parsing files and extracting criteria.
    Subclasses must implement the abstract method to provide specific functionality.
    """

    @abstractmethod
    async def parse_file(self, file: File) -> str:
        """
        Abstract method to parse the given file and return the extracted criteria.

        Args:
            file (File): The file content as bytes.

        Returns:
            str: A string containing the extracted criteria.
        """
        pass