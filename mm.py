#!/usr/bin/env python
"""
COPY THIS FILE TO YOUR PROJECT.
---------
This file generates all the necessary files for packaging for the project.
Read more about it at https://github.com/jpscaletti/mastermold/
"""
from pathlib import Path


data = {
    "title": "Proper Form",
    "name": "proper_form",
    "pypi_name": "proper_form",
    "version": "1.190730",
    "author": "Juan-Pablo Scaletti",
    "author_email": "juanpablo@jpscaletti.com",
    "description": "A not-terrible Python form library.",
    "copyright": "2019",
    "repo_name": "jpscaletti/proper-form",
    "home_url": "https://github.com/jpscaletti/proper-form",
    # Displayed in the pypi project page
    # "project_urls": {
    #     "Documentation": "https://github.com/jpscaletti/proper-form",
    # },

    "development_status": "4 - Beta",
    "minimal_python": 3.6,
    "install_requires": [
        "email-validator ~=1.0.4",
        "idna ~=2.8",
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
    ],
    "entry_points": "",

    "coverage_omit": [],

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
    ".DS_Store",
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
        nav = list(filter(None, mkdocs.get("nav") or []))
        data["docs_nav"] = nav or ["index.md"]

    if data["has_docs"]:
        save_current_nav()
    else:
        data["docs_nav"] = []

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
