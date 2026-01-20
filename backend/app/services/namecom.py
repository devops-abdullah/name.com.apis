import requests
from typing import Optional, Dict, List, Any
from app.config import settings

class NamecomService:
    """Service to interact with name.com API"""
    
    BASE_URL = "https://api.name.com/v4"
    
    def __init__(self, api_token: Optional[str] = None, username: Optional[str] = None):
        self.api_token = api_token or settings.NAMECOM_API_TOKEN
        self.username = username or settings.NAMECOM_USERNAME
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to name.com API"""
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def get_domains(self) -> List[Dict[str, Any]]:
        """Get all domains"""
        response = self._make_request("GET", "/domains")
        return response.get("domains", [])
    
    def get_domain(self, domain_name: str) -> Dict[str, Any]:
        """Get specific domain details"""
        response = self._make_request("GET", f"/domains/{domain_name}")
        return response
    
    def get_dns_records(self, domain_name: str) -> List[Dict[str, Any]]:
        """Get all DNS records for a domain"""
        response = self._make_request("GET", f"/domains/{domain_name}/records")
        return response.get("records", [])
    
    def get_dns_record(self, domain_name: str, record_id: int) -> Dict[str, Any]:
        """Get specific DNS record"""
        response = self._make_request("GET", f"/domains/{domain_name}/records/{record_id}")
        return response
    
    def create_dns_record(
        self,
        domain_name: str,
        name: str,
        type: str,
        content: str,
        ttl: int = 3600,
        priority: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create DNS record"""
        data = {
            "name": name,
            "type": type,
            "content": content,
            "ttl": ttl
        }
        
        if priority:
            data["priority"] = priority
        
        response = self._make_request(
            "POST",
            f"/domains/{domain_name}/records",
            data
        )
        return response
    
    def update_dns_record(
        self,
        domain_name: str,
        record_id: int,
        content: Optional[str] = None,
        ttl: Optional[int] = None,
        priority: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update DNS record"""
        data = {}
        if content:
            data["content"] = content
        if ttl:
            data["ttl"] = ttl
        if priority is not None:
            data["priority"] = priority
        
        response = self._make_request(
            "PUT",
            f"/domains/{domain_name}/records/{record_id}",
            data
        )
        return response
    
    def delete_dns_record(self, domain_name: str, record_id: int) -> bool:
        """Delete DNS record"""
        self._make_request("DELETE", f"/domains/{domain_name}/records/{record_id}")
        return True

namecom_service = NamecomService()
