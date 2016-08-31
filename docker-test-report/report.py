#!/usr/bin/env python
"""
Create a report from the jenkins console log for a Docker engine test run.

Example:

    curl https://jenkins.dockerproject.org/job/Docker-PRs/31507/logText/progressiveHtml

"""
from __future__ import print_function

import decimal
import sys
import textwrap
from datetime import datetime, timedelta
from collections import namedtuple
from operator import itemgetter
from pyquery import PyQuery as pq


NUM_TESTS = 10

def err(msg):
    print(msg, file=sys.stderr)


Entry = namedtuple("Entry", "timestamp text")

def get_lines(stream):
    def get_line(line):
        entry = pq(line)
        timestamp = entry('span.timestamp b').text()
        text = entry.contents()[1]
        if hasattr(text, 'text'):
            text = text.text
        timestamp = datetime.strptime(timestamp, "%H:%M:%S")
        return Entry(timestamp, text)
    return map(get_line, stream)


def format_report(lines):
    start, end = lines[0], lines[-1]
    first, last = find_first_test_line(lines), find_last_test_line(lines)
    times = test_times(lines[first:last])

    print(textwrap.dedent("""
        Elapsed: {elapsed}
        Elapsed integration suite: {elapsed_suite}
        Sum test times: {sum_times}
        Time to first integration test: {time_to_first}
        Time after last integration test: {time_after_last}
        Test count: {count}

        Slowest tests:
    """.format(
        elapsed=end.timestamp - start.timestamp,
        elapsed_suite=lines[last].timestamp - lines[first].timestamp,
        time_to_first=lines[first].timestamp - start.timestamp,
        time_after_last=end.timestamp - lines[last].timestamp,
        count=len(times),
        sum_times=timedelta(seconds=int(sum(e[0] for e in times))),
    )) + format_slowest(times))


def format_slowest(times, n=NUM_TESTS):
    return "\n".join(
        " " * 3 + e[1].rstrip() for e in
        sorted(times, key=itemgetter(0), reverse=True)[:n],
    )


def test_times(lines):
    def get_time(line):
        if line.text.startswith("SKIP:"):
            return None
        parts = line.text.split(None, 4)
        if len(parts) != 4:
            err("Not a test line: %s" % line.text.rstrip())
            return None
        return decimal.Decimal(parts[-1][:-1]), line.text
    return filter(None, map(get_time, lines))


def find_first_test_line(lines):
    for index, line in enumerate(lines):
        if line.text.startswith("INFO: Testing against"):
            return index+1
    return 0


def find_last_test_line(lines):
    for index, line in enumerate(lines):
        if "Making bundle: .integration-daemon-stop" in line.text:
            return index-1
    return 0


def main():
    lines = get_lines(sys.stdin)
    if not lines:
        err("No input")
        return

    format_report(lines)


if __name__ == "__main__":
    main()
