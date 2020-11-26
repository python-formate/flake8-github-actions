#!/usr/bin/env python3
#
#  __main__.py
"""
CLI entry point.
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

# stdlib
import sys
from typing import Union

# 3rd party
import click
from apeye import URL

__all__ = ["main"]

# 3rd party
from consolekit import CONTEXT_SETTINGS

token_var = "GITHUB_TOKEN"


@click.option(
		"-t",
		"--token",
		type=click.STRING,
		help=(
				"The token to authenticate with the GitHub API. "
				f"Can also be provided via the '{token_var}' environment variable."
				),
		envvar=token_var,
		required=True,
		)
@click.option(
		"-r",
		"--repo",
		type=click.STRING,
		default=None,
		help="The repository name (in the format <username>/<repository>) or the complete GitHub URL.",
		)
@click.option(
		"--annotate-only",
		is_flag=True,
		default=False,
		help="Only add the annotations (exit 0 regardless of flake8 output).",
		)
@click.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True, **CONTEXT_SETTINGS})
@click.pass_context
def main(ctx: click.Context, token: str, repo: Union[str, URL, None] = None, annotate_only: bool = False,):
	"""
	Run flake8 and add the errors as annotations on GitHub.
	"""

	# this package
	from flake8_github_action import action

	response, ret = action(token, repo, *ctx.args)

	# if response.status_code == 200:
	# 	sys.exit(0)

	if annotate_only:
		sys.exit(0)
	else:
		sys.exit(ret)


if __name__ == "__main__":
	sys.exit(main(obj={}))
