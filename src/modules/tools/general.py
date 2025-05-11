from langchain_core.tools import tool


def read_file(foldername: str) -> str:
    """Read a file.

    Args:
        foldername (str): A folder name.
    Returns:
        str: A content.
    """
    with open(f"{foldername}/Dockerfile", "r", encoding="utf-8") as file:
        return file.read()


@tool
def save_content(content: str, foldername: str):
    """Save content.

    Args:
        content (str): A content.
        foldername (str): A folder name.
    """
    with open(f"{foldername}/Dockerfile", "w", encoding="utf-8") as file:
        file.write(content)