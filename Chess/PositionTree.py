from Chess import ChessEngine
class Node():
    def __init__(self):
        self.children = {} # {moveID : Node}
        self.comment = "No comment yet"
class Tree():
    def __init__(self):
        self.root = Node()
    def search(self, node, movelog, i):
        if i == len(movelog):
            return node
        if movelog[i].moveID in node.children.keys():
            return self.search(node.children[movelog[i].moveID], movelog, i+1)
        return False
    def newNote(self, node, movelog, i, comment):
        if i == len(movelog):
            node.comment = comment
        if movelog[i].moveID in node.children.keys():
            self.newNote(node.children[movelog[i].moveID], movelog, i+1, comment)
        else:
            newNode = Node()
            node.children[movelog[i].moveID] = newNode
            self.newNote(node.children[movelog[i].moveID], movelog, i+1, comment)