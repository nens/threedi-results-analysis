#/***************************************************************************
# ThreeDiToolbox
#
# Toolbox for working with 3Di hydraulic models
#							 -------------------
#		begin				: 2016-03-04
#		git sha				: $Format:%H$
#		copyright			: (C) 2016 by Nelen&Schuurmans
#		email				: servicedesk@nelen-schuurmans.nl
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

#################################################
# Edit the following to match your sources lists
#################################################


#Add iso code for any locales you want to support here (space separated)
# default is no locales
# LOCALES = af
LOCALES =

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
#LRELEASE = lrelease
#LRELEASE = lrelease-qt4


# translation
SOURCES = __init__.py threedi_toolbox.py threedi_toolbox_dockwidget.py

PLUGINNAME = ThreeDiToolbox

PY_FILES = __init__.py
# ^^^ The rest of the python files is picked up because they're in git.

UI_FILES = ui/*.ui

EXTRAS = metadata.txt icon.png

COMPILED_RESOURCE_FILES = resources.py

HELP = help/build/html

PLUGIN_UPLOAD = $(c)/plugin_upload.py

RESOURCE_SRC=$(shell grep '^ *<file' resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')

default: compile

compile: $(COMPILED_RESOURCE_FILES)

%.py : %.qrc $(RESOURCES_SRC)
	pyrcc5 -o $*.py  $<

%.qm : %.ts
	$(LRELEASE) $<

test: compile transcompile
	@echo "#### Python tests"
	QT_QPA_PLATFORM=offscreen pytest --cov --flake8

docstrings:
	@echo "#### Docstring coverage report"
	python3 scripts/docstring-report.py

zip: compile transcompile
	@echo
	@echo "---------------------------"
	@echo "Creating plugin zip bundle."
	@echo "---------------------------"
	rm -rf /tmp/$(PLUGINNAME)
	cd /tmp; cp -r $(CURDIR) $(PLUGINNAME)
	@echo "Hack to install deps. Better idea: put all this in a new directive and let qgispluginreleaser call it."
	cd /tmp/$(PLUGINNAME) && pip install -r requirements.txt --target=external --no-deps -U
	rm -rf /tmp/$(PLUGINNAME)/test
	rm -rf /tmp/$(PLUGINNAME)/threedi_statistics/tests
	rm -rf /tmp/$(PLUGINNAME)/water_balance/tests
	rm -rf /tmp/$(PLUGINNAME)/.git
	rm -rf /tmp/$(PLUGINNAME)/*.zip
	rm -rf /tmp/$(PLUGINNAME)/Docker
	rm -rf /tmp/$(PLUGINNAME)/docker-compose.yml
	rm -rf /tmp/$(PLUGINNAME)/docker-compose.override.yml
	rm -rf /tmp/$(PLUGINNAME)/__pycache__
	find /tmp/$(PLUGINNAME) -iname "*.pyc" -delete
	cd /tmp; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)

package: compile
	# Create a zip package of the plugin named $(PLUGINNAME).zip.
	# This requires use of git (your plugin development directory must be a
	# git repository).
	# To use, pass a valid commit or tag as follows:
	#   make package VERSION=Version_0.3.2
	@echo
	@echo "------------------------------------"
	@echo "Exporting plugin to zip package.	"
	@echo "------------------------------------"
	rm -f $(PLUGINNAME).zip
	git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
	echo "Created package: $(PLUGINNAME).zip"

upload: zip
	@echo
	@echo "-------------------------------------"
	@echo "Uploading plugin to QGIS Plugin repo."
	@echo "-------------------------------------"
	$(PLUGIN_UPLOAD) $(PLUGINNAME).zip

transup:
	@echo
	@echo "------------------------------------------------"
	@echo "Updating translation files with any new strings."
	@echo "------------------------------------------------"
	@scripts/update-strings.sh $(LOCALES)

transcompile:
	@scripts/compile-strings.sh $(LRELEASE) $(LOCALES)

transclean:
	@echo
	@echo "------------------------------------"
	@echo "Removing compiled translation files."
	@echo "------------------------------------"
	rm -f i18n/*.qm

clean:
	@echo
	@echo "------------------------------------"
	@echo "Removing uic and rcc generated files"
	@echo "------------------------------------"
	rm $(COMPILED_UI_FILES) $(COMPILED_RESOURCE_FILES)

doc:
	@echo
	@echo "------------------------------------"
	@echo "Building documentation using sphinx."
	@echo "------------------------------------"
	cd help; make html


# Run pep8 + pyflakes checks
flake8:
	@echo "#### PEP8/pyflakes issues"
	@flake8 .
	@echo "No issues found."


beautiful:
	isort -y
	black .
	flake8 .
