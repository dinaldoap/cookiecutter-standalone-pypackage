import filecmp
import subprocess as sp
from filecmp import dircmp
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from cookiecutter_python_vscode_github import __main__ as main

_PROJECT_ROOT = Path(__file__).parent.parent


def test_main():
    with pytest.raises(SystemExit, match="0"):
        main.main(["--help"])


def test_show():
    expected_template_path = _PROJECT_ROOT.joinpath("cookiecutter_python_vscode_github")
    actual_template_path = Path(_show())

    assert expected_template_path == actual_template_path


def test_bake(tmp_path: Path, monkeypatch: MonkeyPatch):
    template_dir = _show()
    monkeypatch.chdir(tmp_path)
    sp.run(["cookiecutter", template_dir, "--no-input"], check=True)
    ignore = filecmp.DEFAULT_IGNORES + [
        "pyproject.toml",
        "requirements-dev.txt",
        "__main__.py",
        "test_main.py",
    ]
    diff = dircmp(
        tmp_path.joinpath("cookiecutter_python_vscode_github"),
        _PROJECT_ROOT,
        ignore=ignore,
    )
    diff_list = _list_diff_files(diff)
    assert [] == list(
        diff_list
    ), "Diff list is not empty. Check diff list content to fix differences between template and project."


def _show():
    return sp.run(
        ["cookiecutter-python-vscode-github"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def _list_diff_files(dcmp):
    for name in dcmp.diff_files:
        yield "diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right)
    for sub_dcmp in dcmp.subdirs.values():
        yield from _list_diff_files(sub_dcmp)
