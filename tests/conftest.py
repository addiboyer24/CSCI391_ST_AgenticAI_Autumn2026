"""Shared fixtures for the course-site test suite.

Run everything:      python -m pytest
Skip browser tests:  python -m pytest -m "not browser"
"""
import functools
import http.server
import os
import socket
import subprocess
import sys
import threading
from html.parser import HTMLParser

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR = os.path.join(ROOT, "curriculum")
sys.path.insert(0, CUR)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf8") as f:
        return f.read()


class Page(HTMLParser):
    """Collects what the tests check: ids, links, images, headings, scripts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.imgs, self.tags, self.scripts = [], [], [], [], []
        self._in_script = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if "id" in a:
            self.ids.append(a["id"])
        for k in ("href", "src"):
            if a.get(k):
                self.links.append((tag, k, a[k]))
        if tag == "img":
            self.imgs.append(a)
        if tag == "script" and "src" not in a:
            self._in_script = True
            self.scripts.append("")

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_script = False

    def handle_data(self, data):
        if self._in_script:
            self.scripts[-1] += data


def parse(text):
    p = Page()
    p.feed(text)
    return p


@pytest.fixture(scope="session")
def tracked():
    """Files committed to git: what GitHub Pages will actually serve."""
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return set(out.splitlines())


@pytest.fixture(scope="session")
def index_html():
    return read("index.html")


@pytest.fixture(scope="session")
def guide_html():
    return read("instructor-guide.html")


@pytest.fixture(scope="session")
def site():
    import build_site
    return build_site


@pytest.fixture(scope="session")
def server():
    """Serve the repository over HTTP, the way GitHub Pages does."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(Quiet, directory=ROOT))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()
