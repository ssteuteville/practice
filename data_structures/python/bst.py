#!/usr/bin/python

class Node:
	def __init__(self, data):
		self.left = None
		self.right = None
		self.data = data
		self.parent = None


class Tree:
	def __init__(self, root=None):
		self.root = root


	def clear(self):
		self.root = None


	def _insert(self, r, v):
		if v < r.data:
			if r.left is None:
				r.left = Node(v)
				r.left.parent = r
			else:
				self._insert(r.left, v)
		else:
			if r.right is None:
				r.right = Node(v)
				r.right.parent = r
			else:
				self._insert(r.right, v)


	def insert(self,v):
		if self.root is None:
			self.root = Node(v)
		else:
			self._insert(self.root,v)


	def remove(self,v):
		if self.root is not None:
			self._remove(self.root, v)


	def _remove(self, node, v):
		if node is not None:
			if node.data > v:
				self._remove(node.left, v)
			elif node.data < v:
				self._remove(node.right, v)
			else:
				if node.left is None and node.right is None:
					if node.parent.left is node:#if node is left child
						node.parent.left = None
					else:#if node is right child
						node.parent.right = None
				elif node.left is None:
					if node.parent.left is node:
						node.parent.left = node.right
					else:
						node.parent.right = node.right
				elif node.right is None:
					if node.parent.left is node:
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


	def find(self, v):
		if self.root is None:
			return None
		else:
			return self._find(self.root,v)


	def _find(self,node, v):
		if node is None:
			return None
		elif node.data < v:
			return self._find(node.right, v)
		elif node.data > v:
			return self._find(node.left, v)
		else:
			return node.data


	def in_order_traversal(self, visit, kwargs):
		if self.root is not None:
			self._in_order_traversal(self.root, visit, kwargs);


	def _in_order_traversal(self, node, visit, kwargs):
		if node is not None:
			self._in_order_traversal(node.left, visit, kwargs)
			if kwargs:
				visit(node.data, **kwargs)
			else:
				visit(node.data)
			self._in_order_traversal(node.right, visit, kwargs)


	def reverse_order_traversal(self, visit, kwargs):
		if self.root is not None:
			self._reverse_order_traversal(self.root, visit, kwargs);


	def _reverse_order_traversal(self, node, visit, kwargs):
		if node is not None:
			self._reverse_order_traversal(node.right, visit, kwargs)
			if kwargs:
				visit(node.data, **kwargs)
			else:
				visit(node.data)
			self._reverse_order_traversal(node.left, visit, kwargs)


	def breadth_first_traversal(self, visit, kwargs):
		if self.root is not None:
			self._breadth_first_traversal(self.root, visit, kwargs)


	def _breadth_first_traversal(self, node, visit, kwargs):
		if node is not None:
			queue = [node]
			while queue:
				cur = queue.pop(0)
				if kwargs:
					visit(cur.data, **kwargs)
				else:
					visit(cur.data)
				if cur.left is not None:
					queue.append(cur.left)
				if cur.right is not None:
					queue.append(cur.right)


	def height_if_balanced(self, node):
		if node is None:
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


def to_list_plus_x(v, x=0, l=[]):
	l.append(v + x)


def to_list(v, l=[]):
	l.append(v)


def rebalance_tree(tree):
	if tree.height_if_balanced(tree.root) == -1:
		temp = []
		tree.in_order_traversal(to_list, {'l' : temp} )
		tree.root = None
		insert_sorted_list(tree, temp)


def insert_sorted_list(tree, l):
	size = len(l)
	mid = size//2
	if size != 0:
		tree.insert(l[mid])
		insert_sorted_list(tree, l[0:mid])
		insert_sorted_list(tree, l[mid+1:])


def insert_list(tree, l, b=False):
	if b:
		l.sort()
		insert_sorted_list(tree, l)
	else:
		for val in l:
			tree.insert(val)


if __name__ == "__main__":
	tree = Tree()
	l = [1,2,3,4,9,8,10,12,11]
	insert_list(tree, l, True)
	assert(tree.height_if_balanced(tree.root) == 4)
	tree.clear()
	insert_list(tree, l)
	assert(tree.height_if_balanced(tree.root) == -1)
	rebalance_tree(tree)
	assert(tree.height_if_balanced(tree.root) == 4)
	tree.clear()
	tree.insert(5)
	tree.insert(6)
	tree.insert(7)
	tree.insert(8)
	tree.insert(1)
	tree.insert(2)
	tree.insert(3)
	
	j = []
	t = [6, 7, 8, 10, 11, 12, 13]
	tree.in_order_traversal(to_list_plus_x, { 'x' : 5, 'l' : j })
	assert(j == t)
	assert(tree.find(4) == None)
	assert(tree.find(8) == 8)
	l = []
	t = [1, 2, 3, 5, 6, 7, 8]
	l2 = []
	t2 = t[::-1]
	l3 = []
	t3 = [5, 1, 6, 2, 7, 3, 8]
	tree.in_order_traversal(to_list, { 'l' : l })
	tree.reverse_order_traversal(to_list, {'l' : l2})
	tree.breadth_first_traversal(to_list, {'l' : l3})
	assert(l == t)
	assert(l2 == t2)
	assert(l3 == t3)
	assert(tree.height_if_balanced(tree.root) == -1)
