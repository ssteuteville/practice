#!/usr/bin/python

class Node:
	def __init__(self, data):
		self.left = None
		self.right = None
		self.data = data
		self.parent = None

class Tree:
	def __init__(self, root):
		self.root = root

	def _insert(self, r, v):
		if v < r.data:
			if r.left is None:
				r.left = Node(v)
				r.left.parent=r
			else:
				self._insert(r.left, v)
		else:
			if r.right is None:
				r.right = Node(v)
				r.right.parent=r
			else:
				self._insert(r.right, v)

	def insert(self,v):
		if self.root is None:
			self.root = Node(v)
		else:
			self._insert(self.root,v)

	def remove(self,v):
		if self.root is None:
			return
		else:
			self._remove(self.root, v)

	def _remove(self, node, v):
		if node is None:
			return
		elif node.data > v:
			self._remove(node.left, v)
		elif node.data < v:
			self._remove(node.right, v)
		else:
			if node.left is None and node.right is None:
				if node.parent.left == node:#if node is left child
					node.parent.left = None
				else:#if node is right child
					node.parent.right = None
			elif node.left is None:
				if node.parent.left == node:
					node.parent.left = node.right
				else:
					node.parent.right = node.right
			elif node.right is None:
				if node.parent.left == node:
					node.parent.left = node.left
				else:
					node.parent.right = node.left
			else:
				node.data = self._min_value(node.right).data
				self._remove(node.right, node.data)



	def _min_value(self, node):
		if node is None:
			return None
		elif node.left is None:
			return node
		else:
			return self._min_value(node.left)			



	def print_tree(self):
		if self.root is None:
			return
		else:
			self._print_tree(self.root)

	def _print_tree(self, node):
		if node is None:
			return
		else:
			self._print_tree(node.left)
			print str(node.data)
			self._print_tree(node.right)

	def print_tree_reverse(self):
		if self.root is None:
			return
		else:
			self._print_tree_reverse(self.root)

	def _print_tree_reverse(self, node):
		if node is None:
			return
		else:
			self._print_tree_reverse(node.right)
			print str(node.data)
			self._print_tree_reverse(node.left)

	def find(self, v):
		if self.root is None:
			return None
		else:
			self._find(self.root,v)

	def _find(self,node, v):
		if node is None:
			print "node is none"
			return None
		elif node.data < v:
			print str(node.data) + "<" + str(v)
			return self._find(node.right, v)
		elif node.data > v:
			print str(node.data) + ">" + str(v)
			return self._find(node.left, v)
		else:
			print "node found"
			return node.data





if __name__ == "__main__":
	root = Node(5)
	tree = Tree(root)
	tree.insert(3)
	tree.insert(7)
	tree.insert(10)
	tree.insert(6)
	tree.insert(1)
	tree.insert(4)
	print "in order"
	tree.print_tree()
	print "reverse"
	tree.print_tree_reverse()
	print "find test"
	print tree.find(4)

