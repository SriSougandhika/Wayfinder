# Reference: POI Selection & Judgment

## Quality Benchmarks
- **Min Rating:** 4.2 stars required for any "random" POI.
- **Diversity Rule:** Do not schedule more than two landmarks of the same category (e.g., two museums) in a single hub-spoke cluster.

## Hub-and-Spoke Efficiency [user flow]
- **Anchor Priority:** Always prioritize POIs that minimize the "Total Loop" distance (Hotel -> POI 1 -> POI 2 -> Hotel).
- **Time Boxing:** Ensure the combined `estimated_duration_min` of all selected POIs fits within the gaps between the meal windows defined in AGENTS.md.

## Tie-Breaking
If two POIs have identical ratings, select the one that is closest to the previous stop in the daily sequence to minimize transit fatigue.
