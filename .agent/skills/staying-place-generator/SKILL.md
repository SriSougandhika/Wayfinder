---
name: staying-place-generator
description: |
  Facilitates the selection and finalization of trip accommodation. 
  Use when the user has provided a location but NO 'staying_at' value is finalized. 
  Do NOT use for landmarks, sightseeing, or general itinerary sequencing.
version: 1.0.0
---
# Workflow
1. Query the Google Maps MCP for top-rated accommodations near the destination's city center.
2. **Execute `scripts/rank_accommodations.py`** to filter and rank the top 5 results into varied budget options using `references/budget_categories.md` to filter by rating and budget variety.
3. Present options to the user using `assets/accommodation_options_template.md`.
4. Once a choice is made, query MCP for exact `{lat, lng}` and update the `staying_at` schema.