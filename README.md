# Sri Krishna Taak: portfolio (the Yatra Express)

Live: https://emailsrikrishna9-hub.github.io/sri-krishna-yatra/

A 3D train journey with a text version. One scroll, swipe or key press moves exactly one stop. The index, the dots and the Previous and Next buttons are the accessible controls. A stacked fallback shows the same work if 3D is unavailable.

- `index.html`, `assets/`, `resume*.pdf`: the published site (what GitHub Pages serves from the root).
- `source/`: the generator and copy. `source/world/site_content.py` holds all published text; `source/world/build_world.py` builds `world/dist`; `source/scripts/validate_world.py` checks the build.
- `source/docs/SOURCE-COVERAGE.md`: what was opened and what could not be reached. `source/docs/CLAIMS.md`: every published claim with its source, status and what is mine versus a team's.

Rebuild: copy `source/` to a working folder, run `python3 world/build_world.py` then `python3 scripts/validate_world.py`, and copy `world/dist/` over the repository root.
