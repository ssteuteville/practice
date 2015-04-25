from dateutil import parser
import re


class Descriptor:
    """
        Base Descriptor Class
    """
    def __init__(self, *args, name=None, **kwargs):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Can't delete")


class RegexSearch(Descriptor):
    """
        RegexSearch is a descriptor that will do a regex search on the string that it gets set to.
        If the string contains the pattern being searched for the member will be set to the proper value.
        Otherwise it throws a type error.
    """
    def __init__(self, pattern, group, *args, **kwargs ):
        self.pattern = re.compile(pattern)
        self.group = group
        self.value = None
        super().__init__(*args, name='value', **kwargs)

    def __set__(self, instance, value):
        result = self.pattern.search(value)
        if result:
            super().__set__(self, result.group(self.group))
        else:
            raise TypeError("This string did not match the pattern:\n" + value + '\npattern:' + self.pattern.pattern + '\n')

    def __get__(self, instance, owner):
        return self.value


class RegexDateSearch(Descriptor):
    """
        RegexDateSearch is similar to RegexSearch but it converts the result to a datetime.
        throws a type error.
    """
    def __init__(self, pattern, group, *args, **kwargs):
        self.pattern = re.compile(pattern)
        self.group = group
        self.value = None
        super().__init__(*args, name='value', **kwargs)

    def __set__(self, instance, value):
        result = self.pattern.search(value)
        if result:
            super().__set__(self,  parser.parse(result.group(self.group), fuzzy=True))
        else:
            super().__set__(self, "")

    def __get__(self, instance, owner):
        return self.value