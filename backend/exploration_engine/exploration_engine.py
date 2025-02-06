import json
from abc import ABC
import requests
from backend.tree_navigator.tree_navigator import TreeNavigator


class LLMClient(ABC):
    def completion(self, text, **kwargs):
        raise NotImplementedError

    def chat_completion(self, text, **kwargs):
        raise NotImplementedError

class OpenAILLMClient(LLMClient):
    def __init__(self, base_url, api_key, model_name):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name

    def completion(self, text, **kwargs):
        pass

    def chat_completion(self, messages, **kwargs):
        url = self.base_url + "/v1/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "temperature": 0.7,
            "model": self.model_name,
            "messages": messages,
            "max_tokens": -1,
            **kwargs,
            "stream": False,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()


class ActionManager:
    def __init__(self, client: LLMClient, navigator: TreeNavigator, actions=None):
        self.client = client
        self.action_history = []
        self.tree_navigator = navigator
        self.actions = actions

    def parse(self, response):
        """
        Parse the action from the response
        :param response:
        :return:
        """
        start_parse = response.index("```json")
        end_parse = response.index("```", start_parse + 1)
        if start_parse == -1 or end_parse == -1:
            return None
        json_str = response[start_parse + 7:end_parse]
        try:
            action = json.loads(json_str)
        except json.JSONDecodeError:
            return None

        errors = []
        warnings = []
        if "action" not in action or action["action"] not in self.actions:
            errors.append("Invalid action")

        if "node" not in action or self.tree_navigator.get_node(action["node"]) is None:
            errors.append("Invalid node")

        if "short_comment" not in action:
            warnings.append("Short comment not provided")

        return action, errors, warnings

    def run(self, action):
        """
        Run the action
        :param action:
        :return:
        """
        action_name = action["action"]
        node = action["node"]

        res = getattr(self, action_name)(node, action)

        self.action_history.append(action)
        return res


