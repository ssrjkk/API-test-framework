from typing import Optional, Dict, Any
import time
import threading
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.config import get_config
from utils.logger import logger

MIN_REQUEST_INTERVAL = 1.0


class HTTPClient:
    _lock = threading.Lock()
    _last_request_time: float = 0.0

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 3,
    ) -> None:
        config = get_config()

        self.base_url = base_url or config.base_url
        self.timeout = timeout or config.timeout
        self.max_retries = max_retries

        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self) -> None:
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "API-Test-Framework/1.0",
            }
        )

        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20,
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        logger.info(f"HTTPClient initialized: base_url={self.base_url}, timeout={self.timeout}")

    def _throttle(self) -> None:
        with HTTPClient._lock:
            elapsed = time.monotonic() - HTTPClient._last_request_time
            if elapsed < MIN_REQUEST_INTERVAL:
                time.sleep(MIN_REQUEST_INTERVAL - elapsed)
            HTTPClient._last_request_time = time.monotonic()

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        self._throttle()
        url = self._build_url(path)
        logger.info(f"GET {url} params={params}")

        start_time = time.time()
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
            self._log_response("GET", url, response, start_time)
            return response
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout on GET {url}: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"ConnectionError on GET {url}: {e}")
            raise

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        self._throttle()
        url = self._build_url(path)
        logger.info(f"POST {url} json={json}")

        start_time = time.time()
        try:
            response = self.session.post(
                url,
                json=json,
                headers=headers,
                timeout=self.timeout,
            )
            self._log_response("POST", url, response, start_time)
            return response
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout on POST {url}: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"ConnectionError on POST {url}: {e}")
            raise

    def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        self._throttle()
        url = self._build_url(path)
        logger.info(f"PUT {url} json={json}")

        start_time = time.time()
        try:
            response = self.session.put(
                url,
                json=json,
                headers=headers,
                timeout=self.timeout,
            )
            self._log_response("PUT", url, response, start_time)
            return response
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout on PUT {url}: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"ConnectionError on PUT {url}: {e}")
            raise

    def delete(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        self._throttle()
        url = self._build_url(path)
        logger.info(f"DELETE {url}")

        start_time = time.time()
        try:
            response = self.session.delete(
                url,
                headers=headers,
                timeout=self.timeout,
            )
            self._log_response("DELETE", url, response, start_time)
            return response
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout on DELETE {url}: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"ConnectionError on DELETE {url}: {e}")
            raise

    def _build_url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"

    def _log_response(
        self,
        method: str,
        url: str,
        response: requests.Response,
        start_time: float,
    ) -> None:
        elapsed_ms = (time.time() - start_time) * 1000

        if response.status_code >= 500:
            logger.warning(
                f"{method} {url} -> {response.status_code} ({elapsed_ms:.0f}ms) [SERVER ERROR]"
            )
        elif response.status_code >= 400:
            logger.warning(f"{method} {url} -> {response.status_code} ({elapsed_ms:.0f}ms)")
        else:
            logger.info(f"{method} {url} -> {response.status_code} ({elapsed_ms:.0f}ms)")

    def close(self) -> None:
        self.session.close()
        logger.info("HTTPClient session closed")
