#!/usr/bin/env python

import argparse
import collections
import sys

import requests


def download_json(url):
    r = requests.get(url)

    if r.status_code != 200:
        print(r.json())
        sys.exit(1)

    return r.json()


def find_milestone(milestone):
    url = 'https://api.github.com/repos/{0}/{1}/milestones'.format(args.owner, args.repo)
    js = download_json(url)
    for m in js:
        if m['title'] == args.milestone:
            return m['number']

    print('milestone is not found: {}'.format(milestone))
    sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument('--owner', '-o', required=True, help='Owner name')
parser.add_argument('--repo', '-r', required=True, help='Repository name')
parser.add_argument('--milestone', '-m', required=True, help='Milestone title')
args = parser.parse_args()

issues = collections.defaultdict(list)
page = 1

milestone_number = find_milestone(args.milestone)

while True:
    url = 'https://api.github.com/repos/{0}/{1}/issues?milestone={2}&state=close&page={3}'.format(args.owner, args.repo, milestone_number, page)
    js = download_json(url)
    if len(js) == 0:
        break
    for issue in js:
        for label in issue['labels']:
            issues[label['name']].append(int(issue['number']))

    page += 1

for label, numbers in issues.items():
    print(label + ' ' + ' '.join('#{}'.format(n) for n in sorted(numbers)))
    
