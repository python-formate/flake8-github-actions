#######################
flake8-github-actions
#######################

.. start short_desc

**GitHub Actions integration for flake8.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/python-formate/flake8-github-actions/workflows/Linux/badge.svg
	:target: https://github.com/python-formate/flake8-github-actions/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-formate/flake8-github-actions/workflows/Windows/badge.svg
	:target: https://github.com/python-formate/flake8-github-actions/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-formate/flake8-github-actions/workflows/macOS/badge.svg
	:target: https://github.com/python-formate/flake8-github-actions/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-formate/flake8-github-actions/workflows/Flake8/badge.svg
	:target: https://github.com/python-formate/flake8-github-actions/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-formate/flake8-github-actions/workflows/mypy/badge.svg
	:target: https://github.com/python-formate/flake8-github-actions/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/python-formate/flake8-github-actions/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/python-formate/flake8-github-actions/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/python-formate/flake8-github-actions/master?logo=coveralls
	:target: https://coveralls.io/github/python-formate/flake8-github-actions?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-formate/flake8-github-actions?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-formate/flake8-github-actions
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/flake8-github-actions
	:target: https://pypi.org/project/flake8-github-actions/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/flake8-github-actions?logo=python&logoColor=white
	:target: https://pypi.org/project/flake8-github-actions/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/flake8-github-actions
	:target: https://pypi.org/project/flake8-github-actions/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/flake8-github-actions
	:target: https://pypi.org/project/flake8-github-actions/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/python-formate/flake8-github-actions
	:target: https://github.com/python-formate/flake8-github-actions/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-formate/flake8-github-actions
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-formate/flake8-github-actions/v0.1.1
	:target: https://github.com/python-formate/flake8-github-actions/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-formate/flake8-github-actions
	:target: https://github.com/python-formate/flake8-github-actions/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2025
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/flake8-github-actions
	:target: https://pypi.org/project/flake8-github-actions/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``flake8-github-actions`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install flake8-github-actions

.. end installation

Use with GitHub Actions
----------------------------

Example workflow:

.. code-block:: yaml

	---

	name: Flake8

	on:
	  push:
	  pull_request:
	    branches: ["master"]

	jobs:
	  Run:
	    name: "Flake8"
	    runs-on: "ubuntu-18.04"

	    steps:
	      - name: Checkout 🛎️
	        uses: "actions/checkout@v2"

	      - name: Setup Python 🐍
	        uses: "actions/setup-python@v2"
	        with:
	          python-version: "3.8"

	      - name: Install dependencies 🔧
	        run: |
	          python -VV
	          python -m site
	          python -m pip install --upgrade pip setuptools wheel
	          python -m pip install flake8
	          python -m pip install flake8-github-actions

	      - name: "Run Flake8"
	        run: "flake8 --format github"


The annotations will look something like:

.. image:: https://raw.githubusercontent.com/domdfcoding/flake8-github-actions/master/example_annotations.png
