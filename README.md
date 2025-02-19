# SQL Documentation

This repository contains the documentation for our SQL models, built using Sphinx.

## Local Development

To build the documentation locally:

1. Clone this repository
2. Install dependencies:
   ```bash
   cd docs
   pip install -r requirements.txt
   ```
3. Build the documentation:
   ```bash
   cd docs
   make html
   ```
4. The built documentation will be in `docs/build/html`

For live preview during development:
```bash
cd docs
sphinx-autobuild source build/html
```

## Adding New Documentation

1. Create new `.rst` files in the `docs/source` directory
2. Add them to the toctree in `index.rst`
3. Build and check your changes locally
4. Commit and push to trigger automatic deployment

## Deployment

The documentation is automatically built and deployed to GitHub Pages when changes are pushed to the main branch.
