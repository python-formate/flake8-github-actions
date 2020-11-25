#!/usr/bin/env python3
#
#  checks.py
"""
Provides access to GitHub's Check's API.
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
from datetime import datetime

# 3rd party
import apeye
import attr
from domdf_python_tools.secrets import Secret
from requests import Response
from typing_extensions import Literal

__all__ = ["Checks"]

API_GITHUB_COM = api = apeye.RequestsURL("https://api.github.com")

common_headers = {
		"accept": "application/vnd.github.v3+json",
		"User-Agent": "github.com/domdfcoding/flake8-github-action",
		}


@attr.s
class Checks:
	"""
	Provides access to GitHub's Check's API.
	"""

	#: The owner of the repository
	owner: str = attr.ib()

	#: The name of the repository
	repository_name: str = attr.ib()

	#: The name of the check
	check_name: str = attr.ib()

	#: The commit SHA to associate the check with.
	head_sha: str = attr.ib()

	#: The token used to authenticate with the GitHub api.
	token: Secret = attr.ib(converter=Secret)

	def create_check_run(self) -> int:
		"""
		Create a check and return its ID.
		"""

		# Create the check run
		body_json = {
				"name": self.check_name,
				"head_sha": self.head_sha,
				"status": "in_progress",
				"started_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
				}

		headers = {**common_headers, "Authorization": f"token {self.token.value}"}
		url = api / "repos" / self.owner / self.repository_name / "check-runs"

		response = url.post(json=body_json, headers=headers)

		check_run_id = response.json()["id"]
		# check_suite_id = response.json()["check_suite"]["id"]

		return check_run_id

	def update_check_run(self, check_run_id: int, **kwargs) -> Response:
		r"""
		Update a check.

		:param check_run_id:
		:param \*\*kwargs:
		"""

		# Create the check run
		body_json = {"name": self.check_name, **kwargs}

		headers = {**common_headers, "Authorization": f"token {self.token.value}"}
		url = api / "repos" / self.owner / self.repository_name / "check-runs" / str(check_run_id)

		return url.patch(json=body_json, headers=headers)

	def complete_check_run(
			self,
			check_run_id: int,
			conclusion: Literal["success", "failure", "cancelled", "skipped", "timed_out", "action_required"],
			**kwargs
			) -> Response:
		r"""
		Update a check and mark it as complete.

		:param check_run_id:
		:param conclusion:
		:param \*\*kwargs:
		"""

		return self.update_check_run(
				check_run_id,
				status="completed",
				conclusion=conclusion,
				completed_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
				**kwargs,
				)
