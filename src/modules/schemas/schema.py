from langgraph.graph.message import add_messages

from typing import Annotated, List, Literal
from typing_extensions import TypedDict


class State(TypedDict):
    app_folder: str
    dockerfile_content: str
    messages: Annotated[List, add_messages]


class Router(TypedDict):
    next: Literal["finish_agent", "dockerfile_agent"]