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

## Live catch-up / event history
- The live scorecard remains the primary interaction surface. Social/history content must never block scoring, hole movement, or normal play.
- New score/social events may surface briefly as lightweight transient cards with optional reactions/actions, then collapse automatically.
- Every factual event, selected banter, selected mini, reaction, custom response, Bag action, contribution, blame event, derived moment, and score edit remains available in a persistent live history view.
- The live history entry point should use an on-brand unread label such as `YOU MISSED SOME SHIT • N`, with rotating equivalent phrases allowed.
- Each participant/spectator should have a per-round last-seen event marker so unread counts are personal, not global.
- Opening catch-up marks events seen for that viewer without altering the underlying event history.
- A spectator joining an active round immediately sees the live state and can open the existing history to catch up on what happened before they arrived.
- History should visually distinguish factual golf events, app commentary/mascot events, and group social bullshit.
- History may be grouped by hole/route position and should preserve exact chronological order within each group.
- Old score events remain readable after a score push; replies stay attached to the exact score event they answered.
- Users may respond later from history where appropriate; missing a transient card never removes the opportunity to participate.
- Catch-up headers/empty states may roast the viewer. Example directions include:
  - `YOU MISSED SOME SHIT.`
  - `WELCOME BACK. THE SCORECARD GOT WORSE.`
  - `LOOK AWAY FOR TWO HOLES AND THIS IS WHAT HAPPENS.`
  - `THESE IDIOTS DID THINGS WHILE YOU WEREN'T LOOKING.`
  - `CATCH UP BEFORE SOMEBODY CHANGES THEIR STORY.`
- Catch-up roasting is presentation only and never changes golf state.

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

## Bag of Bullshit vs reactions
- Live reactions respond to an existing event; Bag of Bullshit creates a new social golf event that the app could not know about on its own.
- Reactions belong on the event they answer and remain linked to that exact score/social event in Receipts.
- Bag actions should be fast, optional, and return the user to the live scorecard immediately.
- Core Bag actions:
  - `CALL SOMEONE OUT`: report a screw-up such as water, OB, lost ball, tree, bunker, shank, slice, hook, topped, chunked, bladed, whiff, penalty, mulligan, foot wedge, wrong club, way short, way long, slow play, missed short putt, three-putt, or lip-out.
  - `NICE FUCKING SHOT`: report a good drive, approach, recovery, bunker shot, putt, or long putt.
  - `CALL YOUR SHOT`: record a golfer's own prediction/challenge before the result.
  - `YOU WON'T`: challenge another golfer before an attempted shot/action.
  - `EXCUSE DEPARTMENT`: record excuses such as clubs, wind, weather, bad lie, green, noise, alcohol, hangover, pace, or custom text.
  - `OPEN MIC`: freeform comment tied to the live round/hole.
- Generic `Laugh / Bullshit / Applause` controls should not be primary Bag actions. They belong as contextual reactions on live events and in Receipts.
- Any Bag event can itself receive contextual reactions later.
- Bag activity is social history only; it never changes score, par, route, standings, contribution truth, or completion requirements.
- Spectators may create only the Bag/social actions allowed by spectator permissions; they still never mutate golf state.
- Mental model:
  - Scorecard records golf.
  - Automatic events interpret golf.
  - Reactions answer an existing event.
  - Bag of Bullshit reports the stuff the app cannot know.
  - Receipts preserves everything.

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

## Standings and score display
- Display golf scoring in the familiar professional-leaderboard style: cumulative strokes plus score relative to par when the player's tracked scorecard is complete for the route being counted.
- Example complete display: `82  |  +10`.
- Relative-to-par is always calculated only from holes that legitimately count for that player/team; never invent missing strokes.
- If a player has missing score entries for holes that should count, do not show a misleading cumulative stroke total.
- Instead show the relative-to-par result from the recorded holes plus an explicit incomplete indicator.
- Example incomplete display: `+6  |  INCOMPLETE • 6/9 SCORED` or `+6  |  INCOMPLETE • 12/18 SCORED`, depending on that player's required route.
- Use `THRU N` only when the recorded holes form a true contiguous progression in that player's route; otherwise use `N/M SCORED`.
- Holes intentionally outside a player's tracked route (for example, a legitimate late join) are not treated as missing scores.
- Never hardcode 18 as the denominator. The denominator is the number of holes that actually belong to that player/team's required tracked route.
- A planned 9-hole round uses 9. A custom route uses its actual route length. A wrapped shotgun route uses the number of holes in that route.
- If the whole group explicitly ends the round early, holes beyond the agreed stopping point are removed from the effective required route; they are not shown as missing scores.
- A group-ended-early round must still be visibly labeled as ended early rather than presented as a normal full-route completion.
- A player who has completed every hole in their defined tracked route may show both cumulative strokes and relative-to-par for that route, even when that route is shorter than 18 holes.
- Assumed-par holes, when explicitly chosen, count toward displayed totals but must remain identifiable as assumed in history/Receipts/PDF.

## Placement eligibility
- Official individual placement is based on the player's effective required route, not a hardcoded 18 holes.
- A planned 9-hole round, custom route, wrapped shotgun route, or whole-group early stop can all produce valid official standings when the remaining active players are being compared over the same effective route.
- If every active individual golfer shares the same effective route and has all required scores, normal placement applies even when that route is shorter than 18 holes.
- A legitimate late joiner with a shorter personal route is labeled `PARTIAL ROUND` and is not ranked against golfers who played a different effective route.
- A player with missing required scores is labeled `INCOMPLETE` and is not eligible for official placement until those required scores are filled.
- An individual player who throws in the towel is labeled `DNF` / `WITHDREW` and is excluded from normal winner/place calculations.
- If the whole group ends early together, that shared stopping point becomes the effective route end for the golfers still active; those golfers can still receive official placement over the common played route, while the round remains visibly labeled `ENDED EARLY`.
- Scramble has one team result. A team that ends early keeps its score and score-to-par over the played route, but the report must clearly label the round as ended early.

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

## Experience direction: social app x video game
- The product should feel like a cross between a live social-media feed and a lightweight multiplayer video game, not like a traditional golf scorecard with jokes bolted on.
- The scorecard remains the authoritative game-state layer, but the live experience should constantly surface social energy around it.
- Social-app behaviors:
  - personal unread counts
  - live event feed / Receipts
  - reactions attached to exact events
  - comments / Open Mic
  - mentions/targets through callouts, blame, praise, and challenges
  - catch-up after time away
  - persistent personal/history profiles later through Previous Disasters / Known Offenders
- Video-game behaviors:
  - clear round progress and current objective
  - event-driven popups for birdies, blowups, lead changes, streaks, and other moments
  - lightweight rewards/taunts/awards instead of sterile notifications
  - dramatic but nonblocking transitions
  - persistent player state such as score-to-par, DNF/towel status, contribution history, and round role
  - end-of-round recap that feels like a results screen, not a spreadsheet
- Every major action should create immediate feedback: motion, sound-ready hooks, banter, mascot, reaction opportunity, or a visible state change.
- The app should feel alive even when the user is not entering scores; spectators and inactive players should still have meaningful social interaction.
- Avoid dense permanent control panels. Use layered interaction: game state always visible, transient event cards for live moments, and Receipts for permanent social history.
- Humor and personality are part of the interaction system, not decorative copy placed around conventional forms.

## Edge-case review discipline
- Before implementing any major round-state or UI-flow change, explicitly review edge cases and unresolved decisions rather than assuming the happy path.
- Questions should be asked when a rule can materially change scoring truth, route semantics, standings, completion, history, spectator behavior, or report output.
- Route modeling must distinguish course hole number from play-order position so shotgun starts, wraparound, shortened routes, and repeated physical holes can be represented correctly.
- State changes that deserve explicit edge-case review include:
  - joining an active round as player vs spectator
  - changing participant role mid-round
  - starting late, backfilling, and assumed-par entries
  - withdrawal, return, and group early termination
  - score edits before/after completion or resume
  - route wraparound and repeated physical holes
  - incomplete vs partial vs DNF placement
  - multi-device unread/catch-up state
  - course/tee/par differences that affect score-to-par
- When an ambiguity is discovered, record the chosen behavior in this audit before building around it.

## UI status
- Current UI is functional scaffolding only.
- Final design requires explicit approval before merge to main.
- First approval sequence: Home -> Lobby -> Live Scorecard.
