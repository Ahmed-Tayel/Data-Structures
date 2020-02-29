from collections import deque

# Define a node
class Node(object):
    def __init__(self, value= None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = None
    def get_value(self):
        return self.value
    def set_value(self,value):
        self.value = value
    def set_left_child(self,node):
        self.left = node
    def set_right_child(self,node):
        self.right = node
    def set_height(self,height):
        self.height = height
    def set_parent(self,parent):
        self.parent = parent
    def get_left_child(self):
        return self.left
    def get_right_child(self):
        return self.right
    def get_height(self):
        return self.height
    def get_parent(self):
        return self.parent
    def has_left_child(self):
        return self.left != None
    def has_right_child(self):
        return self.right != None
    def __repr__(self):
        return f"Node({self.get_value()})"
    def __str__(self):
        return f"Node({self.get_value()})"

#Define Tree
class Tree(object):
    def __init__(self, value):
        self.root = Node(value)
    def get_root(self):
        return self.root
    def set_root(self,root):
        self.root = root
    
    def compare(self,node,new_node):
        if new_node.get_value() == node.get_value():
            return 0
        elif new_node.get_value() < node.get_value():
            return -1
        else:
            return 1

    def insert_with_loop(self,val):
        new_node = Node(val)
        current_node = self.get_root()
        if not current_node:
            self.root = new_node
            new_node.set_height(0)
            return
        while(True):
            result = self.compare(current_node,new_node)
            if result == -1:
                if current_node.has_left_child():
                    current_node = current_node.get_left_child()
                else:
                    current_node.set_left_child(new_node)
                    new_node.set_parent(current_node)
                    self.Node_Update(new_node)
                    break
            if result == 1:
                if current_node.has_right_child():
                    current_node = current_node.get_right_child()
                else:
                    current_node.set_right_child(new_node)
                    new_node.set_parent(current_node)
                    self.Node_Update(new_node)
                    break
    
    def Node_Update(self, node):
        heightPtr = node
        node.set_height(0)
        while True:
            nodeParent = heightPtr.get_parent()
            balanced = self.Is_Balanced(nodeParent)
            if balanced:
                heightPtr = nodeParent
                self.Update_Height(heightPtr)
            else:
                leftChildHeight, rightChildHeight = self.get_children_height(nodeParent)
                if leftChildHeight > rightChildHeight:
                    if nodeParent == self.get_root():
                        self.set_root(nodeParent.get_left_child())
                    heightPtr = nodeParent.get_left_child()
                    self.Left_Rotate(nodeParent)
                    nodeParent = nodeParent.get_parent()
                else:
                    if nodeParent == self.get_root():
                        self.set_root(nodeParent.get_right_child())
                    heightPtr = nodeParent.get_right_child()
                    self.Right_Rotate(nodeParent)
                    nodeParent = nodeParent.get_parent()
            if nodeParent == self.get_root():
                break
    
    def Left_Rotate(self, node):
        nodeIsRight = False
        nodeIsLeft = False
        if node.get_parent():
            nodeIsRight = self.Is_Right_Child(node)
            nodeIsLeft = self.Is_Left_Child(node)
        leftChildPtr = node.get_left_child()
        leftChildPtr.set_parent(node.get_parent())
        node.set_left_child(leftChildPtr.get_right_child())
        node.set_parent(leftChildPtr)
        leftChildPtr.set_right_child(node)
        node.set_height(leftChildPtr.get_height() - 1)
        if nodeIsRight:
            leftChildPtr.get_parent().set_right_child(leftChildPtr)
        elif nodeIsLeft:
            leftChildPtr.get_parent().set_left_child(leftChildPtr)
    
    def Right_Rotate(self, node):
        nodeIsRight = False
        nodeIsLeft = False
        if node.get_parent():
            nodeIsRight = self.Is_Right_Child(node)
            nodeIsLeft = self.Is_Left_Child(node)
        rightChildPtr = node.get_right_child()
        rightChildPtr.set_parent(node.get_parent())
        node.set_right_child(rightChildPtr.get_left_child())
        node.set_parent(rightChildPtr)
        rightChildPtr.set_left_child(node)
        node.set_height(rightChildPtr.get_height() - 1)
        if nodeIsRight:
            rightChildPtr.get_parent().set_right_child(rightChildPtr)
        elif nodeIsLeft:
            rightChildPtr.get_parent().set_left_child(rightChildPtr)


    def Update_Height(self, node):
        leftChildHeight, rightChildHeight = self.get_children_height(node)
        node.set_height(max(rightChildHeight,leftChildHeight) + 1)

    def Is_Balanced(self, node):
        leftChildHeight, rightChildHeight = self.get_children_height(node)
        result = abs(leftChildHeight - rightChildHeight)
        return result <= 1

    def get_children_height(self,node):
        leftChildHeight  = -1 
        rightChildHeight = -1
        if node.has_left_child():
            leftChildHeight = node.get_left_child().get_height()
        if node.has_right_child():
            rightChildHeight = node.get_right_child().get_height()
        return leftChildHeight, rightChildHeight

    def Is_Right_Child(self, childNode):
        if childNode.get_parent() == None:
            return False
        else:
            return childNode.get_value() == childNode.get_parent().get_right_child().get_value()

    def Is_Left_Child(self, childNode):
        if childNode.get_parent() == None:
            return False
        else:
            return childNode.get_value() == childNode.get_parent().get_left_child().get_value()

    def search(self,value):
        search_node = Node(value)
        current_node = self.get_root()
        if not current_node:
            return False
        while(True):
            result = self.compare(current_node,search_node)
            if result == 0:
                return current_node
            elif result == -1:
                if current_node.has_left_child():
                    current_node = current_node.get_left_child()
                else:
                    return False
            elif result == 1:
                if current_node.has_right_child():
                    current_node = current_node.get_right_child()
                else:
                    return False

    def delete(self,value):
        oldNode = self.search(value)
        if oldNode == False:
            return False
        elif self.Is_Leaf(oldNode):
            if self.Is_Left_Child(oldNode):
                oldNode.get_parent().set_left_child(None)
            if self.Is_Right_Child(oldNode):
                oldNode.get_parent().set_right_child(None)
            del oldNode
        elif self.has_only_one_child(oldNode):
            if self.has_only_left_child(oldNode):
                newNode = oldNode.get_left_child()
            else:
                newNode = oldNode.get_right_child()
            newNode.set_parent(oldNode.get_parent())
            if self.Is_Left_Child(oldNode):
                oldNode.get_parent().set_left_child(newNode)
            elif self.Is_Right_Child(oldNode):
                oldNode.get_parent().set_right_child(newNode)
            del oldNode
        else:
            nodeRightChild = oldNode.get_right_child()
            if self.Is_Leaf(nodeRightChild) or self.has_only_right_child(nodeRightChild):
                newNode = nodeRightChild
                newNode.set_parent(oldNode.get_parent())
                newNode.set_left_child(oldNode.get_left_child())
                if self.Is_Left_Child(oldNode):
                    oldNode.get_parent().set_left_child(newNode)
                elif self.Is_Right_Child(oldNode):
                    oldNode.get_parent().set_right_child(newNode)
                del oldNode
            else:
                newNode = nodeRightChild
                while newNode.has_left_child():
                    newNode = newNode.get_left_child()
                newNode.get_parent().set_left_child(None)
                newNode.set_parent(oldNode.get_parent())
                newNode.set_left_child(oldNode.get_left_child())
                newNode.set_right_child(oldNode.get_right_child())
                if self.Is_Left_Child(oldNode):
                    oldNode.get_parent().set_left_child(newNode)
                elif self.Is_Left_Child(oldNode):
                    oldNode.get_parent().set_right_child(newNode)
                del oldNode


    def Is_Leaf(self,node):
        return not (node.has_left_child() or node.has_right_child())

    def has_only_left_child(self,node):
        return node.has_left_child() and not node.has_right_child()

    def has_only_right_child(self,node):
        return node.has_right_child() and not node.has_left_child()

    def has_only_one_child(self,node):
        return (self.has_only_left_child(node) or self.has_only_right_child(node))

#TREE TRAVERSALS PRE IN AND POST
def pre_order(tree):
    visit_order = []
    root = tree.get_root()

    def Traverse(node):
        if node:
            visit_order.append(node.get_value())
            Traverse(node.get_left_child())
            Traverse(node.get_right_child())
    Traverse(root)
    return visit_order

def In_order(tree):
    visit_order = []
    root = tree.get_root()

    def Traverse(node):
        if node:
            Traverse(node.get_left_child())
            visit_order.append(node.get_value())
            Traverse(node.get_right_child())
    Traverse(root)
    return visit_order

def post_order(tree):
    visit_order = []
    root = tree.get_root()

    def Traverse(node):
        if node:
            Traverse(node.get_left_child())
            Traverse(node.get_right_child())
            visit_order.append(node.get_value())
    Traverse(root)
    return visit_order

def BFS(tree):
    visit_order = []
    root = tree.get_root()
    q = deque()
    q.appendleft(root)
    while len(q):
        node = q.pop()
        visit_order.append(node.get_value())
        if node.get_left_child():
            q.appendleft(node.get_left_child())
        if node.get_right_child():
            q.appendleft(node.get_right_child())
    return visit_order