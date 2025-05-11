from typing import List

from langchain_core.messages import AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from src.configs.config import OPENROUTER_API_KEY
from src.modules.schemas.schema import State


class DockerfileAgent:
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
            Your task is to reduce the Docker image size **by at least 50%** based on the Dockerfile in the `{app_folder}` directory.  
            Follow these instructions:  
                1. Edit parts that contribute to a large Docker image size.  
                2. **Avoid to add any files that were not present in the original Docker context.**  
                3. Remove all command explanations and inline comments.  
                4. Save the optimized Dockerfile using the `save_content` tool with the folder name as input.  
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
                        input_variables=["app_folder"],
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

    def node(self, state: State) -> Command:
        """Executes the Dockerfile generator agent.
        """
        prompt = self.prompt().invoke(
            {
                "app_folder": state["app_folder"],
                "dockerfile_content": state["dockerfile_content"]
            }
        )

        agent_executor = create_react_agent(self._llm, self._tools)

        response = agent_executor.invoke(prompt)

        return Command(
            update = {"messages": [AIMessage(content=response["messages"][-1].content)]},
        )
