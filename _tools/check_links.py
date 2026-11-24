"""Check links in a built Jekyll site, without third-party dependencies."""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

ORIGIN = "https://jiayuelliesu.github.io"
LINK_ATTRIBUTES = {
    "a": ("href",), "area": ("href",), "link": ("href",),
    "img": ("src",), "script": ("src",), "iframe": ("src",),
    "audio": ("src",), "video": ("src", "poster"), "source": ("src",),
    "track": ("src",), "embed": ("src",), "object": ("data",),
}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.anchors = set()
        self.links = []
        self.base = None
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.anchors.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.anchors.add(attrs["name"])
        if tag == "base" and attrs.get("href") and self.base is None:
            self.base = attrs["href"]
        for key in LINK_ATTRIBUTES.get(tag, ()):
            if attrs.get(key):
                self.links.append((attrs[key], self.getpos()[0]))


def page_url(path):
    name = path.as_posix()
    if name == "index.html":
        return "/"
    if name.endswith("/index.html"):
        return "/" + name[:-len("index.html")]
    return "/" + name


def find_target(root, url_path):
    """Resolve a URL path to a built file, honoring directory index pages."""
    target = (root / unquote(url_path).lstrip("/")).resolve()
    if not target.is_relative_to(root):
        return None
    if target.is_dir():
        target = target / "index.html"
    if target.is_file():
        return target
    # GitHub Pages also serves extensionless URLs for HTML files.
    if not target.suffix and target.with_suffix(".html").is_file():
        return target.with_suffix(".html")
    return None


def check_site(root, origin=ORIGIN):
    root = root.resolve()
    if not (root / "index.html").is_file():
        raise ValueError(f"No built index.html in {root}; build the site first.")
    pages = {path: Page(path) for path in sorted(root.rglob("*.html"))}
    external = defaultdict(set)
    errors, warnings = [], []
    origin_host = urlsplit(origin).hostname
    for path, page in pages.items():
        relative = path.relative_to(root)
        page_base = urljoin(origin, page_url(relative))
        if page.base:
            page_base = urljoin(page_base, page.base)
        for raw, line in page.links:
            raw = raw.strip()
            if not raw or raw == "#":
                continue
            location = f"{relative}:{line}"
            try:
                url = urlsplit(urljoin(page_base, raw))
            except ValueError:
                errors.append(f"{location}: invalid URL {raw!r}")
                continue
            if url.scheme not in ("http", "https"):
                continue
            if url.hostname != origin_host:
                external[url._replace(fragment="").geturl()].add(location)
                continue
            target = find_target(root, url.path or "/")
            if target is None:
                errors.append(f"{location}: missing file for {raw!r}")
                continue
            fragment = unquote(url.fragment).split(":~:text=", 1)[0]
            if not fragment or fragment.lower() == "top" or target.suffix.lower() != ".html":
                continue
            if target not in pages:
                pages_for_target = Page(target).anchors
            else:
                pages_for_target = pages[target].anchors
            if fragment not in pages_for_target:
                message = f"{location}: missing HTML anchor in {raw!r}"
                # The existing theme skip-link on the standalone 404 page
                # has no main landmark. Report it without changing that page.
                if relative.as_posix() == "404.html" and target == path and raw == "#main":
                    warnings.append(message)
                else:
                    errors.append(message)
    return errors, warnings, external, len(pages)


def check_external(url):
    """Report definite missing pages; distinguish blocked/transient requests."""
    request = Request(url, headers={"User-Agent": "WebsiteLinkCheck/1.0"})
    try:
        with urlopen(request, timeout=12) as response:
            if 200 <= response.status < 400:
                return "ok", ""
            return "warning", f"HTTP {response.status}"
    except HTTPError as exc:
        if exc.code in (404, 410):
            return "broken", f"HTTP {exc.code}"
        return "warning", f"HTTP {exc.code}"
    except (URLError, OSError, ValueError) as exc:
        return "warning", str(exc)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, help="Built site directory (normally _site)")
    parser.add_argument("--origin", default=ORIGIN)
    parser.add_argument("--external", action="store_true", help="Also check external HTTP(S) URLs")
    args = parser.parse_args()
    errors, warnings, external, count = check_site(args.site, args.origin)
    if args.external:
        with ThreadPoolExecutor(max_workers=6) as pool:
            for url, (status, reason) in zip(sorted(external), pool.map(check_external, sorted(external))):
                message = f"{url}: {reason} (linked from {', '.join(sorted(external[url]))})"
                if status == "broken":
                    errors.append(message)
                elif status == "warning":
                    warnings.append(message)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Checked {count} HTML files; {len(external)} unique external URLs "
          f"{'checked' if args.external else 'collected (use --external to check)'}.")
    print(f"{len(errors)} broken links; {len(warnings)} warnings.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
