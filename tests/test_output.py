# 3rd party
import pytest
from coincidence.regressions import FileRegressionFixture, check_file_regression
from domdf_python_tools.paths import PathPlus
from flake8.main import cli  # type: ignore

bad_code = PathPlus(__file__).parent / "bad_code.py"


def test_output(file_regression: FileRegressionFixture, capsys):
	with pytest.raises(SystemExit):
		cli.main([str(bad_code), "--select", "F401,F404,F821,F701,E303", "--format", "github"])

	check_file_regression(capsys.readouterr().out, file_regression)
	assert not capsys.readouterr().err
