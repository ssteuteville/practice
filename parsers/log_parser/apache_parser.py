from log_parser.core import *
import argparse
from collections import defaultdict
import operator
from memory_profiler import profile


class DateEntry(Entry):
    date = r'([0-9]{2})\/[a-zA-Z]{3}\/[0-9]{4}:([0-9]{2}):[0-9]{2}:[0-9]{2}'
    _fields = {
        'date': [date, 0, RegexDateSearch]
    }


class ResourceEntry(Entry):
    date = r'([0-9]{2})\/[a-zA-Z]{3}\/[0-9]{4}:([0-9]{2}):[0-9]{2}:[0-9]{2}'
    resource = r'(?i)(GET|HEAD|POST|PUT|OPTIONS|DELETE|PATCH)\s+(\S+)(\s)+((HTTP|HTTPS)\/\d\.\d+)?'
    _fields = {
        'resource': [resource, 2, RegexSearch],
        'date': [date, 0, RegexDateSearch]
    }


class ErrorEntry(Entry):
    date = r'([0-9]{2})\/[a-zA-Z]{3}\/[0-9]{4}:([0-9]{2}):[0-9]{2}:[0-9]{2}'
    resource = r'(?i)(GET|HEAD|POST|PUT|OPTIONS|DELETE|PATCH)\s+(\S+)(\s)+((HTTP|HTTPS)\/\d\.\d+)?'
    code = r'[1-5][0-9]{2}'
    _fields = {
        'resource': [resource, 2, RegexSearch],
        'date': [date, 0, RegexDateSearch],
        'code': [code, 0, RegexSearch]
    }


class RequesterEntry(Entry):
    date = r'([0-9]{2})\/[a-zA-Z]{3}\/[0-9]{4}:([0-9]{2}):[0-9]{2}:[0-9]{2}'
    ip_or_host = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
    ip_or_host += r'|(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]+|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])'
    _fields = {
        'requester': [ip_or_host, 0, RegexSearch],
        'date': [date, 0, RegexDateSearch]
    }


class ApacheParser(FileParser):
    lower = 0
    upper = 0
    limit = 0
    counts = defaultdict(int)

    def __init__(self, lower, upper, filename, limit=100):
        self.lower = lower
        self.upper = upper
        self.filename = filename
        self.limit = limit

    def _cmp(self, entry):
        day = int(entry.date.day)
        if self.lower > day:
            return -1
        elif day < self.upper:
            return 1
        return 0

    def _results(self):
        for key, value in sorted(self.counts.items(), key=operator.itemgetter(1), reverse=True)[0:self.limit]:
            print('\t'.join([str(value), key]))


class DateParser(ApacheParser):
    entry_class = DateEntry

    def _handle(self, entry):
        self.counts[str(entry.date.date()) + " " + str(entry.date.hour) + ":00"] += 1


class ResourceParser(ApacheParser):
    entry_class = ResourceEntry

    def _handle(self, entry):
        self.counts[entry.resource] += 1


class RequesterParser(ApacheParser):
    entry_class = RequesterEntry

    def _handle(self, entry):
        self.counts[entry.requester] += 1


class ErrorParser(ResourceParser):
    entry_class = ErrorEntry

    def _cmp(self, entry):
        day = int(entry.date.day)
        if self.lower > day or int(entry.code) < 400 or int(entry.code) > 599:
            return -1
        elif day < self.upper:
            return 1
        return 0

# @profile
def runner(args):
    parsers = {
        'resources': ResourceParser,
        'requesters': RequesterParser,
        'errors': ErrorParser,
        'hourly': DateParser
    }

    start = end = 0
    if '-' in args.day:
        start, end = (int(v) for v in args.day.split('-'))
    else:
        start = end = int(args.day)
    end += 1

    parser = parsers[args.type]

    if args.number:
        parser(start, end, args.file_path, int(args.number)).run()
    else:
        parser(start, end, args.file_path).run()


if __name__ == '__main__':
    help_messages = {'--type': ['The type argument is required. The types of searches are',
                                'resources\n\t\tDisplays resources and the count of times they occurred',
                                'requesters\n\t\tDisplays hosts that made request and a count of requests',
                                'errors\n\t\tSimilar to resources but only when there was an error.',
                                'hourly\n\t\tCounts number of requests and sorts them by hour'],
                      '--day': ['The --day argument is required and defines the day or day range to parse. The format is --day 12 | --day 9-20'],
                      'options': ['The only option available is --number. Options are optional.',
                      '--number #',
                      '\tThis option causes the script to display only the top # results',
                      '\tThe format is --number 10',
                      '\n\n',
                      'Examples:',
                      '\tlog_parse.py resources 12-15 access_log',
                      '\tlog_parse.py --number 100 hourly 7 access_log']}

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('type', help='\n'.join(help_messages['--type']))
    parser.add_argument('day', help='\n'.join(help_messages['--day']))
    parser.add_argument('file_path', help='the path to the file to be parsed.')
    parser.add_argument('--number', help='\n'.join(help_messages['options']))
    args = parser.parse_args()

    runner(args)