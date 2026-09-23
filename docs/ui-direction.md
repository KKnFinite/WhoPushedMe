# UI Direction

Status: active UI phase after the gameplay/content foundation freeze.

## Product feel

Who Pushed Me?! should feel like a multiplayer golf game with a social feed, not a
traditional scorecard with jokes pasted onto it.

The UI should prioritize:

1. The live hole and current scoring action.
2. The group and standings context.
3. Social reactions, banter, Bag actions and Receipts.
4. Setup/settings only when they are needed.

## Mobile rules

- Mobile is the primary layout.
- Active-round screens are full-screen app surfaces, not desktop-style modals.
- The live hole remains visually dominant and easy to reach while scrolling.
- Score entry needs large touch targets and one-handed use.
- Secondary controls compress rather than compete with score entry.
- Social content should read like a live activity stream.
- Important destructive or corrective actions remain explicit and auditable.

## Visual system

Use the established green / cream / burnt orange / yellow / black identity.

- Green/black = game chrome and factual state.
- Yellow = primary action / live score emphasis.
- Orange = social action, correction, warning or escalation.
- Cream = neutral cards and editing surfaces.

The mascot and content art are accents, not permanent clutter. They should hit when
an event deserves attention.

## Phase order

1. Mobile shell, home hierarchy, live round scoring surface.
2. Round setup and lobby.
3. Receipts/activity presentation and Bag.
4. Round-end results and PDF handoff.
5. Settings/auth polish.
6. Responsive desktop/tablet refinement.

Backend/gameplay changes during this phase should happen only for demonstrated bugs,
locked-rule contradictions, data integrity issues, or UI blockers.
