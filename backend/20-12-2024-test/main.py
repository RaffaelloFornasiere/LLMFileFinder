import json5 as json

from utils import *
from bash_commands import *

system_message = open("messages/system_message.md", "r").read()
user_message = open("messages/user_message.md", "r").read()

tree = FileNavigator("jpalioapp", "/Users/forna/Documents/me/palio/jpalioapp")

operation_history = []

model = "mistral-nemo-instruct-2407"
objective = "Find the game rest controller file/s"

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message.format(tree=tree.get_print(),
                                                    operation_history=operation_history,
                                                    objective=objective)},
]

response = get_response(messages, model, base_url)
response_text = parse_response_text(response)
action = tree.parse(response_text)
tree.run(action)
operation_history.append(json.dumps(action))
