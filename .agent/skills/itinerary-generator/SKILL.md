---
name: itinerary-generator
description: |
  Generates a geographically optimized trip plan anchored to a specific accommodation.
  Use only AFTER 'staying_at' coordinates are finalized.
version: 1.1.0
---
# Workflow
1. **Retrieve Anchor:** Load `staying_at` coordinates from the shared session state.
2. **POI Discovery:** Query Google Maps MCP for Top 20 points of interest within the user-defined radius (15–40km) of the anchor.
3. **Execution:** Pass POIs and anchor to `scripts/cluster_locations.py`.
4. **Judgment:** Use `references/travel_priorities.md` to select the best 3–4 stops per day from the clusters.
5. **Format:** Generate the plan using `assets/itinerary_template.md`.