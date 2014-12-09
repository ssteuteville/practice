import threading
from timeit import default_timer as timer
max_size = 10
condition = threading.Condition()
q = []
def producer():
	l = [i for i in range(100)]
	global q
	for i in l:
		condition.acquire()
		if len(q) == max_size:
			print("queue is full")
			condition.wait()
			print("producer got signal")
		q.append(i)
		print("produced item")
		condition.notify()
		condition.release()

def consumer():
	global q
	for i in range(100):
		condition.acquire()
		if not q:
			print("q is empty")
			condition.wait()
			print("consumer got signal")
		print(q.pop(0))
		print("consumed item")
		condition.notify()
		condition.release()

def find_sum(l):
	return sum(l)

def populate_list(l, start, end):
	for i in range(start, end):
		# print(threading.currentThread().name)
		l.append(i)

if __name__ == "__main__":
	t1 = threading.Thread(target=producer)
	t2 = threading.Thread(target=consumer)
	t1.start()
	t2.start()
	t2.join()
	t1.join()
	start = 0
	l = []
	end = 99999999
	t1 = threading.Thread(name="1", target=populate_list, args=(l, start, end//3))
	t2 = threading.Thread(name="2", target=populate_list, args=(l, end//3, 2*end//3))
	t3 = threading.Thread(name="3", target=populate_list, args=(l, 2*end//3, end))
	start_time = timer()
	t1.start()
	t2.start()
	t3.start()
	t1.join()
	t2.join()
	t3.join()
	print(str(timer() - start_time))
	l2 = []
	start_time = timer()
	populate_list(l, start, end)
	print(str(timer() - start_time))




