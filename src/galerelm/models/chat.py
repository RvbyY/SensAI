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
    arguments: dict

    def __init__(self, name: str, description: str, arguments: dict):
        self.name = name
        self.description = description
        self.arguments = arguments

    def format(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "arguments": self.arguments
        }

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            arguments=data.get("arguments", {})
        )


class ToolCalls:
    """
    Liste des ToolCallsFunctions
    L'API de Ollama veut englober les ToolCallsFunctions dans la liste de ToolCalls

    :param functions: liste des fonctions
    """
    functions: list[ToolCallsFunction]

    def __init__(self, functions: list[ToolCallsFunction]):
        self.functions = functions

    def format(self) -> dict:
        # Ollama API requires a "function" key
        if isinstance(self.functions, list) and len(self.functions) > 0:
            return {"function": self.functions[0].format()}
        return {"function": getattr(self.functions, "format", lambda: {})()}

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        func_data = data.get("function")
        if func_data and isinstance(func_data, dict):
            functions = [ToolCallsFunction.from_format(func_data)]
        else:
            functions = []
        return cls(functions=functions)


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
        self.role = role
        self.content = content
        self.images = images if images is not None else []
        self.tool_calls = tool_calls if tool_calls is not None else []
        self.thinking = thinking

    def format(self) -> dict:
        res = {
            "role": self.role,
            "content": self.content,
        }
        if self.images:
            res["images"] = self.images
        if self.tool_calls:
            res["tool_calls"] = [tc.format() for tc in self.tool_calls]
        if self.thinking is not None:
            res["thinking"] = self.thinking
        return res

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        tool_calls_data = data.get("tool_calls", [])
        return cls(
            role=data.get("role", "user"),
            content=data.get("content", ""),
            images=data.get("images", []),
            tool_calls=[ToolCalls.from_format(tc) for tc in tool_calls_data] if tool_calls_data else [],
            thinking=data.get("thinking")
        )


class MessageList(UserList[Message]):
    """Collection typée réservée aux objets Message."""

    def format_all(self, separator: str = "\n---\n") -> str:
        return separator.join([m.content for m in self.data])

    def format(self) -> list[dict]:
        return [m.format() for m in self.data]

    @classmethod
    def from_format(cls, data: list[dict]):
        if not data:
            return cls([])
        return cls([Message.from_format(m) for m in data])


class ToolsFunction:
    name: str
    parameters: dict
    description: str

    def __init__(self, name: str, parameters: dict, description: str):
        self.name = name
        self.parameters = parameters
        self.description = description

    def format(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            parameters=data.get("parameters", {})
        )


class Tools:
    tool_type: ToolType
    tool_function: ToolsFunction

    def __init__(self, tool_type: ToolType, tool_function: ToolsFunction):
        self.tool_type = tool_type
        self.tool_function = tool_function

    def format(self) -> dict:
        return {
            "type": self.tool_type,
            "function": self.tool_function.format() if self.tool_function else None
        }

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        return cls(
            tool_type=data.get("type", "function"),
            tool_function=ToolsFunction.from_format(data.get("function", {}))
        )


class ToolsList(UserList[Tools]):
    """Collection typée réservée aux objets Message."""

    def format_all(self, separator: str = "\n---\n") -> str:
        return ""

    def format(self) -> list[dict]:
        return [t.format() for t in self.data]

    @classmethod
    def from_format(cls, data: list[dict]):
        if not data:
            return cls([])
        return cls([Tools.from_format(t) for t in data])


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

    def format(self) -> dict:
        return {
            "seed": self.seed,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "min_p": self.min_p,
            "stop": self.stop,
            "num_ctx": self.num_ctx,
            "num_predict": self.num_predict
        }

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        return cls(
            seed=data.get("seed", 0),
            temperature=data.get("temperature", 0.8),
            top_k=data.get("top_k", 40),
            top_p=data.get("top_p", 0.9),
            min_p=data.get("min_p", 0.0),
            stop=data.get("stop", ""),
            num_ctx=data.get("num_ctx", 2048),
            num_predict=data.get("num_predict", 128)
        )


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

    def format(self) -> dict:
        res = {
            "model": self.model,
            "messages": self.messages.format() if self.messages else [],
            "stream": self.stream,
        }
        if self.tools:
            res["tools"] = self.tools.format()
        if self.request_format:
            res["format"] = self.request_format
        if self.options:
            res["options"] = self.options.format()
        if self.think is not None:
            res["think"] = self.think
        if self.keep_alive is not None:
            res["keep_alive"] = self.keep_alive
        if self.logprobs is not None:
            res["logprobs"] = self.logprobs
        if self.top_logprobs is not None:
            res["top_logprobs"] = self.top_logprobs
        return res

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        return cls(
            model=data.get("model", ""),
            messages=MessageList.from_format(data.get("messages", [])),
            tools=ToolsList.from_format(data.get("tools", [])),
            request_format=data.get("format", "json"),
            options=Options.from_format(data.get("options")) if data.get("options") else None,
            stream=data.get("stream", True),
            think=data.get("think"),
            keep_alive=data.get("keep_alive"),
            logprobs=data.get("logprobs", False),
            top_logprobs=data.get("top_logprobs")
        )


class TopLogProb:
    token: str
    logprob: float
    bytes: list[int]

    def __init__(self, token: str, logprob: float, bytes_repr: list[int]):
        self.token = token
        self.logprob = logprob
        self.bytes = bytes_repr

    def format(self) -> dict:
        return {
            "token": self.token,
            "logprob": self.logprob,
            "bytes": self.bytes
        }

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        return cls(
            token=data.get("token", ""),
            logprob=data.get("logprob", 0.0),
            bytes_repr=data.get("bytes", [])
        )


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

    def format(self) -> dict:
        return {
            "token": self.token,
            "logprob": self.logprob,
            "bytes": self.bytes,
            "top_logprobs": [t.format() for t in self.top_logprobs] if self.top_logprobs else []
        }

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        return cls(
            token=data.get("token", ""),
            logprob=data.get("logprob", 0.0),
            bytes_repr=data.get("bytes", []),
            top_logprobs=[TopLogProb.from_format(t) for t in data.get("top_logprobs", [])]
        )


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

    def format(self) -> dict:
        res = {
            "model": self.model,
            "created_at": self.created_at,
            "message": self.message.format() if self.message else None,
            "done": self.done,
            "done_reason": self.done_reason,
            "total_duration": self.total_duration,
            "load_duration": self.load_duration,
            "prompt_eval_count": self.prompt_eval_count,
            "prompt_eval_cached_count": self.prompt_eval_cached_count,
            "prompt_eval_duration": self.prompt_eval_duration,
            "eval_count": self.eval_count,
            "eval_duration": self.eval_duration,
        }
        if self.logprobs is not None:
            res["logprobs"] = [lp.format() for lp in self.logprobs]
        return res

    @classmethod
    def from_format(cls, data: dict):
        if not data:
            return None
        logprobs_data = data.get("logprobs")
        return cls(
            model=data.get("model", ""),
            created_at=data.get("created_at", ""),
            message=Message.from_format(data.get("message", {})),
            done=data.get("done", False),
            done_reason=data.get("done_reason", ""),
            total_duration=data.get("total_duration", 0),
            load_duration=data.get("load_duration", 0),
            prompt_eval_count=data.get("prompt_eval_count", 0),
            prompt_eval_cached_count=data.get("prompt_eval_cached_count", 0),
            prompt_eval_duration=data.get("prompt_eval_duration", 0),
            eval_count=data.get("eval_count", 0),
            eval_duration=data.get("eval_duration", 0),
            logprobs=[LogProb.from_format(lp) for lp in logprobs_data] if logprobs_data else None
        )
