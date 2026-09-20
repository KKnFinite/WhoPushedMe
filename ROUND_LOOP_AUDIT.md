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

## Smooth claim-on-join flow
- When an authenticated user enters a round code, the app must first check that round for any unclaimed round-only player identities before creating a new participant.
- If unclaimed players exist, show a fast claim step such as `ARE YOU ALREADY IN THIS MESS?` with the listed unclaimed golfers.
- The user may tap `THAT'S ME` on the correct golfer and immediately attach their account to that existing participant.
- Claiming preserves the exact participant record and all prior scores, edits, reactions, callouts, contributions, towel/DNF state, standings context, Receipts, and report history.
- If none of the listed golfers is them, they continue with the normal new-player or spectator join flow.
- If multiple unclaimed golfers share the same display name, show enough round context to distinguish them, such as tee, tracked-from hole, or who added them.
- A claimed participant cannot be claimed by another account unless an explicit future unlink/recovery flow is used.
- During an active round, a newly claimed participant may use a simple `UNDO CLAIM` action if they selected the wrong round-only golfer.
- Undoing a mistaken claim detaches the account from that participant without deleting or rewriting any scores, reactions, contributions, Receipts, or report history.
- After undo, the participant returns to unclaimed round-only status and the user returns to the claim/new-player flow.
- If the user has already created new golf-state events after claiming, the app should warn before undoing so the user understands those actions remain attributed to their account while the guest participant history remains intact.
- Once the round is completed, claim changes should require an explicit account/history correction flow rather than a casual undo button.
- The claim step should be fast and nontechnical; do not force account-linking terminology on the golfer.

## Offline / no-app players
- Any active player may add another golfer to the round even when that golfer cannot access the app on their own device.
- An offline/no-app golfer is treated as a full player for golf state: route, tee selection, scores, standings, placement, DNF/withdrawal, awards, Receipts, and Final Damage Report.
- Other active players may enter, edit, and remove scores for that golfer exactly as they can for any other player.
- Shared live events, banter, minis, callouts, blame, praise, and score reactions may still target the offline golfer and remain visible to everyone who is connected.
- The group presentation layer may use special offline/no-app banter when a golfer is being scored by others because they are not connected.
- Offline-player jokes should target the situation, not invent a factual reason. Approved themes include being bad with technology, forgetting how phones/apps work, needing somebody else to operate the tools, or being mysteriously absent from the digital world.
- Examples of tone:
  - `MIKE'S PHONE HAS LEFT THE CHAT. HIS BOGEY HAS NOT.`
  - `SOMEBODY ENTER MIKE'S SCORE. TECHNOLOGY HAS DEFEATED HIM AGAIN.`
  - `MIKE IS CURRENTLY PARTICIPATING THROUGH A HUMAN PROXY.`
  - `APPARENTLY USING A PHONE WAS THE HARDEST SHOT OF THE DAY.`
  - `WE'VE ASSIGNED MIKE A DESIGNATED ADULT WITH A WORKING BATTERY.`
- Do not state a specific cause such as dead battery, forgotten phone, or no signal unless that reason was actually supplied; use generic technology/absence jokes otherwise.
- What the offline golfer lacks is only a personal client/account delivery surface: no personalized unread count, no private/personalized presentation variant delivered to their own screen, and no direct social actions from them unless they later connect.
- Device/app absence must not downgrade the golfer to spectator or guest scoring rules.
- The participant model should support either an account-linked golfer who is simply offline or a round-only golfer identity when no account exists.
- If a round-only golfer later connects or is linked to an account, that link must not duplicate their participant, scores, history, reactions targeting them, or placement.
- A round-only golfer may create an account later and explicitly claim the existing round participant identity.
- Claiming attaches the existing participant record to the new/existing account rather than creating a second participant.
- All previously recorded holes, score revisions, reactions, callouts, blame, praise, contributions, DNF/towel events, standings context, Receipts, awards, and Final Damage Report history tied to that participant remain intact and become part of the claimed account's round history.
- If the claim happens while the round is still active, the golfer immediately continues from the same participant state and can use their own device for future scoring/social actions.
- Historical score ownership is not rewritten: Receipts still show which other player originally entered or edited scores on the golfer's behalf.
- A round-only participant can be claimed only once. The eventual claim/verification flow must prevent one account from taking another golfer's participant history.

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

## Par availability and entry
- Par is all-or-nothing for round-level score-to-par reporting.
- If every counted hole in the effective route has a known par, show normal cumulative score-to-par and allow par-based round summaries.
- If any counted hole lacks par, do not show cumulative round score-to-par at all; treat par as unavailable for that round until the missing pars are supplied.
- Course/API data should populate hole par and tee data whenever available.
- When API/course par is unavailable or incomplete, players may choose to enter all hole pars during setup or enter them progressively hole by hole during play.
- Hole-level birdie/par/bogey/etc. classification is only available once that hole's par is known.
- Adding the missing pars later may activate cumulative score-to-par and derived par-based summaries for the round; it must not fabricate historical score events that were not originally classifiable unless we explicitly add a backfill/reclassification feature later.
- Free Play follows the same rule: either supply all counted pars and use par-based scoring, or play without par-based round scoring.

## Tee and par rules
- Individual play may use different tees per player; each player's score-to-par must use the par associated with that player's selected tee when course data varies by tee.
- Scramble uses one explicitly selected scoring tee for the entire team.
- The scramble team's par, score-to-par, standings/result math, and report output all use that one team scoring tee.
- Individual players may physically hit from different tees during a scramble if the group wants, but that does not change the scoring tee unless the team explicitly changes it through a supported edit flow.
- Any scoring-tee change after scores exist must create a permanent history event and recompute affected score-to-par values rather than silently rewriting history.

## Par changes after scoring
- A par edit after one or more scores already exist must never rewrite or replace the original score event, its banter, mascot, reactions, or replies.
- The original event remains historically true to what the app knew at the time. Example: a score that fired Bogey banter under par 4 keeps that Bogey banter even if the hole is later corrected to par 5.
- Current score-to-par, standings, summaries, awards, and report calculations should immediately recalculate using the corrected par.
- The par edit creates its own permanent Receipt/event that clearly records old par -> new par.
- If scores already exist on that hole, the par-change event should receive special mocking commentary about changing par after the fact.
- If multiple individual players already have scores on that hole, create one shared par-correction event that roasts the group generally; recalculate each player's current score-to-par and standings individually rather than emitting duplicate correction events per player.
- Commentary themes may include:
  - suspicious scorecard accounting / possible cheating
  - changing the math to improve over/under
  - nobody knowing what par was
  - failure to read the scorecard
  - failure to understand numbers
  - paperwork magically improving a bad score
- The correction event may explicitly describe how the existing score's current classification changed (for example Bogey -> Par), but must not create a replacement historical score event.
- After a completed round, par cannot be changed unless the round is explicitly reopened; reopening and the later par correction both remain in Receipts.

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

## Score challenges and corrections
- Any connected participant may challenge a listed score that was entered by somebody else.
- A challenge is social/audit state only; it does not change the current score by itself.
- Challenges attach to the exact score event being disputed and remain in Receipts even if the score is later corrected.
- A challenge may optionally include a proposed corrected score and/or comment.
- Any active player may directly edit or remove any active player's current score; spectators may challenge/react but may not mutate golf state.
- If a challenged score is edited or removed, preserve the original score, challenge(s), replies, and actor/subject history; create a new score-push/removal event for the correction.
- Score corrections should trigger fresh mocking commentary visible to the group, especially when a change makes the golfer's result better.
- Group mockery may target scorekeeping, selective memory, creative accounting, cheating accusations, or suddenly improved mathematics without asserting cheating as fact.
- If several people challenged the same score, the correction event may reference the dispute count (for example `3 PEOPLE CALLED BULLSHIT. THE SCORE HAS NOW MYSTERIOUSLY CHANGED.`).
- The live scorecard always shows the latest valid score; Receipts preserves the entire dispute/correction history.
- A golfer may challenge a score entered for them by somebody else just like any other participant.

## Who can enter, edit, and remove scores
- In individual play, any active player may enter a score for any active player in the round. A golfer does not have to enter only their own score.
- This supports real golf behavior where one person may be keeping score while somebody else is driving, putting clubs away, drinking, or simply not paying attention.
- Every score event must preserve both actor and subject:
  - actor = who entered/edited/removed the score
  - subject = whose score it is
- Receipts may expose that distinction when useful, for example: `KHRIS ENTERED MIKE'S 6` or `JOHN CHANGED MIKE 6 -> 5`.
- Any active player may edit or remove another active player's current score; spectators may never mutate scores.
- Score removal is allowed and creates a permanent removal event rather than deleting history.
- Removing a score removes it from current standings, score-to-par, completion, and derived-current-state calculations, but preserves the original score event and all reactions/replies attached to it.
- Re-entering a removed score creates a new score event and new reaction opportunity.
- Correcting a score that was entered for the wrong player is handled as remove-from-wrong-player plus enter-for-correct-player unless a dedicated move action is later added.
- Completed rounds remain frozen; edits/removals require an explicit round reopen first.
- No host or designated scorekeeper is required. The audit trail is the accountability mechanism rather than restrictive score ownership.
- A player does not need an active phone/session to remain a valid round participant. Their phone may be dead, absent, disconnected, or intentionally unused while other active players keep their score.
- Device presence must never be used to decide whether a player is eligible for scoring, standings, completion, withdrawal, or results.
- Reconnecting later restores that player's live view and social controls without changing any scores other players entered for them.

## Score edits after reactions
- Editing a score never rewrites or deletes the original score event.
- The original reported score keeps its exact banter, mascot, reactions, replies, timestamps, and Receipt history.
- A changed score creates a new score-push event with its own presentation and a fresh opportunity for reactions/responses.
- The live scorecard displays only the latest current score, while Receipts preserves the full sequence of score revisions.
- Reactions remain attached to the exact score version they answered; they do not migrate to the corrected score.
- Current standings, score-to-par, awards, and report calculations use the latest valid score, while the Final Damage Report may still roast the revision history.
- Multiple revisions should remain visible as an audit trail rather than collapsing into one final value.

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
