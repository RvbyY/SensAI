from typing import Literal, Optional, Any
from collections import UserList

#Still unused, maybe will when data will be stored in a real DB
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

Role = Literal["system", "user", "assistant", "tool"]
ToolType = Literal["function"]
Format = Literal["json"]
Think = Literal["high", "medium", "low", "max"]

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
    def __init__(self, role: Role, content: str, images: list[str] = None, tool_calls: list[ToolCalls] = None, thinking: str = None):
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
        :param thinking:
        Optional thinking process for reasoning models
        """
        self.role: Role = role
        self.content: str = content
        self.images: list[str] = images if images is not None else []
        self.tool_calls: list[ToolCalls] = tool_calls if tool_calls is not None else []
        self.thinking: Optional[str] = thinking

class MessageList(UserList[Message]):
    """Collection typée réservée aux objets Message."""

    def format_all(self, separator: str = "\n---\n") -> str:
        """Méthode uniquement disponible sur cette collection de messages."""
        return ""

class ToolsFunction:
    def __init__(self, name: str, parameters: list[Any], description: str):
        self.name: str = name
        self.parameters: list[Any] = parameters
        self.description: str = description

class Tools:
    def __init__(self, tool_type: ToolType, tool_function: ToolsFunction):
        self.tool_type: ToolType = tool_type
        self.tool_function: ToolsFunction = tool_function

class ToolsList(UserList[Tools]):
    """Collection typée réservée aux objets Message."""

    def format_all(self, separator: str = "\n---\n") -> str:
        """Méthode uniquement disponible sur cette collection de messages."""
        return ""

class Options:
    def __init__(self, seed: int, temperature: float, top_k: int, top_p: float, min_p: float, stop: str | list[str], num_ctx: int, num_predict: int):
        self.seed: int = seed
        self.temperature: float = temperature
        self.top_k: int = top_k
        self.top_p: float = top_p
        self.min_p: float = min_p
        self.stop: str | list[str] = stop
        self.num_ctx: int = num_ctx
        self.num_predict: int = num_predict

class Chat:
    def __init__(self, model: str, messages: MessageList, tools: ToolsList, request_format: Format, options: Options, stream: bool, think: bool | Think, keep_alive: str | int, logprobs: bool, top_logprobs: int):
        self.model: str = model
        self.messages: MessageList = messages
        self.tools: ToolsList = tools
        self.request_format: Format = request_format
        self.options: Options = options
        self.stream: bool = stream
        self.think: bool | Think = think
        self.keep_alive: str = keep_alive
        self.logprobs: bool = logprobs
        self.top_logprobs: int = top_logprobs

class TopLogProb:
    def __init__(self, token: str, logprob: float, bytes_repr: list[int]):
        self.token: str = token
        self.logprob: float = logprob
        self.bytes: list[int] = bytes_repr

class LogProb:
    def __init__(self, token: str, logprob: float, bytes_repr: list[int], top_logprobs: list[TopLogProb]):
        self.token: str = token
        self.logprob: float = logprob
        self.bytes: list[int] = bytes_repr
        self.top_logprobs: list[TopLogProb] = top_logprobs

class ChatResponse:
    def __init__(
        self,
        model: str,
        created_at: str,
        message: Message,
        done: bool,
        done_reason: str,
        total_duration: int,
        load_duration: int,
        prompt_eval_count: int,
        prompt_eval_cached_count: int,
        prompt_eval_duration: int,
        eval_count: int,
        eval_duration: int,
        logprobs: Optional[list[LogProb]] = None
    ):
        self.model: str = model
        self.created_at: str = created_at
        self.message: Message = message
        self.done: bool = done
        self.done_reason: str = done_reason
        self.total_duration: int = total_duration
        self.load_duration: int = load_duration
        self.prompt_eval_count: int = prompt_eval_count
        self.prompt_eval_cached_count: int = prompt_eval_cached_count
        self.prompt_eval_duration: int = prompt_eval_duration
        self.eval_count: int = eval_count
        self.eval_duration: int = eval_duration
        self.logprobs: Optional[list[LogProb]] = logprobs
