# Development checkpoints and browser audit

Baseline reviewed: `fd61b77de7cbd35454af79a81f8a63262cb916a8` on
`feature/v04-content-foundation`, September 22, 2026.

## Checkpoint runner

From PowerShell in this repository, with Python available:

```powershell
python tools/checkpoint.py --pull
```

For an explicitly requested migration checkpoint:

```powershell
python tools/checkpoint.py --pull --migrate
```

The runner verifies the repository root, origin and development branch, uses the
repository's `.venv` interpreter, and stops at the first failed command. It never
cleans, stashes, stages, commits or pushes. Untracked `_asset_import/` is tolerated;
other local changes block a pull rather than being removed. Omit `--pull` to test
local edits. Migrations are opt-in and obtain a fresh connection for the fixed
WhoPushedMe Neon project. Captured connection output is never printed, and both
connection-variable names are set only in the child-process environment.

The Python runner does not change the calling shell's directory or keep a child
PowerShell process open. Use `powershell -NoExit` when entering PowerShell from
Command Prompt. Keep setup and verification separate from shell exit behavior.

Runner unit tests mock subprocesses: they do not access Git remotes or databases.
They do not replace application integration or browser testing.

## Frontend blockers found in the baseline

The reviewed baseline had two real browser-flow defects. They are now repaired on
the feature branch.

### Form submission capture

Authentication, round-start and round-join forms now snapshot their values before
temporary busy-state disabling. The busy-state helper also remembers and restores
each control's prior disabled state instead of blindly enabling everything.

Regression tests verify the source ordering for all affected handlers and verify
that the busy-state restoration mechanism remains present.

### Install onboarding listener binding

The PWA install listeners now bind once during application initialization instead
of being added every time the authentication tab changes. Restored sessions,
repeated auth-tab changes and install dismissal therefore share one listener set.

Regression tests assert one registration for each install listener and ensure
`switchAuthView` contains no install-listener binding.

These tests are source-level regression coverage. A future dedicated browser
suite should still exercise full DOM/network behavior in Chromium/WebKit.

## Verification boundary

The user reported 126 passing Python tests and `Applied: none` at the baseline.
That is evidence for those commands, not an end-to-end browser pass. Do not claim
that the above browser issues are resolved until the production handlers are
fixed and exercised. Do not merge to main or change production as part of this
checkpoint-tools work. Do not access or modify NeoApps.
