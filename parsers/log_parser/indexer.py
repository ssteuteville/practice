from log_parser.rbtree import RbTree
import re


class Index(object):
    def __init__(self, index, byte_offset):
        self.index = index
        self.byte_offset = byte_offset

    def __lt__(self, other):
        return self.index < other.index

    def __le__(self, other):
        return self.index <= other.index

    def __eq__(self, other):
        return self.index == other.index

    def __ne__(self, other):
        return self.index != other.index

    def __gt__(self, other):
        return self.index > other.index

    def __ge__(self, other):
        return self.index >= other.index

    def __str__(self):
        return str(self.index) + ',' + str(self.byte_offset)

    def __int__(self):
        return int(self.byte_offset)


class Indexer(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = RbTree()

    def add(self, index, offset):
        self.data.insert(Index(int(index), offset))

    def find(self, index):
        return self.data.find(Index(index, 0)).index


    def __str__(self):
        return ';'.join([index for index in self.data.in_order_traversal(str, None)])

    def __len__(self):
        return self.data.count

    def save(self):
        with open(self.filename + '.index', 'a') as f:
            for index in self.data.in_order_traversal(str, None):
                f.write(index + ';')

    def load(self):
        with open(self.filename + '.index') as f:
            for pair in f.read().split(';'):
                if pair == '':
                    break
                index, offset = pair.split(',')
                self.data.insert(Index(int(index), offset))

    def load_new(self):
        with open(self.filename) as f:
            byte_count = 1
            i = 1
            self.add(0, 0)
            while True:
                _byte = f.read(1)
                byte_count += 1
                if not _byte:
                    break
                if _byte == '\n':
                    self.add(i, byte_count)
                    byte_count += 1
                    i += 1

    def create_index(self):
        self.load_new()
        self.save()

    def reset(self):
        del self.data
        self.data = RbTree()

    def find_start(self, target, visit):
        with open(self.filename) as f:
            i = int(len(self)/2)
            div = 4
            prev = i
            prev_val = None
            prev_count = 0
            while True:
                f.seek(self.find(i))
                value = visit(f.readline().rstrip())
                if prev_val == value:
                    prev_count += 1
                else:
                    prev_count = 0
                if value < target:
                    i += int(len(self)/div)
                elif value > target:
                    i -= int(len(self)/div)
                else:
                    return i
                if i == prev:
                    return None
                elif prev_count > 20 and abs(value - target) < 2:
                    return i
                div *= 2
                prev = i
            while i >= 0:
                f.seek(self.find(i))
                value = visit(f.readline().rstrip())
                if value != target:
                    break
                i -= 1

# i = Indexer('access_log_Jul95')
i = Indexer('test')
i.load()
print(len(i))

def visit(line):
    pattern = re.compile(r'(\d\d)\/Jul')
    value = pattern.search(line)
    if value:
        return int(value.group(1))
    raise TypeError("String didn't match regex")

print(i.find_start(14, visit))