import argparse

from src.modules.tools.general import read_file
from src.graph import graph


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app_folder_name', type=str, required=True, help="Name of the application's folder.")
    return parser.parse_args()

def main():
    args = parse_args()

    output = graph.invoke(
        {
            "app_folder": args.app_folder_name,
            "dockerfile_content": read_file(args.app_folder_name)
        }
    )

    print(output["messages"][-1].content)

if __name__ == "__main__":
    main()
