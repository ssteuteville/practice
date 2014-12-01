import bst
from timeit import default_timer as timer
class Node:
	def __init__(self, data, color):
		self.left = None
		self.right = None
		self.data = data
		self.parent = None
		self.color = color
B = 0
R = 1
NIL = Node(None, B)

class Tree:
	def __init__(self):
		self.root = NIL

	def left_rotate(self, node):
		temp = node.right
		node.right = temp.left
		if temp.left is not NIL:
			temp.left.parent = node
		temp.parent = node.parent
		if node.parent is NIL:
			self.root = temp
		elif node is node.parent.left:
			node.parent.left = temp
		else:
			node.parent.right = temp
		temp.left = node
		node.parent = temp


	def right_rotate(self, node):
		temp = node.left
		node.left = temp.right
		if temp.right is not NIL:
			temp.right.parent = node
		temp.parent = node.parent
		if node.parent is NIL:
			self.root = temp
		elif node is node.parent.right:
			node.parent.right = temp
		else:
			node.parent.left = temp
		temp.right = node
		node.parent = temp

	def insert(self, v):
		y = NIL
		x = self.root
		while x != NIL:
			y = x
			if v < x.data:
				x = x.left
			else:
				x = x.right
		new = Node(v, R)
		new.parent = y
		if y == NIL:
			self.root = new
		elif new.data < y.data:
			y.left = new
		else:
			y.right = new
		new.left = NIL
		new.right = NIL
		self.insert_fix(new)

	def insert_fix(self, node):
		while node.parent.color is R:
			if node.parent is node.parent.parent.left:
				y = node.parent.parent.right
				if y.color is R:
					node.parent.color = B
					y.color = B
					node.parent.parent.color = R
					node = node.parent.parent
				else:
					if node is node.parent.right:
						node = node.parent
						self.left_rotate(node)
					node.parent.color = B
					node.parent.parent.color = R
					self.right_rotate(node.parent.parent)
			else:
				y = node.parent.parent.left
				if y.color is R:
					node.parent.color = B
					y.color = B
					node.parent.parent.color = R
					node = node.parent.parent
				else:
					if node is node.parent.left:
						node = node.parent
						self.right_rotate(node)
					node.parent.color = B
					node.parent.parent.color = R
					self.left_rotate(node.parent.parent)

		self.root.color = B

	def find(self, v):
		if self.root is NIL:
			return None
		else:
			return self._find(self.root,v)


	def _find(self,node, v):
		if node is NIL:
			return None
		elif node.data < v:
			return self._find(node.right, v)
		elif node.data > v:
			return self._find(node.left, v)
		else:
			return node.data


	def in_order_traversal(self, visit, kwargs):
		if self.root is not NIL:
			self._in_order_traversal(self.root, visit, kwargs);


	def _in_order_traversal(self, node, visit, kwargs):
		if node is not NIL:
			self._in_order_traversal(node.left, visit, kwargs)
			if kwargs:
				visit(node.data, **kwargs)
			else:
				visit(node.data)
			self._in_order_traversal(node.right, visit, kwargs)


	def height_if_balanced(self, node):
		if node is NIL:
			return 0
		lht = self.height_if_balanced(node.left)
		if lht == -1:
			return -1
		rht = self.height_if_balanced(node.right)
		if rht == -1:
			return -1
		if abs(lht - rht) > 1:
			return -1
		return max(lht, rht) + 1

def tree_sort(l):
	t = Tree()
	for val in l:
		t.insert(val)
	l = []
	tree.in_order_traversal(bst.to_list, {'l' : l})
	return l


if __name__ == "__main__":
	tree = Tree()
	tree.insert(5)
	tree.insert(3)
	tree.insert(2)
	tree.insert(1)
	l = []
	t = [1, 2, 3, 5]
	tree.in_order_traversal(bst.to_list, {'l' : l})
	assert(l == t)
	assert(tree.find(5) == 5)
	assert(tree.find(0) is None)
	l = [5,4,3,2,1]
	assert(tree_sort(l) == t)
	start = timer()
	l = tree_sort(l)
	end = timer()
	print("mine {0}".format(end - start))
	l = [5,4,3,2,1]
	start = timer()
	l = sorted(l)
	end = timer()
	print("built in {0}".format(end - start))
