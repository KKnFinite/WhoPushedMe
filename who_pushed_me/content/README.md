# WHO PUSHED ME?! content system

This package separates factual game events from presentation content.

- events.json defines the canonical event hierarchy and fallback scopes.
- themes.json defines user-toggleable content themes. New themes are data, not schema.
- banter.json contains version-controlled banter and explicit event eligibility.
- mascots.json contains gameplay eligibility for mini mascot asset IDs.
- catalog.py validates and resolves event-specific content.

Eligibility is explicit. A narrow water-shot joke cannot leak into an unrelated event.
Broad content may target a parent scope such as mid_hole.callout or generic.golf.

Physical image metadata remains in static/assets/_meta/asset-manifest.json.

Use:

python tools/content_admin.py validate
python tools/content_admin.py list-events
python tools/content_admin.py add-banter
python tools/content_admin.py add-mini <path-to-transparent-png>


## Existing-mini visual audit

The first metadata pass for legacy/current minis is intentionally provisional.
Every existing mascot must be visually audited before the content foundation is merged.

Use:

python tools/content_admin.py audit-status
python tools/content_admin.py audit-minis
python tools/content_admin.py audit-minis --family round-end/complete
python tools/content_admin.py validate --strict-audit

The audit command opens each PNG in the operating system's default image viewer and records:
- exact visible message copy
- optional hat copy
- explicit eligible event scopes
- vulgarity level
- content themes
- notes
- verified audit state

A verified mascot record is the authoritative content description of the artwork.
Changing metadata does not alter text baked into the PNG.

## User preferences and runtime controls

User-facing content preferences are stored in Neon in `golfer_content_preferences`.

V1 settings are:
- mini mascots on/off
- trash talk on/off
- vulgarity normal/brutal
- data-driven theme toggles such as drinking and wife jokes

Theme choices are stored as a JSON object so future themes do not require a schema change.

Global beta controls are stored separately:
- `content_system_settings` controls all minis and all trash talk
- `content_event_overrides` can enable/disable an exact event or an event-family scope

After applying migrations, use:

```
python tools/content_admin.py runtime-status
python tools/content_admin.py set-master minis off
python tools/content_admin.py set-master banter off
python tools/content_admin.py set-event mid_hole.callout off
python tools/content_admin.py set-event mid_hole.callout default
```

Runtime controls never remove or alter the underlying factual golf event. They only control presentation content.

