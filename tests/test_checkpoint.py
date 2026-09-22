"""Runner tests use fake child processes: no Git changes or database access."""
import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace

import pytest


SPEC = importlib.util.spec_from_file_location(
    "wpm_checkpoint", Path(__file__).resolve().parents[1] / "tools" / "checkpoint.py"
)
checkpoint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checkpoint)


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    python = tmp_path / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    python.parent.mkdir(parents=True)
    python.touch()
    state = {
        "branch": checkpoint.EXPECTED_BRANCH,
        "remote": "https://github.com/KKnFinite/WhoPushedMe.git",
        "status": "?? _asset_import/",
        "connection": "postgresql://test:never-print-me@example.invalid/wpm",
        "failure": None,
        "calls": [],
    }

    def run(command, **kwargs):
        state["calls"].append((command, kwargs))
        stdout = ""
        if command == ["git", "rev-parse", "--show-toplevel"]:
            stdout = str(tmp_path)
        elif command == ["git", "remote", "get-url", "origin"]:
            stdout = state["remote"]
        elif command == ["git", "branch", "--show-current"]:
            stdout = state["branch"]
        elif command[:3] == ["git", "status", "--porcelain"]:
            stdout = state["status"]
        elif command == ["git", "rev-parse", "HEAD"]:
            stdout = "a" * 40
        elif "connection-string" in command:
            stdout = state["connection"]
        failed = state["failure"] is not None and state["failure"] in command
        return SimpleNamespace(returncode=7 if failed else 0, stdout=stdout, stderr=state["connection"] if failed else "")

    monkeypatch.setattr(checkpoint.subprocess, "run", run)
    monkeypatch.setattr(checkpoint.shutil, "which", lambda *args, **kwargs: "neon")
    return tmp_path, python, state


def commands(state):
    return [command for command, _ in state["calls"]]


def test_checkpoint_uses_repo_venv_without_changing_parent_environment(workspace, capsys):
    root, python, state = workspace
    env = {"PATH": "original", "DATABASE_URL": "unrelated"}
    checkpoint.run_checkpoint(root, pull=True, env=env)
    assert ["git", "pull", "--ff-only", "origin", checkpoint.EXPECTED_BRANCH] in commands(state)
    assert [str(python), "-m", "pytest", "-q"] in commands(state)
    assert ["git", "diff", "--cached", "--check"] in commands(state)
    assert all(kwargs["cwd"] == root for _, kwargs in state["calls"])
    assert env == {"PATH": "original", "DATABASE_URL": "unrelated"}
    assert "CHECKPOINT PASSED" in capsys.readouterr().out
    assert not any("connection-string" in command for command in commands(state))


@pytest.mark.parametrize("branch", ["main", "", "feature/something-else"])
def test_wrong_branch_stops_before_pull_or_tests(workspace, branch):
    root, _, state = workspace
    state["branch"] = branch
    with pytest.raises(checkpoint.CheckpointError, match="Wrong branch"):
        checkpoint.run_checkpoint(root, pull=True, migrate=True, env={})
    assert not any("pull" in command or "pytest" in command or "connection-string" in command for command in commands(state))


def test_wrong_repository_stops_before_changes(workspace):
    root, _, state = workspace
    state["remote"] = "https://github.com/example/another-project.git"
    with pytest.raises(checkpoint.CheckpointError, match="Wrong repository"):
        checkpoint.run_checkpoint(root, pull=True, env={})
    assert not any("pull" in command for command in commands(state))


def test_missing_venv_stops_before_pull(workspace):
    root, python, state = workspace
    python.unlink()
    with pytest.raises(checkpoint.CheckpointError, match=".venv Python is missing"):
        checkpoint.run_checkpoint(root, pull=True, env={})
    assert not any("pull" in command for command in commands(state))


@pytest.mark.parametrize("status", [" M app.py", "M  app.py", "?? other-folder/"])
def test_local_changes_are_not_deleted_or_overwritten(workspace, status):
    root, _, state = workspace
    state["status"] = status
    with pytest.raises(checkpoint.CheckpointError, match="local changes need review"):
        checkpoint.run_checkpoint(root, pull=True, env={})
    assert not any("pull" in command for command in commands(state))
    assert not any("clean" in command or "reset" in command or "stash" in command for command in commands(state))


@pytest.mark.parametrize("failure, forbidden", [
    ("pull", "pytest"),
    ("migrations", "pytest"),
    ("pytest", "compileall"),
    ("compileall", "diff"),
])
def test_failed_step_stops_remaining_work(workspace, capsys, failure, forbidden):
    root, _, state = workspace
    state["failure"] = failure
    with pytest.raises(checkpoint.CheckpointError, match="failed"):
        checkpoint.run_checkpoint(root, pull=True, migrate=True, env={})
    assert not any(forbidden in command for command in commands(state))
    assert "CHECKPOINT PASSED" not in capsys.readouterr().out


def test_migration_uses_only_named_project_and_does_not_print_connection(workspace, capsys):
    root, python, state = workspace
    original = {"PATH": "original", "DATABASE_URL": "unrelated"}
    checkpoint.run_checkpoint(root, migrate=True, env=original)
    assert ["neon", "connection-string", "production", "--project-id", checkpoint.NEON_PROJECT] in commands(state)
    for command, kwargs in state["calls"]:
        if "migrations" in command or "pytest" in command:
            assert command[0] == str(python)
            assert kwargs["env"]["DATABASE_URL"] == state["connection"]
            assert kwargs["env"]["DATABASE_URL_UNPOOLED"] == state["connection"]
    assert original["DATABASE_URL"] == "unrelated"
    assert state["connection"] not in capsys.readouterr().out


@pytest.mark.parametrize("connection", ["", "warning\npostgresql://host/db", "postgresql://host/db extra"])
def test_invalid_neon_output_never_runs_migrations(workspace, connection):
    root, _, state = workspace
    state["connection"] = connection
    with pytest.raises(checkpoint.CheckpointError, match="single PostgreSQL"):
        checkpoint.run_checkpoint(root, migrate=True, env={})
    assert not any("migrations" in command for command in commands(state))


def test_neon_error_output_is_not_exposed(workspace, capsys):
    root, _, state = workspace
    state["failure"] = "connection-string"
    with pytest.raises(checkpoint.CheckpointError) as caught:
        checkpoint.run_checkpoint(root, migrate=True, env={})
    assert state["connection"] not in str(caught.value) + capsys.readouterr().out
    assert not any("migrations" in command for command in commands(state))


def test_neon_not_installed_stops_safely(workspace, monkeypatch):
    root, _, state = workspace
    monkeypatch.setattr(checkpoint.shutil, "which", lambda *args, **kwargs: None)
    with pytest.raises(checkpoint.CheckpointError, match="Neon CLI is unavailable"):
        checkpoint.run_checkpoint(root, migrate=True, env={})
    assert not any("migrations" in command for command in commands(state))


def test_missing_executable_has_redacted_error(workspace, monkeypatch):
    root, _, _ = workspace
    def missing(*args, **kwargs):
        raise FileNotFoundError("private details")
    monkeypatch.setattr(checkpoint.subprocess, "run", missing)
    with pytest.raises(checkpoint.CheckpointError, match="could not start") as caught:
        checkpoint.run_checkpoint(root, env={})
    assert "private details" not in str(caught.value)


def test_local_tests_without_pull_allow_edits(workspace):
    root, _, state = workspace
    state["status"] = " M app.py"
    checkpoint.run_checkpoint(root, env={})
    assert any("pytest" in command for command in commands(state))
    assert not any("pull" in command for command in commands(state))


@pytest.mark.parametrize("remote", [
    "https://github.com/KKnFinite/WhoPushedMe.git",
    "git@github.com:KKnFinite/WhoPushedMe.git",
    "ssh://git@github.com/KKnFinite/WhoPushedMe.git",
])
def test_repository_url_formats(remote):
    assert checkpoint.repository_matches(remote)


def test_main_returns_failure_without_false_success(monkeypatch, capsys):
    def fail(*args, **kwargs):
        raise checkpoint.CheckpointError("test failure")
    monkeypatch.setattr(checkpoint, "run_checkpoint", fail)
    assert checkpoint.main([]) == 1
    output = capsys.readouterr().out
    assert "STOPPED: test failure" in output
    assert "CHECKPOINT PASSED" not in output
