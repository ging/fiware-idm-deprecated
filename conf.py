# -*- coding: utf-8 -*-
#
import os

# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

    # Override default css to get a larger width for local build
    def setup(app):
        app.add_stylesheet('mystyle.css')
else:
    # Override default css to get a larger width for ReadTheDoc build
    html_context = {
        'css_files': [
            '_static/mystyle.css',
        ],
    }

# otherwise, readthedocs.org uses their theme by default, so no need to specify it

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'FIWARE-SDC'
