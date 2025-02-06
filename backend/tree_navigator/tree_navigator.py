import json
import os
from abc import ABC


class Node:
    def __init__(self, name: str, content, **attributes):
        self.name = name
        self.content = content
        self.__dict__.update(attributes)

    def set_attribute(self, key, value):
        self.__dict__[key] = value

    def get_attribute(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def get_attributes(self):
        return self.__dict__.keys() - ["name", "content"]


class TreeNavigator(ABC):
    def __init__(self, root_name: str):
        self.tree = Node(root_name, None)

    def get_node(self, node_path) -> Node | None:
        """
        Get the node object from the tree
        :param node_path: the path of the node
        :return:
        """
        path = node_path.split("/")
        node = self.tree
        for i in path:
            if not self.is_leaf(node):
                matching_children = [child for child in self.get_children(node) if child.name == i]
                if len(matching_children) == 0:
                    return None
                child = matching_children[0]
                node = child
            else:
                return None
        return node

    def get_children(self, node) -> list[Node]:
        return node.content if self.is_leaf(node) else []

    def open(self, node_path):
        """
        Open the node
        :param node_path: the path of the node
        :return:
        """
        return

    def close(self, node_path):
        """
        Close the node
        :param node_path:
        :return:
        """
        tree_node = self.get_node(node_path)
        tree_node.content = None
        return

    def print(self) -> str:
        """
        Get the representation of the tree in the following format:
            node / (attr1: val1) (attr2: val2)
                - child1 / (attr1: val1)
                - child2 / (attr1: val1)
                ...
        :return: str
        """

        def print_node(node, depth):
            node_name = node.name
            content = node.content
            attributes = node.get_attributes()

            header = f"\n{'\t' * depth}- {node_name}" + "".join(
                [f" ({attr}: {node.get_attribute(attr)})" for attr in attributes])
            if isinstance(content, list):
                for child in content:
                    header += print_node(child, depth + 1)
            elif content is not None:
                header += f"\n{'\t' * (depth + 1)}{content}"

            return header

        return print_node(self.tree, 0)

    def is_leaf(self, node) -> bool:
        """
        Check if the node is a leaf
        :param node:
        :return:
        """
        return node.content is not None and isinstance(node.content, list)

    def copy(self):
        return json.loads(json.dumps(self.__dict__))

    def load(self, json_obj):
        """
        Load the tree from a json object
        :return:
        """
        self.__dict__.update(json_obj)


class FolderNavigator(TreeNavigator):
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

    def open_folder(self, node):
        children = os.listdir(os.path.join(self.root_path, node))
        children = [
            Node(
                name=child,
                **({
                       "size": self.sizeof_fmt(os.path.getsize(os.path.join(self.root_path, node, child))),
                       "state": "unopened",
                   } if os.path.isfile(os.path.join(self.root_path, node, child)) else {}),
                **({
                       "children": [],
                       "expanded": False,
                   } if os.path.isdir(os.path.join(self.root_path, node, child)) else {})

            )
            for child in children]
        tree_node: Node = self.get_node(node)
        tree_node["children"] = children
        tree_node["expanded"] = True
        return children

    def is_leaf(self, node_path):
        return os.path.isfile(os.path.join(self.root_path, node_path))

    def open_file(self, node):
        file = open(os.path.join(self.root_path, node), "r").read()
        return file

    def open(self, node):
        if os.path.isdir(os.path.join(self.root_path, node)):
            return self.open_folder(node)
        else:
            file = open(os.path.join(self.root_path, node), "r").read()
            tree_node: Node = self.get_node(node)
            tree_node.content = file
            return file
