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
