#!/usr/bin/env python
"""
COPY THIS FILE TO YOUR PROJECT.
---------
This file generates all the necessary files for packaging for the project.
Read more about it at https://github.com/jpscaletti/mastermold/
"""
data = {
    "title": "Proper Form",
    "name": "proper_form",
    "pypi_name": "proper_form",
    "version": "0.190726",
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
        "markupsafe ~=1.1.1",
        "python-slugify ~=3.0.3",
    ],
    "testing_requires": [
        "pytest",
        "pytest-cov",
        "pony",
        "sqlalchemy",
    ],
    "development_requires": [
        "pytest-flake8",
        "flake8",
        "ipdb",
        "tox",
        "mkdocs",
        "pymdown-extensions",
        "pygments",
        "pygments-github-lexers",
    ],
    "entry_points": "",

    "coverage_omit": [],
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

    copier.copy(
        # "gh:jpscaletti/mastermold.git",
        "../mastermold",  # Path to the local copy of Master Mold
        ".",
        data=data,
        exclude=exclude,
        force=False,
        cleanup_on_error=False
    )


if __name__ == "__main__":
    do_the_thing()
