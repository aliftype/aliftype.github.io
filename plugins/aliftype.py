"""Site specific bits that used to live in Jekyll layouts and plugins."""

import json
import os
import unicodedata

import sass
from markdown.extensions import Extension
from pelican import signals

# Characters Ruby’s /\p{Word}/ matches, used by kramdown’s GFM parser to build
# heading IDs.
WORD_CATEGORIES = frozenset(
    ("Lu", "Ll", "Lt", "Lm", "Lo", "Mn", "Mc", "Me", "Nd", "Nl", "Pc")
)

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


def page_metadata(generator, metadata):
    """Fill in what Jekyll used to derive from the page path."""
    fonts = generator.settings["FONTS"]
    parts = metadata["slug"].split("/")
    project = parts[0] if len(parts) > 1 and parts[0] in fonts else None

    metadata["project"] = project
    metadata["dir"] = "/".join(["", *parts[:-1], ""])

    if project:
        # These were the per-path defaults in Jekyll's _config.yml.
        metadata.setdefault("template", "font")
        metadata.setdefault("title", fonts[project]["title"])

    if parts[-1] == "index":
        metadata["url"] = "/".join([*parts[:-1], ""])


def write_redirects(generator, writer):
    """Redirect pages for the old URLs, was jekyll-redirect-from."""
    template = generator.get_template("redirect")
    for page in generator.pages:
        if "redirect_from" not in page.metadata:
            continue
        writer.write_file(
            page.metadata["redirect_from"].strip("/") + ".html",
            template,
            generator.context,
            target=f"{generator.settings['SITEURL']}/{page.url}",
        )


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
    signals.page_generator_context.connect(page_metadata)
    signals.page_writer_finalized.connect(write_redirects)
    signals.finalized.connect(compile_sass)
