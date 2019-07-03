# Minimal makefile for Sphinx documentation
#

SPHINXOPTS    = -a -E
SPHINXBUILD   = python3 -msphinx
SPHINXPROJ    = ThreeDiToolbox
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make html".
html: build
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# If the index.rst changes, we want all docs go get a new TOC.
build: source/index.rst
	rm -rf build
	mkdir build

.PHONY: help Makefile
