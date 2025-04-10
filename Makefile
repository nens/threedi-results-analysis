#/***************************************************************************
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
LOCALES =


# translation
SOURCES = __init__.py threedi_plugin.py

PLUGINNAME = threedi_results_analysis

PY_FILES = __init__.py
# ^^^ The rest of the python files is picked up because they're in git.

UI_FILES = ui/*.ui

EXTRAS = metadata.txt icon.png

HELP = help/build/html

default: zip

test: 
	@echo "#### Python tests"
	QT_QPA_PLATFORM=offscreen pytest
	# Note: setup.cfg configures the generic options (like --cov) that are
	# passed to pytest.

docstrings:
	@echo "#### Docstring coverage report"
	python3 scripts/docstring-report.py

zip:
	@echo
	@echo "---------------------------"
	@echo "Creating plugin zip bundle."
	@echo "---------------------------"
	rm -rf /tmp/$(PLUGINNAME)
	cd /tmp; cp -r $(CURDIR) $(PLUGINNAME)
	rm -rf /tmp/$(PLUGINNAME)/tests
	rm -rf /tmp/$(PLUGINNAME)/tool_statistics/tests
	rm -rf /tmp/$(PLUGINNAME)/tool_water_balance/tests
	rm -rf /tmp/$(PLUGINNAME)/.git
	rm -rf /tmp/$(PLUGINNAME)/*.zip
	rm -rf /tmp/$(PLUGINNAME)/Docker
	rm -rf /tmp/$(PLUGINNAME)/docker-compose.yml
	rm -rf /tmp/$(PLUGINNAME)/docker-compose.override.yml
	rm -rf /tmp/$(PLUGINNAME)/__pycache__
	find /tmp/$(PLUGINNAME) -iname "*.pyc" -delete
	cd /tmp; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)


html:
	@echo
	@echo "------------------------------------"
	@echo "Building documentation using sphinx."
	@echo "------------------------------------"
	python3 scripts/generate-reference-docs.py
	cd doc; make html
	@echo "Open doc/build/html/index.html to see the documentation"


flake8:
	@echo "#### PEP8/pyflakes issues"
	@flake8 . --extend-exclude=deps
	@echo "No issues found."


beautiful:
	isort .
	black .
	flake8 .
