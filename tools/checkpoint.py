"""Fail-fast verification for the WhoPushedMe development branch.

From an existing PowerShell session in the repository:
    python tools/checkpoint.py --pull
    python tools/checkpoint.py --pull --migrate

This runner uses the repository's .venv interpreter without changing the parent
shell. Enter PowerShell with -NoExit separately when a persistent shell is needed.
No files are cleaned, staged, committed, or pushed by this command.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
from typing import Mapping, Sequence


EXPECTED_BRANCH = "feature/v04-content-foundation"
EXPECTED_REPOSITORY = "KKnFinite/WhoPushedMe"
NEON_PROJECT = "raspy-fire-23701779"


class CheckpointError(RuntimeError):
    """A checkpoint stopped before its remaining steps could run."""


def run_step(
    command: Sequence[str],
    *,
    label: str,
    root: Path,
    env: Mapping[str, str],
    capture: bool = False,
    announce: bool = True,
) -> str:
    """Run an argument list, never a shell string; redact captured failures."""
    if announce:
        print(f"\n{label}", flush=True)
    try:
        result = subprocess.run(
            list(command),
            cwd=root,
            env=dict(env),
            capture_output=capture,
            text=True,
            check=False,
        )
    except OSError as error:
        # Do not echo arguments, the environment, or captured connection output.
        raise CheckpointError(f"{label}: could not start the command.") from error
    if result.returncode:
        raise CheckpointError(f"{label}: failed (exit {result.returncode}).")
    return (result.stdout or "").strip() if capture else ""


def repository_matches(remote: str) -> bool:
    """Accept only credential-free HTTPS or SSH URLs for this repository."""
    return remote.strip().removesuffix(".git").rstrip("/") in {
        f"https://github.com/{EXPECTED_REPOSITORY}",
        f"git@github.com:{EXPECTED_REPOSITORY}",
        f"ssh://git@github.com/{EXPECTED_REPOSITORY}",
    }


def verify_repository(root: Path, env: Mapping[str, str]) -> None:
    top = run_step(
        ["git", "rev-parse", "--show-toplevel"],
        label="Check repository directory", root=root, env=env, capture=True,
    )
    if Path(top).resolve() != root.resolve():
        raise CheckpointError("Run the checkpoint from the WhoPushedMe repository copy.")
    remote = run_step(
        ["git", "remote", "get-url", "origin"],
        label="Check repository identity", root=root, env=env, capture=True,
    )
    if not repository_matches(remote):
        raise CheckpointError("Wrong repository. Expected KKnFinite/WhoPushedMe.")
    branch = run_step(
        ["git", "branch", "--show-current"],
        label="Check development branch", root=root, env=env, capture=True,
    )
    if branch != EXPECTED_BRANCH:
        raise CheckpointError(f"Wrong branch. Expected {EXPECTED_BRANCH}.")
    print(f"Branch: {branch}", flush=True)


def load_migration_environment(root: Path, env: Mapping[str, str]) -> dict[str, str]:
    """Resolve only this project's Neon connection; never print its output."""
    neon = shutil.which("neon", path=env.get("PATH"))
    if not neon:
        raise CheckpointError("Neon CLI is unavailable; migration was not run.")
    connection = run_step(
        [neon, "connection-string", "production", "--project-id", NEON_PROJECT],
        label="Load WhoPushedMe database connection", root=root, env=env,
        capture=True,
    )
    if (
        not connection.startswith(("postgresql://", "postgres://"))
        or any(character.isspace() for character in connection)
    ):
        raise CheckpointError("Neon did not return a single PostgreSQL connection URL.")
    result = dict(env)
    # Both names deliberately point to this project for the child processes.
    # Never reuse an unrelated DATABASE_URL inherited from another project.
    result["DATABASE_URL_UNPOOLED"] = connection
    result["DATABASE_URL"] = connection
    return result


def run_checkpoint(
    root: Path,
    *,
    pull: bool = False,
    migrate: bool = False,
    env: Mapping[str, str] | None = None,
) -> None:
    root = root.resolve()
    child_env = dict(os.environ if env is None else env)
    verify_repository(root, child_env)
    python = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.is_file():
        raise CheckpointError("Repository .venv Python is missing; nothing was pulled.")
    child_env["VIRTUAL_ENV"] = str(root / ".venv")
    child_env["PATH"] = str(python.parent) + os.pathsep + child_env.get("PATH", "")

    if pull:
        status = run_step(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            label="Check local changes before pull", root=root, env=child_env,
            capture=True,
        )
        if any(line != "?? _asset_import/" for line in status.splitlines()):
            run_step(
                ["git", "status", "--short"], label="Local changes need review",
                root=root, env=child_env,
            )
            raise CheckpointError("Pull stopped: local changes need review; nothing was deleted.")
        run_step(
            ["git", "pull", "--ff-only", "origin", EXPECTED_BRANCH],
            label="Pull development branch", root=root, env=child_env,
        )
        # Recheck before running any code from the updated working tree.
        verify_repository(root, child_env)

    head = run_step(
        ["git", "rev-parse", "HEAD"], label="Read verified revision",
        root=root, env=child_env, capture=True,
    )
    print(f"HEAD: {head}", flush=True)
    if migrate:
        child_env = load_migration_environment(root, child_env)
        run_step(
            [str(python), "-m", "migrations"], label="Run migrations",
            root=root, env=child_env,
        )
    for arguments, label in (
        ([str(python), "-m", "pytest", "-q"], "Run tests"),
        ([str(python), "-m", "compileall", "-q", "app.py", "who_pushed_me", "tools"], "Compile Python"),
        (["git", "diff", "--check"], "Check working-tree whitespace"),
        (["git", "diff", "--cached", "--check"], "Check staged whitespace"),
        (["git", "status", "--short"], "Final working-tree status"),
    ):
        run_step(arguments, label=label, root=root, env=child_env)
    print("\nCHECKPOINT PASSED", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pull", action="store_true", help="Fast-forward only; refuse unexpected local changes.")
    parser.add_argument("--migrate", action="store_true", help="Run migrations on the configured WhoPushedMe Neon project.")
    args = parser.parse_args(argv)
    try:
        run_checkpoint(Path(__file__).resolve().parents[1], pull=args.pull, migrate=args.migrate)
    except CheckpointError as error:
        print(f"\nSTOPPED: {error}", flush=True)
        return 1
    except KeyboardInterrupt:
        print("\nSTOPPED: interrupted.", flush=True)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
