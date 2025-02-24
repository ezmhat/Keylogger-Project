from abc import ABC, abstractmethod
from typing import List

class IKeyLogger(ABC):
    @abstractmethod
    def start_logging(self):
        pass

    @abstractmethod
    def on_press(self, key):
        pass

    @abstractmethod
    def stop_logging(self):
        pass

    @abstractmethod
    def get_logged_keys(self) -> List[str]:
        pass


