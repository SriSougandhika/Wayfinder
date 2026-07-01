# Reference: Human-Centric Buffer Standards

## 1. The 15-Minute Padding Rule
- **Rationale:** Humans are not deterministic machines. This 15-minute slack padding accounts for "un-mappable" transit friction like waiting for an elevator, finding a park entrance, or simple pedestrian crowd flow [2, 3].
- **Application:** Apply this buffer *after* every landmark visit and *before* starting the next transit leg.

## 2. Meal Window Integrity
- **Logic:** Meals are mandatory rest states, not optional "stops." If a user request forces a landmark visit to overlap more than 15% of a meal window, the script must flag a conflict [4].

## 3. The 8-Hour Rest Threshold
- **Rationale:** To prevent travel burnout, the system enforces a non-negotiable 8-hour gap between the final drop-off at `staying_at` and the first start time the following day.