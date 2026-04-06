import logging
import sys


class Logger:
    _instance: "Logger | None" = None
    _logger: logging.Logger | None = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
            instance._init_logger()
        return cls._instance

    def _init_logger(self) -> None:
        self._logger = logging.getLogger("api_tests")
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def set_level(self, level: str) -> None:
        if self._logger:
            numeric_level = getattr(logging, level.upper(), logging.INFO)
            self._logger.setLevel(numeric_level)
            for handler in self._logger.handlers:
                handler.setLevel(numeric_level)

    def info(self, message: str) -> None:
        if self._logger:
            self._logger.info(message)

    def debug(self, message: str) -> None:
        if self._logger:
            self._logger.debug(message)

    def warning(self, message: str) -> None:
        if self._logger:
            self._logger.warning(message)

    def error(self, message: str) -> None:
        if self._logger:
            self._logger.error(message)


logger = Logger()
