from inspect import Parameter, Signature
from log_parser.descriptors import *


def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)


class EntryMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        setattr(clsobj, '__signature__', make_signature(clsobj._params))
        for key, value in clsobj._fields.items():
            setattr(clsobj, key, value[-1](*value[:len(value)]))
        return clsobj
        # raise AttributeError('No fields were defined')


class Entry(metaclass=EntryMeta):
    _fields = {}
    _params = ['query']

    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)
        for name, val in self._fields.items():
            setattr(self, name, args[0])



class LogParser(object):
    entry_class = Entry

    def _gen(self):
        """First stage of pipeline collects data from source and yields it"""
        raise NotImplementedError("Must override _gen")

    def _parser(self, iterable):
        """Second stage of pipeline converts raw data to object"""
        for it in iterable:
            try:
                entry = self.entry_class(it)
                yield entry
            except TypeError as e:
                print(str(e))

    def _filter(self, iterable):
        """Third stage of pipeline decides which entries to yield, skip, and when to stop."""
        for it in iterable:
            if self._cmp(it) == 1:
                yield it
            elif self._cmp(it) == 0:
                break

    def _handle(self, entry):
        """Processes each entry as it leaves pipeline"""
        raise NotImplementedError("Must override _handle")

    def _cmp(self, entry):
        """ Comparison function used by _filter"""
        return 1

    def _results(self):
        """Handles collective results of parser."""
        raise NotImplementedError("Must override _results.")

    def run(self):
        gen = self._gen()
        parser = self._parser(gen)
        _filter = self._filter(parser)
        for entry in _filter:
            self._handle(entry)
        self._results()


class FileParser(LogParser):
    filename = ""

    def _gen(self):
        with open(self.filename) as f:
            yield from f