import requests
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)

class RapideAPI:
    """
    Un client HTTP miniature et élégant, conçu pour minimiser la mise en place
    des requêtes API, similaire à l'approche de FastAPI mais pour le côté client.
    """
    
    def __init__(self, base_url: str = "", default_headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        if default_headers:
            self.session.headers.update(default_headers)

    def _build_url(self, endpoint: str) -> str:
        """Construit l'URL finale en combinant la base et l'endpoint."""
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Méthode centrale pour envoyer des requêtes et gérer les erreurs."""
        url = self._build_url(endpoint)
        kwargs.setdefault("timeout", self.timeout)

        logger.debug(f"[{method}] {url} - {kwargs}")

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur API lors de la requête [{method}] {url}: {e}")
            raise e

        # Retourne automatiquement du JSON si le serveur renvoie ce type
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                return response.json()
            except ValueError:
                return response.text
                
        return response.text

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Union[Dict, str]] = None, json: Optional[Dict] = None, **kwargs) -> Any:
        return self.request("POST", endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint: str, data: Optional[Union[Dict, str]] = None, json: Optional[Dict] = None, **kwargs) -> Any:
        return self.request("PUT", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Any:
        return self.request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, data: Optional[Union[Dict, str]] = None, json: Optional[Dict] = None, **kwargs) -> Any:
        return self.request("PATCH", endpoint, data=data, json=json, **kwargs)

    def health(self):
        health = self.request("GET", "api/version")
        print(health)
        return health is not None
