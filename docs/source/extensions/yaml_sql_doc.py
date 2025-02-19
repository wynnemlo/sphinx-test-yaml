# extensions/yaml_sql_doc.py
import os
from pathlib import Path

import yaml
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)

def discover_sql_files(repo_path):
    """Discover all .bq.sql files in the repository."""
    sql_files = []
    repo_path = Path(repo_path)
    
    for sql_file in repo_path.rglob('*.bq.sql'):
        relative_path = sql_file.relative_to(repo_path)
        sql_files.append(str(relative_path))
    
    return sorted(sql_files)

def parse_sql_file(filepath):
    """Parse a SQL file with YAML header."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Extract YAML between /* and */
        if '/*' in content and '*/' in content:
            yaml_text = content.split('/*')[1].split('*/')[0]
            try:
                yaml_data = yaml.safe_load(yaml_text)
                return yaml_data
            except yaml.YAMLError as e:
                logger.warning(f"Failed to parse YAML in {filepath}: {e}")
                return None
    except FileNotFoundError:
        logger.warning(f"Could not find SQL file: {filepath}")
        return None
    except Exception as e:
        logger.warning(f"Error reading SQL file {filepath}: {e}")
        return None
    return None

class YAMLSQLDocDirective(SphinxDirective):
    """Directive to document SQL files with YAML headers."""
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'repo_path': directives.unchanged
    }

    def run(self):
        sql_path = self.arguments[0]
        
        # Try to get repo path from directive options first, then from conf.py
        repo_path = self.options.get('repo_path', '')
        if not repo_path and hasattr(self.config, 'yaml_demo_path'):
            repo_path = self.config.yaml_demo_path
        
        if repo_path:
            full_path = Path(repo_path) / sql_path
        else:
            full_path = Path(sql_path)
        
        full_path = full_path.resolve()
        
        logger.info(f"Looking for SQL file at: {full_path}")
        
        if not full_path.exists():
            return [nodes.paragraph('', f'SQL file not found: {full_path}')]

        yaml_data = parse_sql_file(str(full_path))
        if not yaml_data:
            return [nodes.paragraph('', f'No valid YAML data found in: {full_path}')]

        # Create a container node
        container = nodes.container()
        container['classes'].append('sql-doc')

        # Document metadata
        if 'doc' in yaml_data:
            doc_para = nodes.paragraph()
            doc_para += nodes.Text(yaml_data['doc'])
            container += doc_para

        # Table schema
        if 'output' in yaml_data and 'table_schema' in yaml_data['output']:
            schema_title = nodes.paragraph()
            schema_title += nodes.strong(text='Table Schema')
            container += schema_title
            
            table = nodes.table()
            tgroup = nodes.tgroup(cols=2)
            table += tgroup
            
            for _ in range(2):
                colspec = nodes.colspec(colwidth=1)
                tgroup += colspec
            
            thead = nodes.thead()
            tgroup += thead
            header_row = nodes.row()
            thead += header_row
            header_row += nodes.entry('', nodes.paragraph(text='Field Name'))
            header_row += nodes.entry('', nodes.paragraph(text='Type'))
            
            tbody = nodes.tbody()
            tgroup += tbody
            
            for field in yaml_data['output']['table_schema']['fields']:
                row = nodes.row()
                tbody += row
                row += nodes.entry('', nodes.paragraph(text=field['name']))
                row += nodes.entry('', nodes.paragraph(text=field['type']))
            
            container += table

        # Dependencies
        if 'inputs' in yaml_data:
            deps_title = nodes.paragraph()
            deps_title += nodes.strong(text='Dependencies')
            container += deps_title
            
            bullet_list = nodes.bullet_list()
            for dep in yaml_data['inputs']:
                item = nodes.list_item()
                item += nodes.paragraph(text=dep)
                bullet_list += item
            
            container += bullet_list

        return [container]

def generate_sql_doc_pages(app):
    """Generate documentation pages for all SQL files."""
    repo_path = app.config.yaml_demo_path
    if not repo_path:
        logger.warning("yaml_demo_path not set in conf.py")
        return

    # Discover all SQL files
    sql_files = discover_sql_files(repo_path)
    
    # Create the sql_models directory if it doesn't exist
    docs_dir = Path(app.srcdir) / 'sql_models'
    docs_dir.mkdir(exist_ok=True)
    
    # Generate index.rst for sql_models
    index_content = """SQL Models
==========

.. toctree::
   :maxdepth: 2
   :caption: Models:

"""
    
    # Generate a page for each SQL file
    for sql_file in sql_files:
        # Convert path to documentation path
        doc_name = str(sql_file).replace('/', '_').replace('.bq.sql', '')
        rst_file = docs_dir / f"{doc_name}.rst"
        
        # Generate RST content
        rst_content = f"""
{doc_name}
{'=' * len(doc_name)}

.. yamlsqldoc:: {sql_file}
   :repo_path: {repo_path}
"""
        
        # Write the RST file
        rst_file.write_text(rst_content)
        
        # Add to index
        index_content += f"   {doc_name}\n"
    
    # Write the index file
    (docs_dir / "index.rst").write_text(index_content)

def setup(app: Sphinx):
    app.add_directive('yamlsqldoc', YAMLSQLDocDirective)
    app.add_config_value('yaml_demo_path', None, 'env')
    app.connect('builder-inited', generate_sql_doc_pages)
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
