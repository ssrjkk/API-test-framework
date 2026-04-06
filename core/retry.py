from functools import wraps
from collections.abc import Callable
from typing import Any

from tenacity import (
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
    retry,
)

from utils.logger import logger


class RetryableError(Exception):
    pass


class NonRetryableError(Exception):
    pass


def create_retry_decorator(
    max_attempts: int = 3,
    delay: float = 1.0,
    retryable_exceptions: tuple[type[Exception], ...] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    if retryable_exceptions is None:
        retryable_exceptions = (RetryableError,)

    def before_sleep(retry_state: Any) -> None:
        exc = retry_state.outcome.exception() if retry_state.outcome else "Unknown"
        logger.warning(
            f"Повторная попытка {retry_state.attempt_number}/{max_attempts} "
            f"после ошибки: {exc}"
        )

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_fixed(delay),
        retry=retry_if_exception_type(retryable_exceptions),
        reraise=True,
        before_sleep=before_sleep,
    )


def retry_on_5xx_or_timeout(
    max_attempts: int = 3,
    delay: float = 1.0,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def before_sleep(retry_state: Any) -> None:
            exc_type = (
                type(retry_state.outcome.exception()).__name__
                if retry_state.outcome
                else "Unknown"
            )
            logger.warning(f"Попытка {retry_state.attempt_number}/{max_attempts}: {exc_type}")

        @wraps(func)
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_fixed(delay),
            retry=retry_if_exception_type((TimeoutError, ConnectionError)),
            reraise=True,
            before_sleep=before_sleep,
        )
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        return wrapper

    return decorator
