from abc import ABC, abstractmethod


class BaseCache(ABC):
    @abstractmethod
    def connect(self):
        """Connect to the cache."""
        ...

    def get(self, key: str):
        """Get a value from the cache by key."""
        ...

    def set(self, key: str, value: any, ttl: int = None):
        """Set a value in the cache with an optional time-to-live."""
        ...

    def delete(self, key: str):
        """Delete a value from the cache by key."""
        ...

    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        ...

    def clear(self):
        """Clear the cache."""
        ...

    def ping(self):
        """Ping the cache to check if it's reachable."""
        ...
