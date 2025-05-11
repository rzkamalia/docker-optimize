from typing import List, Literal

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from langgraph.types import Command

from src.configs.config import OPENROUTER_API_KEY
from src.modules.schemas.schema import Router, State


class RouterAgent:
    def __init__(self, tools: List):
        self._llm = ChatOpenAI(
            model="openai/gpt-4o",
            base_url="https://openrouter.ai/api/v1",
            max_retries=3,
            api_key=OPENROUTER_API_KEY,
        )
        self._tools = tools
        
    def system_prompt(self):
        return """
            You are a Docker expert.
            Your task is to analyze the content of a Dockerfile to determine whether it is optimized for minimal image size.

            Use the following criteria to evaluate the Dockerfile:
                - Is the base image minimal (e.g., `slim`, `alpine`, or `distroless`)?
                - Are unnecessary tools, caches, or build dependencies removed?
                - Are multi-stage builds used effectively?
                - Are commands grouped efficiently to reduce layers?
                - Is `.dockerignore` likely being used to exclude large, unused files?
                - Are package managers cleaned up after installation?

            Decision logic:
                - If the Dockerfile adheres to all best practices and is likely to produce an image smaller than 1 GB, the next worker is `finish_agent`.
                - If any issues are found that could result in an image larger than 1 GB or violate best practices, the next worker is `dockerfile_agent`.

            Be strict in your evaluation. It's better to over-optimize than to ship a bloated image.
        """
    
    def human_prompt(self):
        return """
            Dockerfile content:
            {dockerfile_content}
        """
    
    def prompt(self) -> ChatPromptTemplate:
        """Prompt templating.
        """
        return ChatPromptTemplate.from_messages(
            messages=[
                SystemMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template=self.system_prompt(),
                        input_variables=[],
                    )
                ),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        template=self.human_prompt(),
                        input_variables=["dockerfile_content"],
                    )
                )
            ]
        )

    def node(self, state: State) -> Command[Literal["dockerfile_agent", "finish_agent"]]:
        """Executes the Dockerfile generator agent.
        """
        prompt = self.prompt().invoke(
            {
                "dockerfile_content": state["dockerfile_content"]
            }
        )

        response: Router = self._llm.with_structured_output(Router).invoke(prompt)

        return Command(
            goto = response["next"],
        )
