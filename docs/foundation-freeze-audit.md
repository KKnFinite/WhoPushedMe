# Foundation Freeze Audit

Status: UI-ready foundation freeze candidate on `feature/v04-content-foundation`.

This audit marks the point where backend/gameplay/content plumbing stops being the
default priority. New work should move into the real mobile-first product UI unless
a regression or a genuinely blocking rule violation is found.

## Covered foundation

- Account auth uses username/password/recovery key and supports multiple sessions.
- Round modes are individual and scramble; mode/course changes are setup-only.
- Exact route positions support shotgun starts, wraparound routes, repeated nine-hole
  loops, and a separate app tracking start.
- Mid-round app starts can leave earlier route positions deliberately untracked or
  keep them available for factual backfill.
- Late players join at the live hole by default. Earlier planned holes are partial,
  not missing, unless the player actually backfills them. The live UI now exposes
  an explicit backfill path.
- Shared active-hole navigation is separate from personal browsing. Past holes may
  be edited; future holes are preview-only.
- Individual scoring supports any active player entering/editing/removing another
  active player's factual score. Scramble uses one team score.
- Manual next-hole advancement never invents missing scores. Automatic advance uses
  only required active golfers/team score.
- Par tracking can be enabled or disabled before factual scoring and locks after the
  first score. Missing par is enforced server-side when par tracking is on.
- Tee behavior is mode-correct: individual per-player tees, scramble one team tee,
  with audited active-round corrections.
- Optional individual net scoring is gross-first. Missing handicap data never blocks
  play and never creates an official net placement. Scramble remains gross-only.
- Handicap Index, manual round handicap fallback, course-rating/slope storage, and
  correction audit paths are present.
- Withdraw/return, offline round-only golfers, claim/claim-undo, spectator-to-player
  promotion, persistent reactions, score challenges, scramble contributions, Bag
  events, and unanimous connected-player end-early voting are wired.
- Backfilled score entries retain factual history but suppress old derived popup
  storms and collapse into a compact historical-update presentation.
- Receipts retain event/social history and have a server-side per-participant seen
  marker with personal `YOU MISSED SOME SHIT • N` catch-up counts.
- Completed and incomplete round result semantics avoid invented totals/placements.
- Final PDF reporting follows route positions, including repeated physical holes,
  and keeps gross/net distinctions factual.
- Content controls support mini mascots, trash talk, theme toggles, vulgarity, event
  overrides, and presentation filtering.

## Verification surface

The repository currently has migrations `0001` through `0013` and focused test
coverage across API/auth, routes, results, derived events, reporting, content,
preferences, presentations, courses, handicap math, round-end behavior, browser
shell regressions, and checkpoint tooling.

The authoritative acceptance checkpoint remains:

```powershell
python tools/checkpoint.py --pull
```

Use `--migrate` only when a new migration exists.

## Intentionally deferred past UI design

These are known follow-up areas, not blockers for beginning the real UI:

- Completed-round round-only-player claim/history correction. Active-round claim
  undo exists; completed history correction should be an explicit workflow rather
  than a hidden rewrite.
- Richer round-specific presence. End-early currently uses recent valid app sessions
  as a golf-tolerant connected-player approximation.
- Broader real-browser end-to-end automation. Current regression coverage catches
  the known form/listener failures and major shell contracts, but a dedicated
  Chromium/WebKit flow suite can grow alongside UI stabilization.
- Additional content/event families and deeper analytics can be layered on without
  changing the scoring foundation.

## Freeze rule

From this point forward, do not add foundation work merely because another edge case
can be imagined. Fix backend/gameplay code before UI only when it is a demonstrated
bug, a locked-rule contradiction, a data-integrity problem, or a blocker for the
screen being designed.

The next primary phase is the actual user experience: mobile navigation, live game
screen, scoring interaction, social activity, Receipts, Bag, setup, standings,
round-end presentation, settings, and visual system.
