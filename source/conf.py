# -*- coding: utf-8 -*-
#
# Updated documentation of the configuration options is available at
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import posixpath
from os import environ
from datetime import date
from subprocess import check_call

from antmicro_sphinx_utils.defaults import (
    numfig_format,
    extensions as default_extensions,
    myst_enable_extensions as default_myst_enable_extensions,
    myst_fence_as_directive as default_myst_fence_as_directive,
    antmicro_html,
    antmicro_latex
)

# -- General configuration -----------------------------------------------------

project = u'Renode - documentation'
basic_filename = 'renode-docs'
authors = u'Antmicro'
copyright = u'2010-' + str(date.today().year) + ' ' + authors

version = ''
release = ''

sphinx_immaterial_override_builtin_admonitions = False

numfig = True

extensions = list(set(default_extensions + [
    'sphinxcontrib.rsvgconverter',
    'sphinx.ext.extlinks',
    'sphinx_design',
    'sphinx_inline_tabs'
]))

myst_enable_extensions = default_myst_enable_extensions
myst_fence_as_directive = default_myst_fence_as_directive

myst_substitutions = {
    "project": project
}

extlinks = {
    'script'    : ('https://github.com/renode/renode/blob/master/scripts/%s', '%s'),
    'risrc'     : ('https://github.com/renode/renode-infrastructure/blob/3f1abde88ac5a2dae326b77ab91892f335e78f80/%s', '%s'),
    'rsrc'      : ('https://github.com/renode/renode/blob/c16c7bceca07734f6f49b4e107d299aa04b8857c/%s' , '%s')
}

today_fmt = '%Y-%m-%d'

# -- Options for HTML output ---------------------------------------------------

html_theme = 'sphinx_immaterial'

html_last_updated_fmt = today_fmt

html_show_sphinx = False

html_title = project

(
    _,
    html_theme_options,
    html_context
) = antmicro_html(
    gh_slug=environ.get('GITHUB_REPOSITORY', 'renode/renode'),
    #pdf_url=f"{basic_filename}.pdf",
)

html_theme_options["palette"][0].update({
    "primary": "blue",
    "accent": "light-blue",
})
html_theme_options["palette"][1].update({
    "primary": "blue",
    "accent": "light-blue",
})

html_theme_options["features"].append([
    "navigation.expand",
    "navigation.tabs",
    "toc.integrate",
    "navigation.sections",
    "navigation.instant",
    "header.autohide",
    "navigation.top",
    "navigation.tracking",
    "search.highlight",
    "search.share",
    "toc.follow",
    "toc.sticky",
])

html_theme_options.update({
    "globaltoc_collapse": True,
    "site_url": "https://renode.io/",
})

html_logo = 'renode-sphinx/logo-400-html.png'

# -- Options for LaTeX output --------------------------------------------------

(
    latex_elements,
    latex_documents,
    _,
    _,
) = antmicro_latex(basic_filename, authors, project)

latex_logo = 'renode-sphinx/logo-latex.pdf'
latex_additional_files = ['%s/%s.sty' % ('renode-sphinx','renode'),latex_logo]

def setup(app):
    app.connect('build-finished', on_build_finished)
    check_call("./generate-renode-platforms.sh", shell=True, cwd=os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def on_build_finished(app, exc):
    if not app.builder or app.builder.name != 'html':
        return

    if exc is None:
        bad_js = posixpath.join(app.outdir, "_static", "design-tabs.js")
        try:
            os.remove(bad_js)
        except OSError:
            pass