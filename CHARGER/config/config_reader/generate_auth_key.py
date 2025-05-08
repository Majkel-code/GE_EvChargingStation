import os
import secrets
from pathlib import Path

current_path = Path(__file__).absolute().parents[1]


class AuthorizationSystem:
    def __init__(self, auth_path) -> None:
        self.AUTH_PATH = f"{auth_path}/AUTHORIZATION_KEY"
        self.check_path()

    def check_path(self):
        if not os.path.exists(self.AUTH_PATH):
            os.makedirs(self.AUTH_PATH, exist_ok=True)
            with open(f"{self.AUTH_PATH}/host_key.txt", "a") as f:
                f.write(self.generate_auth_key())
        else:
            pass

    def recreate_auth_key(self):
        if os.path.exists(f"{self.AUTH_PATH}/host_key.txt"):
            os.remove(f"{self.AUTH_PATH}/host_key.txt")
            with open(f"{self.AUTH_PATH}/host_key.txt", "a") as f:
                f.write(self.generate_auth_key())
        else:
            pass

    def read_local_key(self):
        if os.path.exists(f"{self.AUTH_PATH}/host_key.txt"):
            with open(f"{self.AUTH_PATH}/host_key.txt", "r") as f:
                return f.read()

    def generate_auth_key(self):
        return secrets.token_hex(128)
