"""
This script tests the ability of the chatbot to scan folders and files to find what the user is looking for.
It iteratively opens folders and files to find the desired information.

The chatbot uses a set of tools to open files and folders.
The tools are:
 - ls: list the contents of a folder
 - cd: change the current folder
 - cat: open a file and read its contents
 - sed -n 'start,endp': read the lines from start to end in a file

The chatbot is provided with a tree structure of folders and files.
As he navigates through the folders, he can open files and read their contents.
Once the chatbot reads the contents of a file, he can mark it as useful or not useful.
If it is useful, it is kept open in the tree structure, otherwise it is closed and marked as not useful.
The chatbot has the ability also to keep open only some chunks of the file, and close the rest.

The chatbot can also mark an entire folder as not useful.
"""
import json5 as json
import os

from utils import *
from bash_commands import *

system_message = """
You are an AI assistant that can help me navigate through folders and files.
I will provide you with a tree structure of folders and files.

You have the following commands at your disposal:
    - ls [{{folder}}]: list the contents of a folder
    - cd {{folder}}: change the current folder
    - cat {{folder}}: open a file and read its contents
    - filesize {{file}}: get the size of a file
    - sed -n '{{start}},{{end}}p': read the lines from start to end in a file
    - mark useful {{file}}|{{folder}}: mark a file or folder as useful
    - mark not useful {{file}}|{{folder}}: mark a file or folder as not useful
    
You have to navigate through the tree structure to find the information I am looking for.
You will be called iteratively to open folders and files. 
At each iteration you have only to execute a command or mark a file or folder as useful or not useful.
When you open a file, you will be able to read its content in the tree structure on the next iteration.

If you mark a file as not useful its content will be hidden in the tree structure.
If you mark a folder as not useful it will be shown as closed in the tree structure.

You will also see other system messages that will keep a synthesis of the tree structure and the files you have opened.

Remember to prune the tree structure to keep only the useful information.

Only one command or action per iteration. Only one line is allowed.

TASK
Find the endpoint to add a game
"""

tree = {
    "jpalioapp": {
        "type": "folder",
        "size": "1.4G",
        "visited": "true",
        ".": {
            "README.md": {
                "type": "file",
                "size": " 12K"
            },
            "angular.json": {
                "type": "file",
                "size": "4.0K"
            },
            "checkstyle.xml": {
                "type": "file",
                "size": "4.0K"
            },
            "eslint.config.mjs": {
                "type": "file",
                "size": "8.0K"
            },
            "jest.conf.js": {
                "type": "file",
                "size": "4.0K"
            },
            "jpalioapp.jdl": {
                "type": "file",
                "size": "4.0K"
            },
            "mvnw": {
                "type": "file",
                "size": " 12K"
            },
            "mvnw.cmd": {
                "type": "file",
                "size": "8.0K"
            },
            "ngsw-config.json": {
                "type": "file",
                "size": "4.0K"
            },
            "node_modules": {
                "type": "folder",
                "size": "570M"
            },
            "npmw": {
                "type": "file",
                "size": "4.0K"
            },
            "npmw.cmd": {
                "type": "file",
                "size": "4.0K"
            },
            "openapi.json": {
                "type": "file",
                "size": "100K"
            },
            "package-lock.json": {
                "type": "file",
                "size": "880K"
            },
            "package.json": {
                "type": "file",
                "size": "8.0K"
            },
            "pom.xml": {
                "type": "file",
                "size": " 60K"
            },
            "sonar-project.properties": {
                "type": "file",
                "size": "4.0K"
            },
            "src": {
                "type": "folder",
                "size": "4.0M",
                ".": {
                    "main": {
                        "size": "3.5M"
                    },
                    "test": {
                        "size": "508K"
                    }
                }
            },
            "target": {
                "type": "folder",
                "size": "821M"
            },
            "tsconfig.app.json": {
                "type": "file",
                "size": "4.0K"
            },
            "tsconfig.json": {
                "type": "file",
                "size": "4.0K"
            },
            "tsconfig.spec.json": {
                "size": "4.0K"
            },
            "venv": {
                "size": "7.9M"
            },
            "webpack": {
                "size": " 20K"
            }
        }
    }
}

operation_list = [
    "cd jpalioapp",
    "ls"
    "cd src",
]

pwd = "./jpalioapp/src"

recap_message = """
TREE STRUCTURE
{tree}

OPERATION HISTORY
{operation_list}

PWD
{pwd}
"""

init_messages = [
    {"role": "system", "content": system_message},
]

messages = json.load(open("messages.json", "r"))
messages = init_messages + messages

model = "mistral-nemo-instruct-2407"

operation_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "operation",
        "schema": {
            "type": "object",
            "properties": {
                "next-operation": {
                    "type": "string"
                }

            },
            "required": ["next-operation"]
        },
    }
}


def send_explain_message(messages):
    messages.append({
        "role": "user",
        "content": "Briefly explain what is the purpose of the operation you might want next (max 20 words)"
    })
    response = get_response(messages, model, base_url)
    response_text = parse_response_text(response)
    messages.append({"role": "assistant", "content": response_text})
    f = open("messages.json", "w")
    json.dump(messages[1:], f, indent=2)
    f.flush()
    f.close()


def send_next_operation_message(messages):
    messages = list(
        filter(lambda x: not (x["role"] == "user" and x["content"].strip().startswith("TREE STRUCTURE")), messages))
    messages.append({
        "role": "user",
        "content": recap_message.format(tree=tree, operation_list=operation_list, pwd=pwd)
    })
    messages.append({
        "role": "user",
        "content": "Write the command or the operation to execute what you have explained"
    })

    response = get_response(messages, model, base_url, operation_schema)
    response_text = parse_response_text(response)
    messages.append({"role": "assistant", "content": response_text})
    f = open("messages.json", "w")
    json.dump(messages[1:], f, indent=2)
    f.flush()
    f.close()


def get_answer(messages):
    response = get_response(messages, model, base_url, operation_schema)
    response_text = parse_response_text(response)
    messages.append({"role": "assistant", "content": response_text})
    f = open("messages.json", "w")
    json.dump(messages[1:], f, indent=2)
    f.flush()
    f.close()
    return response_text


command = input("> ")
if command == "explain":
    send_explain_message(messages)
elif command == "nextop":
    send_next_operation_message(messages)
else:
    get_answer(messages)
