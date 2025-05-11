from langgraph.graph import END, START, StateGraph

from src.modules.agents.dockerfile_agent import DockerfileAgent
from src.modules.agents.router_agent import RouterAgent
from src.modules.agents.finish_agent import finish_agent
from src.modules.schemas.schema import State
from src.modules.tools.general import save_content


dockerfile_agent = DockerfileAgent(tools=[save_content])
router_agent = RouterAgent(tools=[])

graph = StateGraph(state_schema=State)

graph.add_node("dockerfile_agent", dockerfile_agent.node)
graph.add_node("finish_agent", finish_agent)
graph.add_node("router_agent", router_agent.node)

graph.add_edge(START, "router_agent")
graph.add_edge("dockerfile_agent", END)
graph.add_edge("finish_agent", END)

graph = graph.compile()
