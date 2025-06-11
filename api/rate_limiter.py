import time
from fastapi import HTTPException, status
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def _cleanup_old_requests(self, key: str):
        now = time.time()
        if key in self.requests:
            self.requests[key] = [
                timestamp for timestamp in self.requests[key]
                if now - timestamp < self.window_seconds
            ]

    def allow_request(self, key: str) -> bool:
        self._cleanup_old_requests(key)
        if len(self.requests[key]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for key: {key}")
            return False
        self.requests[key].append(time.time())
        return True

    def limit(self, key: str = "global"):
        """Decorator or direct call to check rate limit."""
        if not self.allow_request(key):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {self.window_seconds} seconds.",
            )
        return True
