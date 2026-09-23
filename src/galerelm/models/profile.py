import uuid
from typing import Literal

class Profile:
    id: str
    name: str
    email: str
    password: str
    instructions: str

    def __init__(self, name: str, email: str, instructions: str):
        self.id = ""
        self.name = name
        self.email = email
        self.password = ""
        self.instructions = instructions
