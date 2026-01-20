import hvac
from app.config import settings
import json

class VaultService:
    def __init__(self):
        self.client = hvac.Client(url=settings.VAULT_ADDR, token=settings.VAULT_TOKEN)
    
    def get_namecom_credentials(self) -> dict:
        """Retrieve name.com credentials from Vault"""
        try:
            response = self.client.secrets.kv.read_secret_version(
                path=settings.VAULT_SECRET_PATH
            )
            return response['data']['data']
        except Exception as e:
            raise Exception(f"Error retrieving credentials from Vault: {str(e)}")
    
    def store_user_token(self, user_id: int, token: str):
        """Store user JWT token in Vault"""
        try:
            path = f"secret/data/users/{user_id}/token"
            self.client.secrets.kv.create_or_update_secret(
                path=path,
                secret_dict={"token": token}
            )
        except Exception as e:
            raise Exception(f"Error storing token in Vault: {str(e)}")
    
    def get_user_token(self, user_id: int) -> str:
        """Retrieve user JWT token from Vault"""
        try:
            path = f"secret/data/users/{user_id}/token"
            response = self.client.secrets.kv.read_secret_version(path=path)
            return response['data']['data']['token']
        except Exception as e:
            raise Exception(f"Error retrieving token from Vault: {str(e)}")
    
    def revoke_user_token(self, user_id: int):
        """Delete user token from Vault"""
        try:
            path = f"secret/data/users/{user_id}/token"
            self.client.secrets.kv.delete_secret_version(path=path)
        except Exception as e:
            raise Exception(f"Error revoking token in Vault: {str(e)}")

vault_service = VaultService()
