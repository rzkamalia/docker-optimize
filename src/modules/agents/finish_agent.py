from src.modules.schemas.schema import State
from src.modules.tools.general import save_content


def finish_agent(state: State):

    save_content.invoke(
        {   
            "content": state["dockerfile_content"],
            "foldername": state["app_folder"]
        }
    )
    
    return {"messages": ["No need to optimize."]}