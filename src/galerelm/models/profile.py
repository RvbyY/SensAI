import uuid
from typing import Literal

class Profile:
    def __init__(self, name: str, email: str, instructions: str):
        self.id = ""
        self.name: str = name
        self.email: str = email
        self.password: str = ""
        self.instructions: str = instructions
        