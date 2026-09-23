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

    def format(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "instructions": self.instructions
        }

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        prof = cls(
            name=data.get("name", ""),
            email=data.get("email", ""),
            instructions=data.get("instructions", "")
        )
        if "id" in data:
            prof.id = data["id"]
        if "password" in data:
            prof.password = data["password"]
        return prof
