#!/usr/bin/env python3
#
#  annotation.py
"""
Class to model a GitHub Check Annotation.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Any, Mapping, MutableMapping

# 3rd party
import attr
from typing_extensions import Literal

__all__ = ["Annotation"]


@attr.s
class Annotation:
	"""
	Class to model a GitHub Check Annotation.
	"""

	#: The path of the file to add an annotation to. For example, ``assets/css/main.css``.
	path: str = attr.ib()

	#: The start line of the annotation.
	start_line: int = attr.ib()

	#: The end line of the annotation.
	end_line: int = attr.ib()

	#: The level of the annotation. Can be one of notice, warning, or failure.
	annotation_level: Literal["notice", "warning", "failure"] = attr.ib()

	#: A short description of the feedback for these lines of code. The maximum size is 64 KB.
	message: str = attr.ib()

	start_column: int = attr.ib(default=None)
	"""
	The start column of the annotation.
	Annotations only support start_column and end_column on the same line.
	Omit this parameter if start_line and end_line have different values.
	"""

	end_column: int = attr.ib(default=None)
	"""
	The end column of the annotation.
	Annotations only support start_column and end_column on the same line.
	Omit this parameter if start_line and end_line have different values.
	"""

	#: The title that represents the annotation. The maximum size is 255 characters.
	title: str = attr.ib(default=None)

	#: Details about this annotation. The maximum size is 64 KB.
	raw_details: str = attr.ib(default=None)

	def to_dict(self) -> MutableMapping[str, Any]:
		data = {
				"path": self.path,
				"start_line": self.start_line,
				"end_line": self.end_line,
				"annotation_level": self.annotation_level,
				"message": self.message,
				}

		for attr in [
				"start_column",
				"end_column",
				"title",
				"raw_details",
				]:
			if getattr(self, attr) is not None:
				data[attr] = getattr(self, attr)

		return data

	@classmethod
	def from_flake8json(cls, filename: str, data: Mapping[str, Any]):
		return cls(
				path=filename,
				start_line=data["line_number"],
				end_line=data["line_number"],
				start_column=data["column_number"],
				end_column=data["column_number"],
				annotation_level="warning",
				message="{code}: {text}".format_map(data)
				)

	def to_str(self) -> str:
		return (
				f"::{self.annotation_level} "
				f"file={self.path},line={self.start_line},col={self.start_column}"
				f"::{self.message}"
				)
