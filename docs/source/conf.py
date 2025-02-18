# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from navigate import __version__

sys.path.insert(0, os.path.abspath("../../src"))


# -- Project information -----------------------------------------------------

project = "navigate"
copyright = "2024, Dean Lab, UT Southwestern Medical Center"
author = "Dean Lab, UT Southwestern Medical Center"

# The full version, including alpha/beta/rc tags
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx_toolbox.collapse",
    "sphinx.ext.autosectionlabel",
]

autosectionlabel_prefix_document = True

# Boolean indicating whether to scan all found documents for
# autosummary directives, and to generate stub pages for each
# (http://sphinx-doc.org/latest/ext/autosummary.html)
autosummary_generate = True

# Both the class’ and the __init__ method’s docstring are concatenated
# and inserted.
autoclass_content = "class"  # "both"

# inheritance_graph_attrs = {'rankdir': "TB",
#                           'clusterrank': 'local'}
# inheritance_node_attrs  = {'style': 'filled'}

# This value selects how automatically documented members are sorted
# (http://sphinx-doc.org/latest/ext/autodoc.html)
autodoc_member_order = "groupwise"

# This value is a list of autodoc directive flags that should be
# automatically applied to all autodoc
# directives. (http://sphinx-doc.org/latest/ext/autodoc.html)
autodoc_default_flags = [
    "members",
    "inherited-members",
    "show-inheritance",
]

autodoc_inherit_docstrings = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["./_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# If true, the current module name will be prepended to all
# description unit titles (such as .. function::).
add_module_names = True

# The default language to highlight source code
highlight_language = "python"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["**/configurations_archive/*", "*archive*", "**/*_archive.rst"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_show_sphinx = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

html_logo = "../../src/navigate/view/icon/mic.png"

pygments_style = "sphinx"

# -- Linkcheck Options ---------------------------------------------
linkcheck_ignore = [
    r'http://proxy\.your_university\.edu:1234',
    r'https://proxy\.your_university\.edu:1234'
]
# -- LaTeX output options ----------------------------------------------------

latex_elements = {
    "preamble": r"""
                  \usepackage[utf8]{inputenc}
                  \usepackage{enumitem}
                  \setlistdepth{99}
                  \DeclareUnicodeCharacter{03BC}{$\mu$}
                  """,
    "extraclassoptions": "openany,oneside",
}

latex_documents = [
    (
        "index",
        "navigate.tex",
        "navigate Documentation",
        "Dean Lab, UT Southwestern Medical Center",
        "manual",
        True,
    ),
]

latex_domain_indices = False
