#!/usr/bin/env python
"""
COPY THIS FILE TO YOUR PROJECT.
---------
This file generates all the necessary files for packaging for the project.
Read more about it at https://github.com/jpscaletti/mastermold/
"""
from pathlib import Path


data = {
    "title": "Proper",
    "name": "proper",
    "pypi_name": "proper",
    "version": "1.190730",
    "author": "Juan-Pablo Scaletti",
    "author_email": "juanpablo@jpscaletti.com",
    "description": "A web framework optimized for programmer happiness.",
    "copyright": "2019",
    "repo_name": "jpscaletti/proper",
    "home_url": "https://properframework.dev",
    # Displayed in the pypi project page
    "project_urls": {
        "Documentation": "https://properframework.dev/docs",
    },

    "development_status": "4 - Beta",
    "minimal_python": 3.6,
    "install_requires": [
        "multipart ~=0.2",
        "copier ~=2.4",
        "cryptography ~=2.5",
        "gevent ~=1.4",
        "gevent-websocket",
        "itsdangerous ~=1.1",
        "jinja2 ~=2.10",
        "pyceo ~=2.190702",
        "toml ~=0.10",
        "text-editor ~=1.0.5",  # WITH A DASH!
        "ujson ~=1.35",
        "wsaccel ~=0.6",
    ],
    "testing_requires": [
        "pytest-cov",
    ],
    "development_requires": [
        "pytest",
        "pytest-flake8",
        "flake8",
        "ipdb",
        "tox",

        "mkdocs",
        "mkdocs-material",
        "pymdown-extensions",
        "pygments",
        "pygments-github-lexers",
    ],
    "entry_points": "proper = proper.cli:run",

    "coverage_omit": [
        "proper/base_channel.py",
        "proper/cli.py",
        "proper/server.py",
        "proper/router/channel.py",
    ],

    "has_docs": True,
    "google_analytics": "UA-XXXXXXXX-X",
    "docs_nav": [],
}

exclude = [
    "copier.yml",
    "README.md",
    ".git",
    ".git/*",
    ".venv",
    ".venv/*",
]


def do_the_thing():
    import copier
    from ruamel.yaml import YAML

    def save_current_nav():
        yaml = YAML()
        mkdocs_path = Path("docs") / "mkdocs.yml"
        if not mkdocs_path.exists():
            return
        mkdocs = yaml.load(mkdocs_path)
        data["docs_nav"] = mkdocs.get("nav")

    if data["has_docs"]:
        save_current_nav()

    copier.copy(
        # "gh:jpscaletti/mastermold.git",
        "../mastermold",  # Path to the local copy of Master Mold
        ".",
        data=data,
        exclude=exclude,
        force=True,
        cleanup_on_error=False
    )


if __name__ == "__main__":
    do_the_thing()
