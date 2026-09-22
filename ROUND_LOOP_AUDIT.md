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

## Multiple devices per golfer
- The same golfer account may be logged in on multiple devices at the same time.
- Each device receives its own authenticated session, but all sessions resolve to the same golfer/account identity and therefore the same round participant.
- Logging in on a second phone/tablet must never create a duplicate participant in the round.
- Reactions, challenges, unread/catch-up state, and participant-level limits apply to the golfer identity, not separately to each device.
- Either device may score, comment, react, or browse history using the same participant permissions.
- Conflicting golf-state edits from two devices owned by the same golfer follow the same normal concurrency/audit rules as edits from different golfers.
- Logging out on one device should revoke only that device's session; account recovery/password reset may revoke all active sessions as a security action.

## Account and entry
- A valid authenticated account can create or join a round.
- New rounds begin in `setup`.
- A round code is four digits and is only unique among live setup/active rounds.
- Reused historical codes resolve within the authenticated golfer's own round history.
- Spectators can join setup or active rounds.

## Round-code privacy and access
- The 4-digit round code is optimized for easy live joining and must not be treated as a permanent secret.
- Joining a live round by code requires an authenticated account unless the golfer is being represented as a round-only/no-app participant added by an existing player.
- Wrong-code attempts must be aggressively rate-limited so 4-digit codes cannot be brute-forced efficiently.
- If an account enters a code for a round they already belong to, resume the existing participant identity rather than creating a duplicate.
- Knowing a round code grants access only to that round's allowed live/post-round surface; it does not expose a golfer's unrelated profile/history.
- After a round is completed, the simple 4-digit code should not be the long-term public sharing mechanism for brand-new viewers.
- Existing participants/viewers retain access through their account/history; future sharing with new people should use a separate unguessable share link/token.

## Spectator mode
- A spectator joins the round, not a specific hole.
- Spectators never choose a starting hole, tracked-from hole, or scoring window.
- Joining an active round as a spectator immediately opens the live spectator view at the round's current state.
- As the group advances, the spectator follows the live round and sees events unfold in real time.
- Spectators can view live scores, banter, minis, score responses, Bag activity, contributions, standings, and other shared round events as they occur.
- Spectators may use allowed social actions such as score responses, reactions, and Open Mic.
- Spectators never acquire score, par, tee, contribution, completion, or hole-advancement obligations merely by joining.
- A spectator may become a player during an active round. On conversion, they choose whether to start scoring from the current live route position or backfill earlier scores if they were already physically playing.
- In individual play, an active player who stops playing should use the towel/withdrawal flow rather than silently changing themselves to spectator, so DNF history and completion rules stay honest.
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

## Adding a no-app player after the round starts
- Any active player may add a round-only/no-app golfer after the round has already started.
- Scramble: the new golfer joins the existing team state from that point forward; prior team scores remain untouched and no earlier personal contribution history is fabricated.
- Individual: default the new golfer's tracked route to the group's current live hole.
- If that golfer was already physically playing before being added, earlier scores may be backfilled.
- If earlier scores are not backfilled, those earlier holes are outside that golfer's tracked route and are treated as PARTIAL, not assumed par and not missing.
- The new golfer can immediately be scored, targeted by banter/callouts/blame, receive reactions, throw in the towel, and appear in Receipts/results/report history according to normal player rules.
- If the golfer later creates an account, the existing round-only participant is claimed rather than duplicated.
- If multiple unclaimed golfers share a display name, show enough context to identify the correct participant.

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

## Player and spectator limits
- A round supports a maximum of 4 golfers/players total, including connected, offline/no-app, and round-only golfers.
- Individual and scramble modes both use the same 4-player cap.
- Withdrawn/DNF golfers remain part of the round roster and continue to count toward the original 4-player roster; another golfer cannot replace them as a fifth participant.
- Spectators have no user-facing hard cap.
- Spectator access should instead be protected by ordinary technical safeguards such as authentication, rate limiting, efficient event delivery, and abuse controls so an unexpectedly large audience cannot overwhelm live polling/database resources.
- If a future infrastructure safety ceiling is needed, it should be a high technical limit rather than a normal product rule shown to golfers.

## Challenges to backfilled / historical scores
- Backfilled and other old-hole scores remain fully challengeable from Receipts/history.
- Any connected participant may challenge an old score they did not originally enter, using the normal challenge rules.
- Active players may correct or remove old-hole scores while the round is active; spectators may challenge/react/comment but may not mutate golf state.
- A correction to an old/backfilled score preserves the original score event, all challenges/replies, and the correction audit trail.
- Historical corrections update current totals, score-to-par, standings, stats, and report calculations immediately.
- Historical corrections must not interrupt the current live hole with a large game-event takeover or replay old derived moments.
- A compact live notice or catch-up item is appropriate, with mocking copy such as:
  - `HISTORICAL REVISION: MIKE'S HOLE 4 HAS MIRACULOUSLY IMPROVED.`
  - `THE ARCHIVES HAVE BEEN EDITED.`
  - `APPARENTLY WE REMEMBER THAT HOLE DIFFERENTLY NOW.`
  - `OLD SCORE. NEW STORY.`
- The detailed dispute/correction stays in Receipts, while the live scorecard remains focused on the current route position.

## Backfilling earlier scores
- Backfilled scores are stored as normal factual scores but marked as `BACKFILLED` so history can distinguish delayed entry from live entry.
- Backfilled scores immediately update current totals, score-to-par, stats, and current standings.
- Each backfilled score remains individually visible in Receipts and available to the Final Damage Report.
- Backfilling multiple old holes must not replay a flood of old live-event popups, old lead-change banners, or historical streak notifications as though those moments just happened.
- Instead, a batch backfill should create one shared summary event for the group, such as:
  - `MIKE JUST FILED 9 HOLES OF EVIDENCE AFTER THE FACT.`
  - `THE HISTORICAL RECORD HAS BEEN CONVENIENTLY UPDATED.`
  - `NOTHING SUSPICIOUS ABOUT REMEMBERING NINE SCORES ALL AT ONCE.`
- Historical score classifications (birdie, bogey, etc.) may still be derived and retained for stats/reporting, but their presentation should be catch-up/history oriented rather than live interruption.
- Current standings should recalculate immediately after the backfill batch completes.
- Old-hole backfill never changes the shared live route position.

## Replacement / late-joining player scoring
- A replacement or late-joining individual golfer defaults to a `PARTIAL ROUND` whose tracked route begins at the live route position where they join.
- If that golfer was already physically playing before joining the app/roster, they may backfill any legitimate earlier scores at any time while the round is active.
- Backfilled earlier scores become part of that golfer's tracked route and current totals once entered.
- If the earlier scores are never entered, those earlier holes remain outside that golfer's tracked route rather than being treated as missing or assumed par.
- A replacement golfer is not ranked against full-route players unless their effective tracked route becomes comparable under the normal placement rules.
- The removed player's status/history remains `REMOVED BY GROUP`; adding or backfilling a replacement player never rewrites the removed golfer's history.
- Old-hole backfill never moves the shared live route position backward.

## Removed-player roster slots
- A player with status `REMOVED BY GROUP` does not permanently reserve one of the four active-player slots.
- Removing a player frees an active roster slot, so the group may add another golfer up to the normal 4-player maximum.
- The removed player's participant record and all prior scores/history remain preserved for the life of the round; do not delete or overwrite that data when a replacement golfer is added.
- A removed player may be reinstated later only if an active-player slot is available at that time.
- If the active roster is already back at 4 players, the removed player cannot be reinstated until another active golfer leaves, withdraws, or is removed.
- Reinstatement restores the same preserved participant record and history rather than creating a new golfer entry.
- A replacement golfer's scores/history remain their own; never merge the replacement with the previously removed golfer.
- The UI should make this state clear: a removed golfer can be `ELIGIBLE TO RETURN` when a slot exists, or `ROSTER FULL` when no slot is available.

## Reinstating a removed player
- A player with status `REMOVED BY GROUP` may be voted back into the same active round.
- Reinstatement requires a new majority vote of the currently connected eligible players, excluding the removed player from the voting quorum until reinstated.
- The removed player cannot reinstate themselves.
- Reinstatement restores the same participant record; never create a replacement participant.
- All prior scores, reactions, comments, contributions, callouts, removal-vote history, and Receipts remain attached to that participant.
- Reinstatement creates its own permanent Receipt/event and does not erase the original removal event.
- In individual play, scoring obligation resumes from the route position where the player returns unless earlier missed holes are explicitly backfilled.
- Missed holes during removal are not silently assumed, fabricated, or required unless the group/player chooses to backfill them.
- In scramble, the reinstated golfer simply becomes active for future contributions/social actions again; prior team scores remain untouched.
- Reinstatement is available only while the round is active. Once the round has ended, roster correction requires the explicit post-round correction flow.

## Vote to remove a participant
- Only players may initiate or vote on removing another participant; spectators do not get removal votes.
- A removal vote may target either a spectator or a player.
- A player removed by vote receives the distinct status `REMOVED BY GROUP`, not DNF/WITHDREW.
- Individual play: a removed player's prior scores/history remain, but they are excluded from final placement after removal.
- Scramble: a removed player's prior contributions/history remain, but they stop being an active team participant.
- Player-removal votes are disabled when the round has only 2 golfers. In a 2-player round, one golfer cannot vote the other golfer out and turn the match into a solo round.
- In a 2-player round, a golfer who wants to stop may use the normal towel/withdrawal flow, and the pair may use the normal consensus end-round flow.
- Spectator-removal voting remains available in 2-player rounds; the no-removal rule applies specifically to kicking one of the two golfers.
- Majority vote wins among the currently connected eligible players, excluding the participant being voted on.
- The target does not vote on their own removal.
- One golfer gets one vote regardless of how many devices they are logged into.
- Offline/no-app/round-only golfers who have no connected client are not part of the live voting quorum.
- The vote UI must show who initiated it, who has voted, and whether the threshold has been reached.
- A successful removal must create a permanent Receipt/event. Removal is never silent.
- Removing a participant must preserve all historical scores, reactions, comments, contributions, callouts, and other events already associated with them.
- Removed participants lose live access to that round unless a later explicit re-invite/restore flow permits return.
- The exact competitive treatment of a removed player (for example REMOVED vs DNF and how placement is handled) must follow the player-removal rule chosen before implementation.

## Lobby
- Any player may start the round.
- Spectators may not start it.
- Course rounds with tee data require every player to choose a tee before start.
- Free Play does not require a tee.

## Route editing before round start
- While the round is still in setup/lobby, the planned route remains freely editable.
- Players may change starting hole, planned length, custom ending hole, wraparound choice, and whether the round is 9/full/custom before `START THE SHITSHOW`.
- Pre-start route edits may rebuild the planned play order because no live golf state has begun yet.
- Once the round becomes active, the normal active-route rules take over: the played route is locked, and the route may only be extended forward or ended early.
- Pre-start route changes must not create noisy Receipts/history events; only the final route at round start becomes the authoritative starting plan.

## Round route and starting mid-round
- A round is defined by an explicit play order, not by assuming hole 1 through hole 18.
- Route position is distinct from physical course hole number. This is required for 9-hole courses played twice, shotgun starts, wraparound routes, and any route where the same physical hole can appear more than once.
- Example: route position 3 may be physical Hole 3 on the first loop, while route position 12 may be physical Hole 3 on the second loop.
- If `CUSTOM END` equals the selected starting hole, interpret that as playing only that one hole. A full loop must be expressed explicitly with `FULL 9` or `FULL 18`.
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
- Par tracking is an explicit round mode: either the round tracks par or it does not.
- Course/API data should populate hole par and tee data whenever available.
- When API/course par is unavailable or incomplete, setup offers:
  - enter all pars now
  - enter pars as you go
  - do not track par for this round
- If the group chooses `DO NOT TRACK PAR`, score entry proceeds without par prompts and the app does not show cumulative score-to-par, birdie/par/bogey classification, or par-based derived moments for that round.
- If par tracking is enabled and the current route position has no known par, the first attempt to enter a score on that hole should pause that score entry with a lightweight sarcastic prompt to establish par first.
- The prompt should be fast and nontechnical, with copy in the direction of:
  - `HOW ABOUT WE ESTABLISH PAR BEFORE WE START INVENTING BOGEYS?`
  - `WE NEED PAR BEFORE WE CAN JUDGE YOU PROPERLY.`
  - `NUMBERS ARE HARD. WHAT'S PAR?`
- Once par is entered, return directly to the pending score entry so the golfer does not have to restart the flow.
- When par tracking is enabled, every counted route position must ultimately have par before the round can show cumulative score-to-par or finalize par-based summaries.
- Par is all-or-nothing for round-level score-to-par reporting: if any counted route position is missing par, suppress cumulative round score-to-par until the missing pars are supplied.
- Hole-level birdie/par/bogey/etc. classification is available only once that hole's par is known.
- Free Play follows the same rule: either track par for the route or explicitly play without par-based scoring.
- To avoid rewriting the scoring model mid-round, the track-par vs no-par choice should be locked once the first factual score is accepted. Before the first score, the group may change that setup choice freely.

## Game-mode lock after round start
- Round mode is editable only during setup/lobby before the round becomes active.
- Once the round starts, the mode is permanently locked for that round.
- Do not show individual/scramble mode controls anywhere in the active-round UI; the option should disappear rather than appear disabled.
- An active round cannot switch between `EVERY ASSHOLE FOR THEMSELVES` and `WE SUCK TOGETHER`.
- If the wrong mode was chosen, the group must abandon/end that round and start a new one in the correct mode.
- Do not attempt to convert individual scores into team scores or vice versa.
- Mode history remains part of the abandoned round record rather than being silently rewritten.

## Course lock after round start
- Course selection is locked once the round status becomes active.
- The selected course, course identity, and hole mapping cannot be changed during an active round.
- If the group selected the wrong course, they must explicitly end/abandon the current round and start a new round with the correct course.
- Do not attempt to remap already-entered holes to another course after play has begun.
- Tee/scoring-tee corrections may still follow their own audited rules when supported, but the underlying course itself remains immutable once the round starts.
- Receipts/history should preserve that the abandoned round existed rather than silently converting it into a different course.

## Tee selection behavior
- Each individual golfer selects a tee during round setup; scramble selects one team scoring tee during setup.
- The selected tee controls the tee-specific hole data shown for that golfer/team, including yardage, par when tee-specific, Course Rating/Slope when available, and handicap calculations.
- Keep tee controls out of the normal live-hole UI. Tee selection is a round setting, not something golfers toggle hole-by-hole.
- During an active round, allow a tee selection to be corrected from round settings if the wrong tee was chosen, following the familiar pattern used by mainstream scorecard apps.
- A tee correction applies to that golfer's/team's round scoring context rather than creating per-hole mixed-tee scoring in v1.
- If a tee correction changes par, rating, slope, or handicap math, recalculate current derived standings/net values while preserving the prior tee choice and the correction in Receipts.
- Completed rounds require the explicit correction/reopen flow before tee data can be changed.

## Tee and par rules
- Individual play may use different tees per player; each player's score-to-par must use the par associated with that player's selected tee when course data varies by tee.
- Scramble uses one explicitly selected scoring tee for the entire team.
- The scramble team's par, score-to-par, standings/result math, and report output all use that one team scoring tee.
- Individual players may physically hit from different tees during a scramble if the group wants, but that does not change the scoring tee unless the team explicitly changes it through a supported edit flow.
- Any scoring-tee change after scores exist must create a permanent history event and recompute affected score-to-par values rather than silently rewriting history.

## Score entry when par is missing
- If par tracking is ON, do not accept the first factual score for a route position until that route position has par.
- This prevents a score from being recorded without knowing whether it is birdie/par/bogey and avoids retroactively fabricating the original score presentation later.
- If par tracking is OFF for the round, accept scores normally with no par prompt and no par-based classification.
- A later par correction is still allowed under the normal audited par-change rules; this section only governs the initial missing-par case.

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

## Repeated physical-hole display
- When the route visits the same physical course hole more than once, keep the physical hole number as the primary label and use route progress to disambiguate it.
- Example:
  - first occurrence: `HOLE 3 • 3 OF 18`
  - second occurrence: `HOLE 3 • 12 OF 18`
- Do not add `FIRST LOOP` / `SECOND LOOP` labels or other special loop terminology.
- Route progress is the universal disambiguator for repeated holes, shotgun routes, wraparound routes, and custom-length rounds.

## Future-hole preview
- Any participant may browse ahead to future route positions to preview hole data without changing the shared active hole.
- Future route positions are read-only for scoring until the round actually reaches them.
- Show available hole data such as par, yardage, tee/course details, and route position while hiding/disabling score-entry and score-mutation controls.
- The UI should clearly label future browsing, for example `PREVIEWING HOLE 12 • LIVE: HOLE 8`, and offer `BACK TO LIVE`.
- Active players may freely edit the current active hole and previously reached holes, but may not pre-enter factual scores on unreached future route positions.
- Preventing future score entry avoids accidental score events, standings changes, banter, and auto-advance behavior for golf that has not happened yet.
- When the shared active route reaches that future position, normal score controls become available automatically.

## Active hole vs browsing old holes
- The round has one shared active route position/hole that represents where the group is currently playing.
- The live scorecard defaults to that active hole and shows the relevant hole data for each golfer/team, including tee-specific yardage/par data when available.
- Players and spectators may browse back to any previously reached route position to review hole data, scores, events, contributions, reactions, and Receipts for that hole.
- Players and spectators may also browse ahead to future route positions to preview hole data such as par, yardage, tee information, and course details without changing the shared active hole.
- Active players may edit/add/remove scores or other editable golf data on an older hole while viewing it.
- Editing an older hole never changes the shared active hole and never drags other connected users backward.
- After an old-hole edit, the user may stay on that viewed hole or return to the active hole; the app should always make the current live hole obvious.
- Route position, not just physical hole number, identifies the viewed hole so repeated holes on wrapped/9-hole-loop routes remain distinct.
- The shared active hole changes only through explicit live-round advancement/navigation rules, not because somebody browsed history.
- Tee selection is a separate concept from hole navigation. A golfer's selected tee determines which tee-specific hole data/scoring inputs apply; browsing backward does not change that tee selection.

## Active-hole progression
- The round has one shared active route position.
- The active hole automatically advances to the next route position once every currently active individual golfer has a score for the active hole.
- In scramble, the active hole automatically advances once the team score for the active hole is entered.
- Automatic advancement is convenience only; it must not prevent old-hole editing or future-hole preview.
- Any active player may manually advance the shared active hole before all scores are present. Missing scores remain flagged and may be backfilled later under the normal rules.
- Browsing an old or future hole never changes the shared active hole.
- When the active hole changes automatically or manually, connected clients should follow the new live state unless that user is intentionally browsing another route position, in which case the UI should clearly show `LIVE: HOLE X` and offer `BACK TO LIVE`.

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

## Reconnect after the round advances
- If a device is offline while the group advances one or more holes, reconnecting must snap that client to the round's current live hole/state.
- Do not replay old holes as forced navigation and do not move the shared round backward to match the reconnecting device.
- Any old hole the user was locally viewing before disconnect remains only as local viewing context; the live round state wins on reconnect.
- Reconnection should surface a personal catch-up count through `YOU MISSED SOME SHIT • N` so the user can review everything that happened while they were away.
- Pending offline actions keep their original target hole/event and are reconciled against current server state independently of where the live round has advanced.
- If a pending offline score targets an older hole and does not conflict, it may sync without moving the live hole backward.
- If it conflicts with a newer accepted value, use the normal offline conflict-resolution flow.
- Spectators follow the same reconnect rule: resume at the current live round state, with history available for catch-up.

## Temporary offline play and sync conflicts
- The live round must tolerate temporary loss of cell/data service without preventing score entry or lightweight social actions.
- When a connected client loses service, supported actions may be queued locally with their original local timestamp and attempted when connectivity returns.
- The UI must clearly show that an action is pending/offline rather than pretending it has already been accepted by the server.
- Score/par/route mutations queued offline must include enough prior-state/version context for the server/client to detect whether the same golf state changed while that device was disconnected.
- If an offline score entry/revision no longer conflicts when reconnecting, sync it normally and preserve the original actor plus queued timestamp metadata.
- If another accepted change already modified that same current score, do not silently overwrite it.
- Show an explicit conflict resolution such as:
  - current server score
  - queued offline score
  - who last changed the server score when known
  - actions to keep the server value or apply the queued value
- Resolving the conflict creates a normal audited score event; the rejected alternative remains visible in conflict/history metadata where useful.
- Conflict copy may mock the situation, for example:
  - `SCORECARD FIGHT DETECTED.`
  - `APPARENTLY EVEN THE INTERNET DOESN'T KNOW WHAT MIKE SHOT.`
  - `OFFLINE ACCOUNTING HAS ENTERED THE CHAT.`
  - `THE COURSE HAS NO SIGNAL AND APPARENTLY NO CONSENSUS EITHER.`
- Social-only queued actions such as reactions/comments may generally replay in order when service returns, provided the target event still exists.
- Duplicate retries must be idempotent so reconnecting does not create the same score/comment/reaction multiple times.
- If the round ended while a device was offline, queued golf-state mutations must not automatically reopen or rewrite the completed round; surface them for explicit review.
- Offline support must preserve the same rule as online play: current state may change, but accepted historical events are never silently deleted.

## Concurrent score edits
- If two or more connected players edit the same current score from different devices at nearly the same time, the latest accepted edit becomes the current score.
- Every accepted edit remains a separate immutable Receipt with actor, subject, old value, new value, and timestamp.
- A later edit never deletes or rewrites an earlier accepted edit, even when the edits were only seconds apart.
- The live scorecard shows only the latest accepted value; Receipts preserves the full edit race in order.
- If near-simultaneous conflicting edits occur, the app may emit a special shared chaos/correction event and mock the group for fighting over the scorecard.
- Suggested tone includes:
  - `TWO PHONES. THREE OPINIONS. ONE SCORECARD.`
  - `THE SCORE HAS CHANGED AGAIN. NOBODY APPEARS TO BE IN CHARGE.`
  - `MULTIPLAYER ACCOUNTING IS GOING GREAT.`
  - `EVERYBODY STOP TOUCHING THE FUCKING SCORE.`
- Concurrency handling must never silently discard an accepted edit from history, even though only one value can be current.

## Score challenges and corrections
- Any connected participant may challenge a listed score that was entered by somebody else.
- A participant cannot formally challenge a score event they themselves entered; they may simply edit/remove it or use a normal social reaction instead.
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

## Reactions and challenge limits
- Quick reactions are per participant, per event. One participant gets one active quick reaction on a given event.
- A participant may change their quick reaction (for example `NICE` -> `BULLSHIT`) or remove it; counts update rather than stacking another reaction from the same person.
- Reaction counts represent unique participants, not repeated button presses.
- Freeform comments/replies may be multiple and remain separate social events.
- Formal score challenges are separate from quick reactions.
- A participant may have at most one active challenge on a specific score version/event.
- A challenger may withdraw the challenge or update its comment/proposed corrected score, but cannot stack multiple challenges from the same person against the same score version.
- If the score is edited, the new score-push event is a new score version with its own fresh reactions and challenges; reactions/challenges on the prior score version remain attached to that historical event.

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
- If an individual golfer withdraws and later returns, holes missed during the withdrawal remain outside their competitive continuity unless they are backfilled; returning does not silently invent scores for the gap.
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

## Simple handicap setup
- Keep handicap setup familiar to mainstream scorecard apps and optional for casual golfers.
- Individual play only; scramble remains gross-only in v1.
- A golfer profile may store a Handicap Index when the golfer knows it.
- If the selected course/tee provides Course Rating and Slope Rating, calculate the golfer's round/course handicap automatically from the stored Index and tee data.
- If the required course/tee rating data is unavailable, allow a simple manual `ROUND HANDICAP` number instead of forcing the golfer through handicap math.
- Round setup should prefill saved handicap data and require as little input as possible.
- Gross score is always recorded and displayed regardless of handicap availability.
- Net scoring appears only when the group has enabled net competition and the golfer has a usable round handicap.
- Do not require GHIN/USGA linkage, membership, or an official Handicap Index to use Who Pushed Me?!.
- A future official handicap-provider integration may be added separately; v1 should not attempt to become an official handicap authority.
- UI should explain only what the golfer needs at that moment. Prefer `HANDICAP INDEX` when available and fall back to `ROUND HANDICAP` when course data cannot calculate it.

## Handicap availability and correction
- Individual play may use optional net scoring; scramble is gross-only in v1.
- If an individual round uses net scoring for official placement, every golfer needs a round handicap before becoming eligible for net placement.
- A golfer without a saved handicap may still play and score normally; show gross scoring and mark them `NET HANDICAP MISSING` until a round handicap is supplied.
- Existing account handicap data should prefill automatically when available.
- A round-only/no-app golfer's handicap may be entered by any active player.
- Once the golfer's first factual score is accepted, their round handicap is locked against casual editing.
- A later handicap correction is allowed only through an audited correction flow that preserves old value -> new value in Receipts and recalculates current net standings.
- Handicap corrections may trigger mocking group commentary, for example:
  - `AMAZING. FOUR STROKES APPEARED WITHOUT ANYONE SWINGING A CLUB.`
  - `THE HANDICAP HAS BEEN CONVENIENTLY REVISED.`
  - `NET SCORING JUST GOT A LITTLE MORE CREATIVE.`
- Gross scoring/history is never rewritten by handicap changes.
- Scramble ignores handicap/net calculations entirely in v1 and always uses gross team scoring.

## Handicap and net scoring
- Gross scoring is always the factual foundation and is always recorded.
- Handicap/net scoring is optional and never required to create, join, or complete a round.
- When handicap play is disabled, standings/results use gross scoring only.
- When handicap play is enabled, the UI may show both gross and net values in familiar golf format.
- Round setup determines whether official individual placement is based on gross or net scoring.
- A golfer without handicap data may still participate normally; the round must not block them from playing.
- Handicap data belongs to the golfer profile when available, with support for a round-specific value/override when needed.
- Who Pushed Me?! should not present itself as an official handicap authority unless a future sanctioned handicap integration is added.
- Gross history must remain preserved even when net scoring is used for competitive placement.

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

## Participant state model
- Participant state is split into independent dimensions rather than one overloaded status.

### Participation state
- `ACTIVE`: currently part of live play.
- `WITHDREW`: voluntarily threw in the towel; individual play treats this as DNF.
- `REMOVED BY GROUP`: removed by player vote.

### Scorecard coverage state
- `COMPLETE`: every score required by that participant's effective tracked route is present.
- `PARTIAL`: the participant legitimately has a shorter tracked route, such as a late join or approved shortened participation window.
- `INCOMPLETE`: one or more scores are missing that are required by that participant's effective tracked route.
- During an active round, a golfer may also simply be `IN PROGRESS` until their route is finished.

### Connection state
- `CONNECTED`: the golfer currently has a live client/presence.
- `OFFLINE / NO-APP`: the golfer has no active client but remains a normal round participant.

- These dimensions may coexist. Examples:
  - active + in progress + offline
  - active + partial + connected
  - active + incomplete + connected
  - removed by group + partial
- Connection state never changes competitive state by itself.
- Reconnecting restores client/presence only; it does not alter participation or coverage state.
- Returning after withdrawal creates a return event and restores participation to active without erasing the withdrawal Receipt.
- Reinstatement after removal creates a reinstatement event and restores participation to active without erasing the removal Receipt.
- Scorecard coverage is always derived from the participant's effective required route and current accepted scores, not from whether their device is online.

## Placement eligibility
- Official individual placement is based on the player's effective required route, not a hardcoded 18 holes.
- A planned 9-hole round, custom route, wrapped shotgun route, or whole-group early stop can all produce valid official standings when the remaining active players are being compared over the same effective route.
- If every active individual golfer shares the same effective route and has all required scores, normal placement applies even when that route is shorter than 18 holes.
- A legitimate late joiner with a shorter personal route is labeled `PARTIAL ROUND` and is not ranked against golfers who played a different effective route.
- A player with missing required scores is labeled `INCOMPLETE` and is not eligible for official placement until those required scores are filled.
- An individual player who throws in the towel is labeled `DNF` / `WITHDREW` and is excluded from normal winner/place calculations.
- If the whole group ends early together, that shared stopping point becomes the effective route end for the golfers still active; those golfers can still receive official placement over the common played route, while the round remains visibly labeled `ENDED EARLY`.
- Scramble has one team result. A team that ends early keeps its score and score-to-par over the played route, but the report must clearly label the round as ended early.

## Skipping a hole
- The group may explicitly skip the current active route position when a physical hole is unavailable, closed, flooded, excessively backed up, or otherwise not being played.
- `SKIP HOLE` advances the shared active route to the next route position without creating a fake score.
- The skipped route position remains in Receipts/history as `SKIPPED` with the physical hole number, route position, actor, and optional reason.
- A skipped hole is removed from the effective scoring route for totals, score-to-par, completion, streaks, standings, and awards.
- Skipping a hole must not fabricate par, assumed par, zero strokes, or any other placeholder golf result.
- If the group later returns to that physical hole before the round ends, it should be added as a new future route position rather than silently unskipping/reusing the old skipped position.
- Skip actions may trigger mocking commentary, for example:
  - `HOLE SKIPPED. APPARENTLY EVEN THE COURSE HAS HAD ENOUGH.`
  - `WE'RE CALLING THIS ONE A STRATEGIC RETREAT.`
  - `THE HOLE SURVIVES ANOTHER GROUP OF IDIOTS.`
- Skipping is a shared golf-state action and should create a permanent Receipt.
- Any active player may propose `SKIP THIS HOLE`, but the skip takes effect only after a majority of currently connected eligible players approve it.
- Spectators do not vote on hole skips.
- One golfer gets one vote regardless of device count.
- Offline/no-app golfers without a connected client do not block the skip vote.
- The proposer may count as one approving vote.
- The vote UI should show who has approved, who has rejected, and whether the majority threshold has been reached.
- A rejected skip vote leaves the active hole unchanged.
- Future-hole preview does not imply skip; the hole is skipped only through an explicit action.
- A hole cannot be skipped once any factual score has been entered for that route position.
- Do not provide a separate `VOID THIS HOLE` action after scoring has begun.
- If a score was entered by mistake and the group truly intends to skip the hole, the erroneous score(s) must first be removed through the normal audited score-removal flow; only then may the normal skip vote be started.
- Removing those mistaken scores does not erase their Receipts/history.

## Extending an active round
- An active round may be deliberately extended forward from its planned endpoint without changing the locked course or rewriting already-played route positions.
- Use an explicit `EXTEND THE ROUND` action rather than arbitrary mid-route editing.
- Examples:
  - planned 1-9 may be extended to 1-18
  - custom 4-12 may be extended through 18
  - on a 9-hole course, a second loop creates new route positions rather than overwriting the first 1-9
- Already-played route positions, scores, pars, reactions, and Receipts remain unchanged.
- Newly appended route positions immediately become part of the effective required route for active players/team completion.
- Extending the round creates a permanent history event and may trigger mocking presentation such as:
  - `APPARENTLY NINE HOLES OF THIS SHIT WASN'T ENOUGH.`
  - `THEY HAD A CHANCE TO GO HOME. THEY CHOSE MORE GOLF.`
  - `BAD DECISIONS HAVE BEEN EXTENDED.`
- Once active, the route may be changed only by extending the unfinished end or explicitly ending early; do not allow arbitrary surgery in the middle of the route.
- Extra holes added before the round is ended are simply appended to the active route and score normally. There is no separate playoff/bonus scoring mode.
- If the round has already been completed or ended, it stays closed. Any decision to play more golf starts a new round rather than reopening the old one merely to append extra holes.

## Vote math
- Majority actions use a strict majority of currently connected eligible voters: floor(eligible / 2) + 1 yes votes.
- Majority actions include hole skip, participant removal, and participant reinstatement unless a more specific rule overrides them.
- End-the-round-early remains unanimous among currently connected eligible players.
- One golfer gets one vote regardless of how many devices they are logged into.
- The target of a removal or reinstatement vote is excluded from that vote's eligible-voter count.
- No-app/offline golfers without a connected client are excluded from live quorum.
- An abstention / no response is treated as waiting, not as a yes or no vote.
- A vote may remain open while passage is still mathematically possible; once enough explicit no votes make passage impossible, the vote fails.
- Examples:
  - 4 eligible voters, majority action -> 3 yes required.
  - 3 eligible voters, majority action -> 2 yes required.
  - 2 eligible voters, majority action -> 2 yes required.
  - 4 connected golfers, remove 1 target -> 3 eligible voters -> 2 yes required.
  - 3 connected golfers, remove 1 target -> 2 eligible voters -> 2 yes required.
- Player-removal votes remain disabled entirely in a 2-player golf group, regardless of generic majority math.

## Consensus end-of-round and live presence
- Ending the entire round early is a group-consensus action, not a single-player action.
- Any active connected player may initiate an `END THE ROUND` vote.
- Every distinct golfer who is currently considered live/connected to that round must agree before the whole round ends.
- Agreement is per golfer identity, not per device; a golfer logged in on two devices gets one vote.
- Round-only/no-app golfers and players whose clients are offline are not part of the live vote quorum because they have no client capable of voting.
- A connected golfer may vote `END IT` or `KEEP PLAYING`. Any explicit `KEEP PLAYING` vote blocks the end request.
- Authentication/session existence is NOT proof that a golfer is still present. Live presence must use a short heartbeat/last-seen mechanism tied to the active round.
- A golfer who closes the app, loses signal, leaves the course, or simply abandons the session without logging out automatically falls out of the connected vote quorum after the presence timeout.
- If a golfer reconnects before the round actually ends, they rejoin the live presence set and must agree if the end vote is still open.
- If only one golfer remains live/connected, that golfer may end the round by agreeing to their own end request.
- The vote UI should show who has agreed, who is still being waited on, and who is no longer considered connected.
- Presence state is ephemeral operational state and must not rewrite roster membership, DNF status, scores, or history.
- Personal `THROW IN THE TOWEL` remains separate: it affects only that golfer and does not require group approval.
- Presence must be intentionally tolerant of normal golf behavior. Players may go many holes without opening the app because somebody else is keeping score, so a short heartbeat timeout is not appropriate.
- Recommended implementation: keep a long inactivity window (target about 30-45 minutes, tune during field testing) before a golfer is automatically considered unavailable for end-vote quorum.
- Starting an end vote should not instantly exclude a golfer merely because their screen is locked or the app is backgrounded.
- If a golfer has exceeded the long inactivity window, the end-vote UI may label them `INACTIVE / NOT CURRENTLY REQUIRED` and exclude them from quorum.
- If a golfer has not exceeded the inactivity window but does not respond to an end vote, the group should be able to start a separate `MARK AS GONE` confirmation for that golfer; all other currently responding players must agree before that golfer is removed from the vote quorum.
- `MARK AS GONE` changes only live-presence/quorum state. It does not withdraw the golfer, erase scores, or change their competitive status.
- If the marked-gone golfer reconnects before the round ends, they immediately re-enter the live quorum and can vote.

## Advancing with missing scores
- Advancing the shared live route position never requires every score on the current hole to be present.
- Missing scores are a warning state, not a navigation blocker.
- Before advancing, the UI may show a lightweight warning identifying the missing player/team score and offer a clear `GO ANYWAY` action.
- Individual example tone:
  - `DAVE'S SCORE IS STILL MISSING. APPARENTLY WE'RE DOING PAPERWORK LATER.`
- Scramble example tone:
  - `WE'RE LEAVING WITHOUT A SCORE? BOLD.`
- Advancing with missing scores moves the live round forward normally and leaves the earlier route position flagged as missing.
- Active players may backfill the missing score later without moving the shared live route position backward.
- Current standings must reflect the player's/team's incomplete state while required scores are missing.
- Round completion still requires all scores that belong to each active player's/team's effective required route, unless later route/status changes legitimately remove that requirement.
- The app should follow the golf group rather than holding the group on a hole because somebody has not entered a number yet.

## Finishing with missing scores
- Reaching the end of the route with missing required scores must not hold the entire group hostage.
- Before finalizing, show a clear warning that one or more required scores are still missing.
- Offer:
  - `FIX THE SCORECARD` to review/fill the missing entries
  - `FINISH INCOMPLETE` to close the round with the missing data preserved as missing
- Individual play:
  - any golfer with missing required scores finishes as `INCOMPLETE`
  - that golfer is excluded from official placement
  - all recorded scores, banter, reactions, Receipts, awards based on valid recorded data, and Final Damage Report history remain available
  - golfers with complete comparable routes may still receive official placement
- Scramble:
  - the team may finish as `INCOMPLETE ROUND` when one or more required team scores are missing
  - do not show a misleading final cumulative stroke total or final score-to-par when required team scores are missing
  - preserve and report all valid recorded holes and social history
- Finishing incomplete must never invent replacement scores, assumed pars, or synthetic totals.
- The completion event/report should clearly distinguish `INCOMPLETE` from `ENDED EARLY`, `DNF`, and normal completion.
- Suggested warning tone:
  - `WE'RE MISSING A SCORE. APPARENTLY REMEMBERING HOW MANY TIMES YOU HIT THE BALL WAS TOO AMBITIOUS.`
  - `THE SCORECARD HAS A HOLE IN IT. FITTING.`

## Completion
- Contributions, Bag actions, reactions, and score responses are never required to finish.
- Individual completion requires every player to have a score on every hole.
- Scramble completion requires one team score on every hole.
- Completed rounds freeze score/par/shared-hole mutation unless explicitly resumed.
- A completed round may be explicitly reopened for a correction. Reopening creates a permanent Receipt/event, and any later correction creates its own normal audited event. Results/standings/awards are then recomputed from the corrected current state.
- Round-end presentations are selected and stored server-side.

## Joining a completed round
- Entering the code for a completed round opens a read-only post-round view rather than creating a new live participant.
- Post-round viewers may see standings/results, Receipts, awards, and Final Damage Report content that is allowed to be shared.
- A new player cannot be added to the competitive roster after completion.
- A round-only/unclaimed golfer who actually participated may still create an account and claim that existing participant after the round ends.
- Post-round spectator/viewer access does not create a scored participant and does not alter historical standings, completion, or roster counts.
- Any correction to a completed round's roster or golf state requires an explicit reopen/correction flow; ordinary post-round viewing never mutates history.

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

## Notification preferences
- Push notifications are optional and are not required for scoring, voting, challenges, catch-up, or any other round function.
- Default notification mode is `KEEP ME IN THE LOOP`.
- Personal notification modes:
  - `KEEP ME IN THE LOOP` (default): important direct items plus live round activity such as score events, lead changes, Bag activity, comments/replies, and similar social/game moments.
  - `IMPORTANT SHIT ONLY`: direct/high-priority items such as challenges to your score, direct callouts/mentions, vote requests, removal votes, end-round votes, and other actions that specifically need your attention.
  - `SHUT THE FUCK UP`: no push notifications; all activity accumulates normally in `YOU MISSED SOME SHIT` / Receipts.
- Turning notifications off never removes the user from the round, changes presence/roster state, or blocks other players from continuing.
- If push delivery is unavailable, denied, or delayed, the in-app unread/catch-up system remains the authoritative fallback.
- Notification preference applies per golfer account, with future room for device-specific overrides if needed.

## Engagement spectrum
- The app must work equally well for highly engaged players and low-attention golfers.
- A golfer may react/comment on nearly every event, or may look at the app only a few times during the entire round; neither behavior should create scoring, completion, or participation problems.
- Core golf state must continue to function when only one person is actively operating the app for the group.
- Social actions, reactions, Bag activity, contributions, comments, challenges, catch-up, and mascot interactions are optional enrichment, never required workflow.
- The live scorecard should remain useful with zero social interaction.
- Highly engaged users should have deep social/gameplay interaction available without forcing that complexity onto everyone else.
- Low-attention users should be able to reopen the app after a long gap, land on the current live state, and use `YOU MISSED SOME SHIT` / Receipts to catch up at their own pace.
- Notifications/presence logic must not assume frequent screen use or continuous foreground activity.
- Personalized unread state should accumulate safely without blocking the round, and large unread counts should collapse into useful catch-up summaries rather than demanding item-by-item acknowledgment.
- The design target is progressive engagement: score-only users can stay score-only; social users can go as deep as they want.

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
