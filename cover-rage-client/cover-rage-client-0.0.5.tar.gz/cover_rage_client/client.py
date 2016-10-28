#!/usr/bin/env python

import sys

import asyncio
from collections import OrderedDict
from hashlib import sha1
import hmac
import json
import os
import subprocess

from aiohttp import ClientSession

from .cover import PythonCoverage


async def send_request(
    req_server_url: str,
    req_token: str,
    req_overall_coverage: float,
    req_uncovered_lines: dict,
    req_git_commit: str,
    loop=None
) -> None:
    data = OrderedDict([
        ('git_commit', req_git_commit),
        ('overall_coverage', req_overall_coverage),
        ('uncovered_lines', json.dumps(req_uncovered_lines)),
    ])
    mac = hmac.new(req_token.encode('utf-8'), msg=json.dumps(data).encode('utf-8'), digestmod=sha1)
    headers = {'X-CoverRage-Signature': 'sha1={}'.format(mac.hexdigest())}
    async with ClientSession(loop=loop) as session:
        async with session.get(req_server_url, headers=headers, data=data) as response:
            response_text = await response.text()
            assert response.status == 200, response_text


def main(server_url: str, token: str, git_root: str, coverage_file: str) -> None:
    assert server_url
    assert token
    assert git_root
    assert coverage_file
    assert os.path.exists(git_root)
    assert os.path.isdir(git_root)
    assert os.path.exists(coverage_file)
    assert os.path.isfile(coverage_file)

    coverage = PythonCoverage(git_root, coverage_file)
    assert coverage

    overall_coverage = coverage.line_rate
    uncovered_lines = coverage.compare_coverage_with_diff()
    git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=git_root)
    assert isinstance(git_commit, bytes)
    git_commit = git_commit.decode("utf-8").rstrip()
    assert git_commit

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(
        send_request(
            server_url,
            token,
            overall_coverage,
            uncovered_lines,
            git_commit
        )
    )


def __main__():  # pragma: no cover

    if len(sys.argv) != 5:
        print('Usage: {} <cover_rage_server_url> <cover_rage_app_token> </path/to/git/root> </path/to/coverage.xml>'.format(sys.argv[0]))
        exit(1)

    main(*sys.argv[1:5])
