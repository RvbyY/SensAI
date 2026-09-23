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
    name: str
    description: str
    arguments: list[Any]

    def __init__(self, name: str, description: str, arguments: list[Any]):
        self.name = name
        self.description = description
        self.arguments = arguments

class ToolCalls:
    """
    Liste des ToolCallsFunctions
    L'API de Ollama veut englober les ToolCallsFunctions dans la liste de ToolCalls

    :param functions: liste des fonctions
    """
    functions: list[ToolCallsFunction]

    def __init__(self, functions: list[ToolCallsFunction]):
        self.functions = functions

class Message:
    """
    Chat history as an array of message objects (each with a role and content)
    """
    role: Role
    content: str
    images: list[str]
    tool_calls: list[ToolCalls]
    thinking: Optional[str]

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
        self.role = role
        self.content = content
        self.images = images if images is not None else []
        self.tool_calls = tool_calls if tool_calls is not None else []
        self.thinking = thinking

class MessageList(UserList[Message]):
    """Collection typée réservée aux objets Message."""

    def format_all(self, separator: str = "\n---\n") -> str:
        """Méthode uniquement disponible sur cette collection de messages."""
        return ""

class ToolsFunction:
    name: str
    parameters: list[Any]
    description: str

    def __init__(self, name: str, parameters: list[Any], description: str):
        self.name = name
        self.parameters = parameters
        self.description = description

class Tools:
    tool_type: ToolType
    tool_function: ToolsFunction

    def __init__(self, tool_type: ToolType, tool_function: ToolsFunction):
        self.tool_type = tool_type
        self.tool_function = tool_function

class ToolsList(UserList[Tools]):
    """Collection typée réservée aux objets Message."""

    def format_all(self, separator: str = "\n---\n") -> str:
        """Méthode uniquement disponible sur cette collection de messages."""
        return ""

class Options:
    seed: int
    temperature: float
    top_k: int
    top_p: float
    min_p: float
    stop: str | list[str]
    num_ctx: int
    num_predict: int

    def __init__(self, seed: int, temperature: float, top_k: int, top_p: float, min_p: float, stop: str | list[str], num_ctx: int, num_predict: int):
        self.seed = seed
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.min_p = min_p
        self.stop = stop
        self.num_ctx = num_ctx
        self.num_predict = num_predict

class Chat:
    model: str
    messages: MessageList
    tools: ToolsList
    request_format: Format
    options: Options
    stream: bool
    think: bool | Think
    keep_alive: str | int
    logprobs: bool
    top_logprobs: int

    def __init__(self, model: str, messages: MessageList, tools: ToolsList, request_format: Format, options: Options, stream: bool, think: bool | Think, keep_alive: str | int, logprobs: bool, top_logprobs: int):
        self.model = model
        self.messages = messages
        self.tools = tools
        self.request_format = request_format
        self.options = options
        self.stream = stream
        self.think = think
        self.keep_alive = keep_alive
        self.logprobs = logprobs
        self.top_logprobs = top_logprobs

class TopLogProb:
    token: str
    logprob: float
    bytes: list[int]

    def __init__(self, token: str, logprob: float, bytes_repr: list[int]):
        self.token = token
        self.logprob = logprob
        self.bytes = bytes_repr

class LogProb:
    token: str
    logprob: float
    bytes: list[int]
    top_logprobs: list[TopLogProb]

    def __init__(self, token: str, logprob: float, bytes_repr: list[int], top_logprobs: list[TopLogProb]):
        self.token = token
        self.logprob = logprob
        self.bytes = bytes_repr
        self.top_logprobs = top_logprobs

class ChatResponse:
    model: str
    created_at: str
    message: Message
    done: bool
    done_reason: str
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_eval_cached_count: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int
    logprobs: Optional[list[LogProb]]

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
        self.model = model
        self.created_at = created_at
        self.message = message
        self.done = done
        self.done_reason = done_reason
        self.total_duration = total_duration
        self.load_duration = load_duration
        self.prompt_eval_count = prompt_eval_count
        self.prompt_eval_cached_count = prompt_eval_cached_count
        self.prompt_eval_duration = prompt_eval_duration
        self.eval_count = eval_count
        self.eval_duration = eval_duration
        self.logprobs = logprobs
