import os
import sys
from pathlib import Path
from datetime import datetime

# -- Project information -----------------------------------------------------
project = 'CPH Analytics Catalog'
copyright = 'AF Pod'
author = 'AF Pod'
release = '0.1'
today_fmt = '%B %d, %Y'

# -- General configuration ---------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'extensions')))
# Add chatbot and API paths
sys.path.insert(0, os.path.abspath('../api/app'))

# Enable chatbot widget
html_static_path = ['_static']
templates_path = ['_templates']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'yaml_sql_doc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
	'sphinx.ext.doctest',
    'sphinx_tabs.tabs',
    'sphinx_togglebutton',
    'sphinx_book_theme',
	'sphinx.ext.todo',
    'iframe',
	'chatbot_api',
]

# Path to SQL repository - different for local development vs CI
if os.environ.get('GITHUB_ACTIONS'):
    # In GitHub Actions, the SQL repo is checked out to 'sql-repo'
    yaml_demo_path = str(Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'sql-repo'))).resolve())
else:
    # Local development path
    yaml_demo_path = '../sql-repo'

autodoc_mock_imports = ['bs4', 'requests']
todo_include_todos = True
napoleon_google_docstring = False
napoleon_include_special_with_doc = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_book_theme"
html_copy_source = True

html_title = "CPH Analytics Catalog"

html_last_updated_fmt = ""

html_sidebars = {
    "reference/blog/*": [
        "navbar-logo.html",
        "search-field.html",
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/tagcloud.html",
        "ablog/categories.html",
        "ablog/archives.html",
        "sbt-sidebar-nav.html",
    ]
}

html_static_path = ["_static"]
html_css_files = ["custom.css"]
# Enable chatbot widget
templates_path = ['_templates']

html_sidebars = {
  "path/to/page": [],
}

html_theme_options = {
    "secondary_sidebar_items": {
        "path/to/page": []},
    "repository_url": 'https://github.com/CloverHealth/ca-pipeline/tree/master/counterpart_health/tenant_common/data_flows',
    "repository_branch": 'main',
    "home_page_in_toc": True,
    "path_to_docs": "docs/",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": False,
    # Please don't change unless you know what you're doing.
    "extra_footer": """
        <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
            <img
                alt="Creative Commons License"
                style="border-width:0"
                src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png"/>
        </a>
        <br>
        These works by
            <a
                xmlns:cc="https://creativecommons.org/ns#"
                href="https://openedx.org"
                property="cc:attributionName"
                rel="cc:attributionURL"
            >Axim Collaborative</a>
        are licensed under a
            <a
                rel="license"
                href="https://creativecommons.org/licenses/by-sa/4.0/"
            >Creative Commons Attribution-ShareAlike 4.0 International License</a>.
    """
}
