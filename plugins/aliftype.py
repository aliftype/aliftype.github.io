"""Site specific bits that used to live in Jekyll layouts and plugins."""

import json
import os
import unicodedata

import sass
from jinja2 import Environment, FileSystemLoader
from markdown.extensions import Extension
from pelican import signals
from pelican.contents import Page

# Characters Ruby’s /\p{Word}/ matches, used by kramdown’s GFM parser to build
# heading IDs.
WORD_CATEGORIES = frozenset(
    ("Lu", "Ll", "Lt", "Lm", "Lo", "Mn", "Mc", "Me", "Nd", "Nl", "Pc")
)

_pages = []


def slugify(value, separator):
    """Generate heading IDs the way kramdown’s GFM parser does."""
    value = value.lower()
    value = "".join(
        c
        for c in value
        if c in "- \t" or unicodedata.category(c) in WORD_CATEGORIES
    )
    return value.replace(" ", separator).replace("\t", separator)


class AlifTypeExtension(Extension):
    """Treat <picture> as a block level element, like kramdown does."""

    def extendMarkdown(self, md):
        md.block_level_elements.append("picture")


def picture(src, alt=None, ext="svg"):
    """A light/dark aware <picture>, was the “picture” Jekyll include."""
    src = "/" + src.lstrip("/")
    attrs = f' alt="{alt}" title="{alt}"' if alt else ""
    return (
        f'<picture><source srcset="{src}_dark.{ext}"'
        f' media="(prefers-color-scheme: dark)" />'
        f'<img src="{src}.{ext}"{attrs} /></picture>'
    )


def jsonify(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def page_metadata(page):
    """Fill in what Jekyll used to derive from the page path."""
    if not isinstance(page, Page):
        return

    fonts = page.settings["FONTS"]
    parts = os.path.splitext(page.relative_source_path)[0].split(os.sep)
    project = parts[0] if len(parts) > 1 and parts[0] in fonts else None

    page.project = project
    page.dir = "/".join(["", *parts[:-1], ""])

    if project:
        # These were the per-path defaults in Jekyll’s _config.yml.
        if "template" not in page.metadata:
            page.template = "font"
        if "title" not in page.metadata:
            page.title = fonts[project]["title"]

    page.override_save_as = "/".join(parts) + ".html"
    if parts[-1] == "index":
        page.override_url = "/".join(["", *parts[:-1], ""]).lstrip("/")
    else:
        page.override_url = page.override_save_as


def collect_pages(generator):
    # Kept for write_redirects, which runs once the output has been written.
    _pages[:] = generator.pages


def write_redirects(pelican):
    """Redirect pages for the old URLs, was jekyll-redirect-from."""
    settings = pelican.settings
    env = Environment(
        loader=FileSystemLoader(os.path.join(settings["THEME"], "templates"))
    )
    template = env.get_template("redirect.html")
    for page in _pages:
        if "redirect_from" not in page.metadata:
            continue
        source = page.metadata["redirect_from"].strip("/") + ".html"
        path = os.path.join(settings["OUTPUT_PATH"], source)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        target = f"{settings['SITEURL']}/{page.url}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(template.render(target=target))


def compile_sass(pelican):
    """Compile the stylesheets, was jekyll-sass-converter."""
    settings = pelican.settings
    source = os.path.join(settings["PATH"], "assets", "css")
    output = os.path.join(settings["OUTPUT_PATH"], "assets", "css")
    os.makedirs(output, exist_ok=True)
    for name in sorted(os.listdir(source)):
        stem, ext = os.path.splitext(name)
        if ext != ".scss" or name.startswith("_"):
            continue
        css = sass.compile(
            filename=os.path.join(source, name),
            include_paths=[os.path.join(settings["PATH"], "_sass")],
            output_style="expanded",
        )
        with open(os.path.join(output, stem + ".css"), "w", encoding="utf-8") as f:
            f.write(css)


def register():
    signals.content_object_init.connect(page_metadata)
    signals.page_generator_finalized.connect(collect_pages)
    signals.finalized.connect(compile_sass)
    signals.finalized.connect(write_redirects)
