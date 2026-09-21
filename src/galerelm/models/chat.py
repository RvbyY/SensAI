from typing import Literal, Optional, Any
from collections import UserList

#Still unused, maybe will when data will be stored in a real DB
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

Role = Literal["system", "user", "assistant", "tool"]
ToolType = Literal["function"]

class ToolCallsFunction:
    """
    :param name:
    :param description:
    :param arguments:
    """
    def __init__(self, name: str, description: str, arguments: list[Any]):
        self.name: str = name
        self.description: str = description
        self.arguments: list[Any] = arguments

class ToolCalls:
    """
    Liste des ToolCallsFunctions
    L'API de Ollama veut englober les ToolCallsFunctions dans la liste de ToolCalls

    :param functions: liste des fonctions
    """

    def __init__(self, functions: list[ToolCallsFunction]):
        self.functions: list[ToolCallsFunction] = functions


class Message:
    """
    Chat history as an array of message objects (each with a role and content)
    """
    def __init__(self, role: Role, content: str, images: list[str], tool_calls: list[ToolCalls]):
        """
        :param role:
        Author of the message.
        Available options: system, user, assistant, tool
        :param content:
        Message text content
        :param images:
        Optional list of inline images for multimodal models
        Base64-encoded image content
        :param tool_calls:
        Tool call requests produced by the model
        """
        self.role: Role = role
        self.content: str = content
        self.images: list[str] = images
        self.tool_calls: list[ToolCalls] = tool_calls

class ToolsFunction:
    def __init__(self, name: str, parameters: list[Any], description: str):
        self.name: str = name
        self.parameters: list[Any] = parameters
        self.description: str = description

class Tools:
    def __init__(self, tool_type: ToolType, tool_function: ToolsFunction):
        self.tool_type: ToolType = tool_type
        self.tool_function: ToolsFunction = tool_function
        

