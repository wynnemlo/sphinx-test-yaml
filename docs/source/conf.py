import os
import sys
from pathlib import Path

# -- Project information -----------------------------------------------------
project = 'test-yaml'
copyright = '2025, Wynne Lo'
author = 'Wynne Lo'

# -- General configuration ---------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'extensions')))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'yaml_sql_doc'
]

# Path to SQL repository - different for local development vs CI
if os.environ.get('GITHUB_ACTIONS'):
    # In GitHub Actions, the SQL repo is checked out to 'sql-repo'
    yaml_demo_path = str(Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'sql-repo'))).resolve())
else:
    # Local development path
    yaml_demo_path = '../sql-repo'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
