from abc import ABC, abstractmethod

from fastapi import File


class Fileparser(ABC):
    @abstractmethod
    async def parse_file(self, file: File) -> str:
        """
        Parse the given file and return the extracted criteria as a dictionary.

        :param file: The file content as bytes.
        :return: A dictionary containing the extracted criteria.
        """
        pass

