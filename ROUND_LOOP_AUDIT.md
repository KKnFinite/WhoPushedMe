# Round Loop Audit

This file records the functional acceptance rules for the v0.4 round loop.
The current HTML/CSS is scaffolding only. Visual approval happens separately.

## Account and entry
- A valid authenticated account can create or join a round.
- New rounds begin in `setup`.
- A round code is four digits and is only unique among live setup/active rounds.
- Reused historical codes resolve within the authenticated golfer's own round history.
- Spectators can join setup or active rounds.

## Lobby
- Any player may start the round.
- Spectators may not start it.
- Course rounds with tee data require every player to choose a tee before start.
- Free Play does not require a tee.

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
