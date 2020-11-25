#!/usr/bin/env python3
#
#  __init__.py
"""
GitHub Action to run flake8.
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
import json
from typing import List, Tuple, Union

# 3rd party
import click
import dulwich.errors
from apeye import URL
from domdf_python_tools.iterative import chunks
from domdf_python_tools.secrets import Secret
from dulwich.repo import Repo
from requests import Response

# this package
from flake8_github_action.annotation import Annotation
from flake8_github_action.checks import Checks
from flake8_github_action.flake8_app import Application

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["action"]


def action(
		token: Union[str, Secret],
		repo: Union[str, URL, None] = None,
		*args,
		) -> Tuple[Response, int]:
	r"""
	Action!

	:param token: The token to authenticate with the GitHub API.
	:param repo: The repository name (in the format <username>/<repository>) or the complete GitHub URL.
	:param \*args: flake8 command line arguments.
	"""

	if not isinstance(token, Secret):
		token = Secret(token)

	dulwich_repo = Repo('.')

	if repo is None:
		try:
			config = dulwich_repo.get_config()
			repo = URL(config.get(("remote", "origin"), "url").decode("UTF-8"))
		except dulwich.errors.NotGitRepository as e:
			raise click.UsageError(str(e))

	elif not isinstance(repo, URL):
		repo = URL(repo)

	if repo.suffix == ".git":
		repo = repo.with_suffix('')

	repo_name = repo.name

	# first case is for full url, second for github/hello_world
	github_username = repo.parent.name or repo.domain.domain

	check = Checks(
			owner=github_username,
			repository_name=repo_name,
			check_name="Flake8",
			head_sha=dulwich_repo.head().decode("UTF-8"),
			token=token.value,
			)

	# check_run_id = check.create_check_run()
	check_run_id = check.find_run_for_action()

	flake8_app = Application()
	flake8_app.run(args)
	flake8_app.exit()

	annotations: List[Annotation] = []

	json_annotations = json.loads(flake8_app.formatter.output_fd.getvalue()).items()
	for filename, raw_annotations in json_annotations:
		annotations.extend(Annotation.from_flake8json(filename, ann) for ann in raw_annotations)

	# Github limits updates to 50 annotations at a time
	annotation_chunks = list(chunks(annotations, 50))

	if flake8_app.result_count:
		conclusion = "failure"
		ret = 1
	else:
		conclusion = "success"
		ret = 0

	for chunk in annotation_chunks[:-1]:
		check.update_check_run(
				check_run_id,
				conclusion=conclusion,
				output={
						"title": "Flake8 checks",
						"summary": "Output from Flake8",
						"annotations": [a.to_dict() for a in chunk],
						},
				)

	return check.complete_check_run(
			check_run_id,
			conclusion="success",  # TODO: reflect flake8 output
			output={
					"title": "Flake8 checks",
						"summary": "Output from Flake8",
					"annotations": [a.to_dict() for a in annotation_chunks[-1]],
					},
			), ret




