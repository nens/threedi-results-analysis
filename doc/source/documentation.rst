Documentation howto
===================

To build the documentation, run ``make html``::

  docker-compose run qgis-desktop make html

Some handy sphinx links:

- https://www.sphinx-doc.org/en/master/markup/inline.html

- https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

- https://www.sphinx-doc.org/en/master/domains.html#cross-referencing-python-objects
  for pointing at functions/modules/methods/classes.

- https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
  for google-style argument lists in docstrings.

In the **reference** part of the documentation, add ``automodule`` statements
to files that you're missing.
