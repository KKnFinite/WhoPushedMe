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

## Unresolved frontend blockers

These findings describe the reviewed baseline. This checkpoint-tools commit does
**not** repair the application JavaScript.

### Form values are read after controls are disabled

In `static/app.js`, the login, registration and recovery submit handlers call
`setFormBusy(form, true)` before constructing `new FormData(form)`. The helper
disables inputs and selects. A minimal Chromium reproduction confirmed that the
same form yields its populated values before disabling, but an empty FormData
after disabling. The reviewed start-round and join-round handlers use this same
ordering and must be covered by the fix as well.

Fix at the source: capture and validate submission data before disabling controls;
restore each control's prior state afterward. Add browser tests exercising actual
submitted request bodies, not just string-presence or fake-store API tests.

### Install listeners are bound inside auth-tab switching

`switchAuthView` registers `beforeinstallprompt`, `appinstalled`, install-primary,
and install-skip handlers. Each auth-tab change adds more listeners. A restored
session can also enter `showApp` without calling `switchAuthView`, so this binding
location is not a reliable application initialization path.

Move one-time listener registration outside `switchAuthView`. Check initial
login, restored sessions, repeated auth-tab changes, and install dismissal.

## Verification boundary

The user reported 126 passing Python tests and `Applied: none` at the baseline.
That is evidence for those commands, not an end-to-end browser pass. Do not claim
that the above browser issues are resolved until the production handlers are
fixed and exercised. Do not merge to main or change production as part of this
checkpoint-tools work. Do not access or modify NeoApps.
