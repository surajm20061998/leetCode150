# Interesting question at -> https://www.interviewskool.com/practice/dsa-problems/design-in-memory-file-system?utm_source=chatgpt.com
# Need to understand question better
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_file = False
        self.content = ""

class FileSystem:
    def __init__(self):
        self.root = TrieNode()

    def _navigate(self, path):
        node = self.root
        parts = [p for p in path.split("/") if p]
        for part in parts:
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]
        return node

    def ls(self, path):
        node = self._navigate(path)
        if node.is_file:
            return [path.split("/")[-1]]
        return sorted(node.children.keys())

    def mkdir(self, path):
        self._navigate(path)

    def addContentToFile(self, filePath, content):
        node = self._navigate(filePath)
        node.is_file = True
        node.content += content

    def readContentFromFile(self, filePath):
        return self._navigate(filePath).content