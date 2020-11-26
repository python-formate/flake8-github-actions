#!/usr/bin/env python3
#
#  flake8_app.py
"""
Subclass of Flake8's ``Application``.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#
#  "Application" based on Flake8
#  Copyright (C) 2011-2013 Tarek Ziade <tarek@ziade.org>
#  Copyright (C) 2012-2016 Ian Cordasco <graffatcolmingov@gmail.com>
#  MIT Licensed
#
#  "GitHubFormatter" based on https://gitlab.com/pycqa/flake8-json
#  Copyright (C) 2017-2018 Ian Stapleton Cordasco <graffatcolmingov@gmail.com>
#  MIT Licensed
#

# stdlib
from functools import partial
from gettext import ngettext
from typing import Optional, Tuple, Type

# 3rd party
import click
import flake8.main.application  # type: ignore
from flake8.formatting.base import BaseFormatter  # type: ignore
from typing_extensions import NoReturn

__all__ = ["Application", "GitHubFormatter"]

_error = partial(ngettext, "error", "errors")
_file = partial(ngettext, "file", "files")


class Application(flake8.main.application.Application):
	"""
	Subclass of Flake8's ``Application``.
	"""

	def exit(self) -> NoReturn:
		"""
		Handle finalization and exiting the program.

		This should be the last thing called on the application instance.
		It will check certain options and exit appropriately.
		"""

		if self.options.count:
			if True:
				files_checked = self.file_checker_manager.statistics["files"]
				files_with_errors = self.file_checker_manager.statistics["files_with_errors"]
				if self.result_count:
					click.echo(
							f"Found {self.result_count} {_error(self.result_count)} "
							f"in {files_with_errors} {_file(files_with_errors)} "
							f"(checked {files_checked} source {_file(files_checked)})"
							)
				else:
					click.echo(f"Success: no issues found in {files_checked} source {_file(files_checked)}")

		if self.options.exit_zero:
			raise SystemExit(self.catastrophic_failure)
		else:
			raise SystemExit((self.result_count > 0) or self.catastrophic_failure)

	def report_errors(self) -> None:
		"""
		Report all the errors found by flake8 3.0.

		This also updates the :attr:`result_count` attribute with the total
		number of errors, warnings, and other messages found.
		"""

		flake8.main.application.LOG.info("Reporting errors")

		files_with_errors = results_reported = results_found = 0

		for checker in self.file_checker_manager._all_checkers:
			results_ = sorted(checker.results, key=lambda tup: (tup[1], tup[2]))
			filename = checker.display_name

			with self.file_checker_manager.style_guide.processing_file(filename):
				results_reported_for_file = self.file_checker_manager._handle_results(filename, results_)
				if results_reported_for_file:
					results_reported += results_reported_for_file
					files_with_errors += 1

			results_found += len(results_)

		results: Tuple[int, int] = (results_found, results_reported)

		self.total_result_count, self.result_count = results
		flake8.main.application.LOG.info(
				"Found a total of %d violations and reported %d",
				self.total_result_count,
				self.result_count,
				)

		self.file_checker_manager.statistics["files_with_errors"] = files_with_errors

	def make_formatter(self, formatter_class: Optional[Type[BaseFormatter]] = None) -> None:
		"""
		Initialize a formatter based on the parsed options.
		"""

		self.formatter = GitHubFormatter(self.options)


class GitHubFormatter(BaseFormatter):

	def write_line(self, line):
		"""
		Override write for convenience.
		"""
		self.write(line, None)

	def start(self):
		super().start()
		self.files_reported_count = 0

	def beginning(self, filename):
		"""
		We're starting a new file.
		"""

		self.reported_errors_count = 0

	def finished(self, filename):
		"""
		We've finished processing a file.
		"""

		self.files_reported_count += 1

	def format(self, violation):
		"""
		Format a violation.
		"""

		if self.reported_errors_count == 0:
			self.write_line(violation.filename)

			self.write_line(
					f"::warning "
					f"file={violation.filename},line={violation.line_number},col={violation.column_number}"
					f"::{violation.code}: {violation.text}"
					)

		self.reported_errors_count += 1
