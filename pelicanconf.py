import os
import subprocess
import sys

import yaml

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "plugins"))

import aliftype  # noqa: E402


def _data(name):
    with open(os.path.join(BASE, "_data", name), encoding="utf-8") as f:
        return yaml.safe_load(f)


AUTHOR = "Khaled Hosny"
SITENAME = "حروف ألف"
SITESUBTITLE = "مسبك حروف رقمي"
SITEURL = ""
EMAIL = "info@aliftype.com"
FEDIVERSE_CREATOR = "@khaled@typo.social"

TIMEZONE = "Africa/Cairo"
DEFAULT_LANG = "ar"
# ICU locales, for formatting like calendar and digits
LOCALES = {"ar": "ar@numbers=arab", "en-US": "en_GB"}

FONTS = _data("config.yml")
MESSAGES = _data("messages.yml")

# What jekyll-github-metadata used to provide.
GITHUB_HOSTNAME = "github.com"
GITHUB_OWNER = "aliftype"
GITHUB_OWNER_URL = f"https://{GITHUB_HOSTNAME}/{GITHUB_OWNER}"
BUILD_REVISION = os.environ.get("GITHUB_SHA") or subprocess.run(
    ["git", "-C", BASE, "rev-parse", "HEAD"],
    capture_output=True,
    text=True,
).stdout.strip()

PATH = "."
OUTPUT_PATH = "output"
CACHE_PATH = "cache"
THEME = "theme"

ARTICLE_PATHS = ["blog"]
PAGE_PATHS = ["index.md", "english.md", "about", "artwork", *FONTS]
PAGE_EXCLUDES = ["amiri/documentation"]
STATIC_PATHS = [
    "CNAME",
    "app",
    "assets",
    "amiri/documentation",
    *(f"{font}/app" for font in FONTS if FONTS[font].get("app")),
]
STATIC_EXCLUDES = ["app/harfbuzz", "assets/css"]
IGNORE_FILES = [".*"]

# URLs and file names follow the source tree, as they did under Jekyll.
PATH_METADATA = r"(?P<slug>.+)\.md"
PAGE_URL = PAGE_LANG_URL = "{slug}"
PAGE_SAVE_AS = PAGE_LANG_SAVE_AS = "{slug}.html"
ARTICLE_URL = "{slug}/english"
ARTICLE_SAVE_AS = "{slug}/english.html"
ARTICLE_LANG_URL, ARTICLE_LANG_SAVE_AS = ARTICLE_URL, ARTICLE_SAVE_AS
ARTICLE_ORDER_BY = "reversed-date"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"

# No categories, tags or authors: without templates for them Pelican falls
# back to its own bundled theme, which looks nothing like the site.
USE_FOLDER_AS_CATEGORY = False
CATEGORY_SAVE_AS = TAG_SAVE_AS = AUTHOR_SAVE_AS = ""
PAGE_TRANSLATION_ID = None
PAGE_ORDER_BY = "relative_source_path"

DIRECT_TEMPLATES = ["blog", "blog_english", "sitemap", "robots"]
BLOG_SAVE_AS = "blog/index.html"
BLOG_ENGLISH_SAVE_AS = "blog/english.html"
TEMPLATE_EXTENSIONS = [".html", ".xml", ".txt"]
SITEMAP_SAVE_AS = "sitemap.xml"
ROBOTS_SAVE_AS = "robots.txt"

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["pelican.plugins.jinja2content", "aliftype"]
JINJA_ENVIRONMENT = {
    "trim_blocks": True,
    "lstrip_blocks": True,
    "keep_trailing_newline": True,
}
JINJA_GLOBALS = {"picture": aliftype.picture}
JINJA_FILTERS = {"jsonify": aliftype.jsonify, "long_date": aliftype.long_date}

MARKDOWN = {
    "extensions": [
        "markdown.extensions.extra",
        "markdown.extensions.meta",
        "markdown.extensions.smarty",
        "markdown.extensions.toc",
        aliftype.AlifTypeExtension(),
    ],
    "extension_configs": {
        "markdown.extensions.smarty": {
            "substitutions": {
                "ellipsis": "…",
                "ndash": "–",
                "mdash": "—",
                "left-single-quote": "‘",
                "right-single-quote": "’",
                "left-double-quote": "“",
                "right-double-quote": "”",
                "left-angle-quote": "«",
                "right-angle-quote": "»",
            },
        },
        "markdown.extensions.toc": {"slugify": aliftype.slugify},
    },
    "output_format": "xhtml",
}

DELETE_OUTPUT_DIRECTORY = True

FEED_ALL_RSS = "blog/feed.xml"
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
