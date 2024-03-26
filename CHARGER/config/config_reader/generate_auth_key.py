from pathlib import Path
import os
import yaml
import secrets

current_path = Path(__file__).absolute().parents[1]

class AuthorizationSystem:
    def __init__(self, auth_path) -> None:
        self.AUTH_PATH = auth_path
        self.check_path()

    def check_path(self):
        if not os.path.exists(self.AUTH_PATH):
            with open(self.AUTH_PATH, "a") as f:
                f.write(self.generate_auth_key())
        else: pass 


    def read_local_key(self):
        if os.path.exists(self.AUTH_PATH):
            with open(self.AUTH_PATH, "r") as f:
                return f.read()

    def generate_auth_key(self):
        return secrets.token_hex(128)
    