---
name: itinerary-refiner
description: |
  Refines travel itineraries based on user feedback. 
  Use when the user wants to add, remove, or swap landmarks.
  Enforces 15-minute padding, meal windows, and 8-hour rest rules.
  Validates all tool calls via the local Policy Server.
---

# Itinerary Refiner

## When to use
- Modifying an existing JSON itinerary.
- Re-calculating routes after a hotel change.

## Workflow
1. **Context Resolution**: Run `scripts/context_resolver.py` to map [[STAYING_AT]] and [[USER_PREFS]] to active session state [3, 4].
2. **Policy Check**: Before calling any Maps or calculation tools, invoke `scripts/policy_server.py` to ensure the action is permitted under `policies.yaml` [5, 6].
3. **Constraint Validation**: Run `scripts/validate_updates.py` to check for violations of "Human-Centric Buffer Standards" (found in `references/`) [7, 8].
4. **Conflict Resolution**: If a rule is violated, return the template from `assets/conflict_message.md`.
5. **Security Review**: For final itinerary commits, present the `assets/vibe_diff.md` and wait for 'APPROVED' [9, 10].

## Anti-patterns
- Do NOT bypass the Policy Server for "quick" updates.
- Do NOT ignore the 8-hour rest threshold even if the user requests a late-night arrival.