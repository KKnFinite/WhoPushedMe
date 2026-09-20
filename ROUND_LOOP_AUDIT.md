# Round Loop Audit

This file records the functional acceptance rules for the v0.4 round loop.
The current HTML/CSS is scaffolding only. Visual approval happens separately.

## First-login install onboarding
- After account creation/login setup, show a one-time device-specific install screen before Home unless the app is already running in standalone/PWA mode.
- The screen must explain that installing to the Home Screen takes only a few seconds and makes Who Pushed Me?! behave like a normal downloaded app.
- Tone should be mocking/playful, not technical or apologetic.
- Installation is optional; the user can skip and continue in the browser.
- Do not repeatedly nag on every launch. Store dismissal/seen state per device and keep a manual `INSTALL THE APP` entry in Settings.
- Android/Chromium:
  - when an install prompt is available, show a primary install button that triggers the browser's PWA install flow.
  - otherwise show concise device/browser instructions.
- iPhone/iPad Safari:
  - show Share -> Add to Home Screen -> Add instructions.
  - explain that iOS does not provide the same one-tap install prompt as Android.
- If the app is already installed/standalone, skip this onboarding automatically.
- Suggested copy direction:
  - headline: `TAKE 10 SECONDS. MAKE IT AN ACTUAL APP.`
  - body: `Yeah, you can keep opening this in a browser like a psychopath. Or add it to your Home Screen and let it behave like the app we built.`
  - primary CTA: `FINE. INSTALL THE DAMN THING.`
  - skip CTA: `I ENJOY MAKING THINGS HARDER.`

## Account and entry
- A valid authenticated account can create or join a round.
- New rounds begin in `setup`.
- A round code is four digits and is only unique among live setup/active rounds.
- Reused historical codes resolve within the authenticated golfer's own round history.
- Spectators can join setup or active rounds.

## Spectator mode
- A spectator joins the round, not a specific hole.
- Spectators never choose a starting hole, tracked-from hole, or scoring window.
- Joining an active round as a spectator immediately opens the live spectator view at the round's current state.
- As the group advances, the spectator follows the live round and sees events unfold in real time.
- Spectators can view live scores, banter, minis, score responses, Bag activity, contributions, standings, and other shared round events as they occur.
- Spectators may use allowed social actions such as score responses, reactions, and Open Mic.
- Spectators never acquire score, par, tee, contribution, completion, or hole-advancement obligations merely by joining.
- Any ability to browse older holes or Receipts is viewing history only and does not change what hole the spectator is "on."

## Lobby
- Any player may start the round.
- Spectators may not start it.
- Course rounds with tee data require every player to choose a tee before start.
- Free Play does not require a tee.

## Round route and starting mid-round
- A round is defined by an explicit play order, not by assuming hole 1 through hole 18.
- Setup supports any starting hole.
- A full 18 wraps after hole 18 back to hole 1 until all 18 holes in the route are played.
- Setup may instead choose an explicit ending hole, including an ending hole after wraparound.
- Examples:
  - start 4 / full 18 -> 4-18, then 1-3
  - start 4 / end 18 -> 4-18
  - start 4 / end 1 -> 4-18, then 1
  - start 15 / end 4 -> 15-18, then 1-4
- Mid-round adoption distinguishes the intended round route from the hole where Who Pushed Me tracking begins.
- Earlier holes may be backfilled, left untracked, or explicitly filled as assumed par.
- Untracked holes do not count toward totals, standings, streaks, completion, or performance awards.
- Assumed-par holes must be stored as assumed, never silently treated as factual scores.
- Backfilling old holes never moves the shared live hole backward.
- Completion requires scores only for the holes that are part of the tracked route for the relevant player/team.
- Individual players may have different tracked-from holes if somebody joins an already-active round late.

## Live scoring
- Score, par, and shared-hole mutations are only allowed while status is `active`.
- Spectators cannot change score, par, or shared current hole.
- Old-hole score edits never move the shared current hole backward.
- The shared current hole cannot be moved backward through the API.
- A score report creates a factual score event and canonical content event.
- A later score edit creates a new score-push event. It does not replace the original event.
- Score outcomes classify to ace/albatross/eagle/birdie/par/bogey/double/triple/quad-plus when par is known.
- Score-specific banter does not require a mini mascot.

## Score interaction
- Responses are optional.
- Every recorded score event can receive responses from any participant, including spectators.
- Canned responses include bullshit, cheater, lucky, nice, blame, and random trash talk.
- Custom responses are supported.
- A response links to the exact score event it reacted to.
- A score push creates a fresh response opportunity while preserving replies to the old score event.

## Scramble
- Team score is the only required score.
- Contribution attribution is optional.
- Any participant may attribute scramble contributions during an active round.
- Contribution attribution never changes the actual score.
- Score responses remain available in addition to contribution attribution.
- A participant can be blamed for a scramble score without making that blame factual scoring data.

## Bag of Bullshit
- Available only during an active round.
- Players can use all Bag actions.
- Spectators are limited to Open Mic and reactions.
- Bag actions never block scoring or hole advancement.

## Derived moments
- Derived moments are presentation/events, not score mutations.
- Supported moments include:
  - first birdie
  - first eagle
  - back-to-back birdies
  - 3+ birdie streak
  - 3+ bogey-or-worse streak
  - blow-up hole
  - new leader
  - tied lead
  - lost lead
  - entered last
  - escaped last
- Extending an existing streak does not repeatedly fire the same streak-start event.

## Throw in the towel / withdrawal
- Towel actions are always explicit and require confirmation; the app never ends participation automatically.
- Late-round towel taunts are presentation only and are based on holes remaining in the defined route, not literal hole numbers.
- Late-round taunt tone may vary by score-to-par:
  - suffering: meaningfully over par
  - hanging around: near par
  - annoyingly competent: under par
- Scramble:
  - an individual player may throw in the towel without ending the team round.
  - the player remains in the round as an inactive/spectating participant for social actions.
  - their earlier scramble contributions remain preserved.
  - their personal towel state is comedy/history metadata, not a scoring result.
  - they may return before the round ends; returning becomes its own event and does not erase the original quit event.
- Individual play:
  - a player towel throw is a real DNF/withdrawal state.
  - future holes are no longer required from that player.
  - the withdrawn player is excluded from normal winner/place calculations.
  - all prior scores and events remain preserved.
  - the withdrawn player can remain as a spectator/social participant.
  - the player may return before the round ends; if they return, normal scoring requirements resume from the return point unless earlier missing holes are backfilled.
- Optional surrender reason may be recorded and can be used in banter, Receipts, history, and the Final Damage Report.
- A whole group may explicitly end the round early; the report must clearly distinguish early termination from a normally completed round.
- Towel events and late-round taunts must never be required to continue or finish a round.

## Completion
- Contributions, Bag actions, reactions, and score responses are never required to finish.
- Individual completion requires every player to have a score on every hole.
- Scramble completion requires one team score on every hole.
- Completed rounds freeze score/par/shared-hole mutation unless explicitly resumed.
- Round-end presentations are selected and stored server-side.

## Round-end routing
- Two-player individual: winner / head-to-head loser.
- Three-player individual: winner / not-last / dead-last.
- Four-player individual: winner / not-last / not-last / dead-last.
- Tie-aware events use co-winner, tied-middle, or tied-last.
- Scramble uses one group `round.end.scramble.complete` presentation.

## Receipts and Final Damage Report
- Receipts preserve factual events and the server-selected presentation.
- The PDF is generated on demand and is not stored in Neon.
- The PDF includes every banter and mini mascot actually rendered for that viewer during the round.
- Repeated banter/minis remain repeated if they fired multiple times.
- Custom score replies, Bag text, and Open Mic text are preserved.
- Individual PDFs include personal hole-by-hole performance plus final standings.
- Scramble PDFs include team performance plus contribution audit.
- PDF download uses the permanent round UUID, not the reusable four-digit round code.

## UI status
- Current UI is functional scaffolding only.
- Final design requires explicit approval before merge to main.
- First approval sequence: Home -> Lobby -> Live Scorecard.
