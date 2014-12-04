def merge_sort(l):
	if len(l) < 2:
		return l
	return merge(merge_sort(l[:len(l)//2]), merge_sort(l[len(l)//2:]))

def merge(l1, l2):
	l3 = []
	while l1 and l2:
		if l1[0] > l2[0]:
			l3.append(l2[0])
			l2.pop(0)
		else:
			l3.append(l1[0])
			l1.pop(0)
	while l1:
		l3.append(l1[0])
		l1.pop(0)
	while l2:
		l3.append(l2[0])
		l2.pop(0)
	return l3

def inserstion_sort(l):
	for i in range(len(l)):
		x = l[i]
		j = i
		while j > 0 and l[j - 1] > x:
			l[j] = l[j-1]
			j -=1
		l[j] = x
	return l


if __name__ == "__main__":
	l = [43,56,12,31,93, 45, 12, 32, 13, 123, 0, 4124]
	assert(sorted(l) == merge_sort(l))
	assert(sorted(l) == inserstion_sort(l))
