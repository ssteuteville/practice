import re
from datetime import datetime
import argparse
from memory_profiler import profile

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
start = args.day
end = start
printed = 0

if '-' in args.day:
    start, end = args.day.split('-')


ip_or_host = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
ip_or_host += r'|(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])'
time_stamp = r'([0-9]{2})\/[a-zA-Z]{3}\/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}'
request = r'(?i)(GET|HEAD|POST|PUT|OPTIONS|DELETE|PATCH)\s+(\S+)\s+(HTTP|HTTPS)\/\d\.\d+'
code = r'[1-5][0-9]{2}'




def find_day(data, day):
    i = int(len(data)/2)
    dividend = 4
    prev = i
    while datetime.strptime(re.search(time_stamp, data[i]).group(0), '%d/%b/%Y:%H:%M:%S').day != day:
        if datetime.strptime(re.search(time_stamp, data[i]).group(0), '%d/%b/%Y:%H:%M:%S').day < day:
            i += int(len(data)/dividend)
        else:
            i -= int(len(data)/dividend)
        if i == prev:
            return None
        dividend *= 2
        prev = i
    while i >= 0 and datetime.strptime(re.search(time_stamp, data[i]).group(0), '%d/%b/%Y:%H:%M:%S').day == day:
        i -= 1;

    return i + 1


@profile
def doIt(f):
    global printed
    start_index = find_day(f.readlines(), int(start))
    f.seek(0)
    if args.type == 'hourly':
        current_count = 0
        prev_date = None
        for line in f.readlines()[start_index:]:
            date = datetime.strptime(re.search(time_stamp, line).group(0), '%d/%b/%Y:%H:%M:%S')
            if prev_date is None or date.hour == prev_date.hour:
                current_count += 1
            else:
                print(str(current_count) + '\t' + str(prev_date.date()) + " " + str(prev_date.hour) + ":00")
                printed += 1
                current_count = 1
                if date.day > int(end) or printed >= int(args.number):
                    break
            prev_date = date

with open(args.file_path) as f:
    doIt(f)