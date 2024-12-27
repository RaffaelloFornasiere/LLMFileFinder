import json5 as json
import os
from abc import ABC, abstractmethod


class NodeNavigator(ABC):
    def __init__(self, root_name: str):
        self.tree = {
            "name": root_name,
            "expanded": False,
        }

    @abstractmethod
    def expand(self, node):
        """
        Expand the node
        :param node:
        :return:
        """
        raise NotImplementedError

    def get_node(self, nodeName):
        """
        Get the node object from the tree
        :param node:
        :return:
        """

        path = nodeName.split("/")
        node = {
            "children": [self.tree]
        }
        for i in path:
            if "children" in node:
                child = [child for child in node["children"] if child["name"] == i]
                if len(child) == 0:
                    return None
                child = child[0]
                node = child
            else:
                return None

        return node

    def open(self, node):
        """
        S
        :param node:
        :return:
        """
        tree_node = self.get_node(node)
        tree_node["state"] = "opened"
        return

    def close(self, node):
        """
        Close the node
        :param node:
        :return:
        """
        tree_node = self.get_node(node)
        tree_node["state"] = "closed"
        if "children" in tree_node:
            tree_node["children"] = []
        return

    def mark_as_useful(self, node):
        """
        Mark the node as useful
        :param node:
        :return:
        """
        if isinstance(node, str):
            node = [node]
        for n in node:
            tree_node: dict = self.get_node(n)
            tree_node["useful"] = True
        return

    def mark_as_useless(self, node):
        """
        Mark the node as useless
        :param node:
        :return:
        """
        if isinstance(node, str):
            node = [node]
        for n in node:
            tree_node: dict = self.get_node(n)
            tree_node["useful"] = False
        return

    def get_json(self):
        """
        Get the JSON representation of the tree
        :return:
        """

        return json.dumps(self.tree, indent=2)

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
        if "action" not in action or action["action"] not in ["expand", "open", "close", "mark_as_useful",
                                                              "mark_as_useless"]:
            errors.append("Invalid action")

        if "node" not in action or self.get_node(action["node"]) is None:
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

        if action_name == "expand":
            self.expand(node)
        elif action_name == "open":
            self.open(node)
        elif action_name == "close":
            self.close(node)
        elif action_name == "mark_as_useful":
            self.mark_as_useful(node)
        elif action_name == "mark_as_useless":
            self.mark_as_useless(node)
        return


class FileNavigator(NodeNavigator):
    def __init__(self, root_name: str, root_path: str):
        super().__init__(root_name)
        self.root_path = root_path

    @staticmethod
    def sizeof_fmt(num, suffix="B"):
        for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    def expand(self, node):
        children = os.listdir(os.path.join(self.root_path, node))
        children = [
            {
                "name": child,
                **({
                       "size": self.sizeof_fmt(os.path.getsize(os.path.join(self.root_path, node, child))),
                       "state": "unopened",
                   } if os.path.isfile(os.path.join(self.root_path, node, child)) else {}),
                **({
                       "children": [],
                       "expanded": False,
                   } if os.path.isdir(os.path.join(self.root_path, node, child)) else {})

            }
            for child in children]

        self.get_node(node)["children"] = children

        return children

    def open(self, node):
        super().open(node)
        file = open(os.path.join(self.root_path, node), "r").read()
        return file
