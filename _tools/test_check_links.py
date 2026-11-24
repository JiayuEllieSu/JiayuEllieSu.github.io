import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from check_links import check_site, check_external


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("index.html", "<h1 id='home'>Home</h1>")

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_pages_assets_and_anchors(self):
        self.write("index.html", """
          <a href='/projects/#math'>Project</a>
          <a href='/assets/a%20b.pdf?download=1'>PDF</a>
          <audio><source src='/assets/song.mp3'></audio>
          <script src='/assets/site.js'></script>
          <a href='https://jiayuelliesu.github.io/projects/'>Same site</a>
          <a href='mailto:example@example.com'>Email</a>
        """)
        self.write("projects/index.html", "<h2 id='math'>Math</h2><a href='../'>Home</a>")
        for name in ("assets/a b.pdf", "assets/song.mp3", "assets/site.js"):
            self.write(name, "")
        errors, warnings, external, count = check_site(self.root)
        self.assertEqual((errors, warnings, dict(external), count), ([], [], {}, 2))

    def test_missing_path_and_anchor(self):
        self.write("index.html", "<a href='/gone.pdf'>File</a><a href='#missing'>Section</a>")
        errors, warnings, _, _ = check_site(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("missing file" in error for error in errors))
        self.assertTrue(any("missing HTML anchor" in error for error in errors))
        self.assertEqual(warnings, [])

    def test_external_deduplication_and_404_skip_link(self):
        self.write("index.html", "<a href='https://example.org/#a'>A</a><a href='https://example.org/#b'>B</a>")
        self.write("404.html", "<a href='#main'>Skip to content</a>")
        errors, warnings, external, _ = check_site(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertEqual(list(external), ["https://example.org/"])

    def test_missing_vs_blocked_external(self):
        for code, expected in ((404, "broken"), (410, "broken"), (403, "warning"), (429, "warning"), (503, "warning")):
            with self.subTest(code=code), patch("check_links.urlopen", side_effect=HTTPError("https://example.org", code, "", {}, None)):
                self.assertEqual(check_external("https://example.org")[0], expected)
        with patch("check_links.urlopen", side_effect=URLError("timeout")):
            self.assertEqual(check_external("https://example.org")[0], "warning")


if __name__ == "__main__":
    unittest.main()
