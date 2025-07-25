from abc import ABC, abstractmethod
from typing import List


class Fileparser(ABC):
    @abstractmethod
    def parse_file(self, file: bytes) -> List[str]:
        """
        Parse the given file and return the extracted criteria as a dictionary.

        :param file: The file content as bytes.
        :return: A dictionary containing the extracted criteria.
        """
        pass

