import time
from functools import wraps
from typing import Callable, Optional, Tuple, Type

from tenacity import (
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
    retry,
    RetryError,
)

from utils.logger import logger


class RetryableError(Exception):
    pass


class NonRetryableError(Exception):
    pass


def create_retry_decorator(
    max_attempts: int = 3,
    delay: float = 1.0,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
) -> Callable:
    if retryable_exceptions is None:
        retryable_exceptions = (RetryableError,)

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_fixed(delay),
        retry=retry_if_exception_type(retryable_exceptions),
        reraise=True,
        before_sleep=lambda retry_state: logger.warning(
            f"Повторная попытка {retry_state.attempt_number}/{max_attempts} "
            f"после ошибки: {retry_state.outcome.exception()}"
        ),
    )


def retry_on_5xx_or_timeout(
    max_attempts: int = 3,
    delay: float = 1.0,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_fixed(delay),
            retry=retry_if_exception_type((TimeoutError, ConnectionError)),
            reraise=True,
            before_sleep=lambda retry_state: logger.warning(
                f"Попытка {retry_state.attempt_number}/{max_attempts}: "
                f"{type(retry_state.outcome.exception()).__name__}"
            ),
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
