from heapq import heapify, heappush, heappop
class priority_queue(object):
	""" Node must implement __lt__ and __hash__ and also have a valid boolean member"""
	def __init__(self, heap=[]):
		heapify(heap)
		self.heap = heap
		self.map = dict({hash(task) : task for task in heap}) # priority : node pairs

	def insert(self, node):
		if hash(node) in self.map:
			self.delete(hash(node))
		self.map[hash(node)] = node
		heappush(self.heap, node)

	def delete(self, node):
		entry = self.map.pop(node)
		entry.valid = False # find some way to have nodes represent this
		return entry

	def pop(self):
		while self.heap:
			node = heappop(self.heap)
			if node.valid:
				del self.map[hash(node)]
				return node
		raise KeyError('pop from empty pq')

class test_node(object):
	def __init__(self, weight, source, dest):
		self.weight = weight
		self.source = source
		self.dest = dest
		self.valid = True

	def __hash__(self):
		return hash(''.join([str(self.weight), str(self.source), str(self.dest)]))


	def __lt__(self, other):
		return self.weight < other.weight

	def __str__(self):
		return '->'.join([self.source, self.dest]) + '{0}'.format(self.weight)


if __name__ == "__main__":
	n1 = test_node(10, 'a', 'b')
	n2 = test_node(2, 'b', 'c')	
	n3 = test_node(3, 'a', 'b')
	pq = priority_queue([n1, n2, n3])
	while pq.heap:
		print(str(pq.pop()))