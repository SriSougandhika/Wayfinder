# Feature: AI Travel Itinerary Agent

**As a** traveler    
**I want** to provide my trip details and receive a highly optimized, comfortable daily itinerary    
**So that** I can maximize my vacation time without burning out.

## Background & Intent  
The agent creates logically sequenced, geographically optimized travel plans based on user "must-visit" landmarks and preferences. Traditional travel planning forces users to bounce between map routing tools, calendars, and review sites. This agent acts as an autonomous coordinator that understands spatial-temporal relationships. 

The intent is to maximize destination engagement while entirely neutralizing travel fatigue. It accomplishes this by clustering geographically close attractions, computing realistic transit times, and protecting human bio-needs (regular meals and sufficient rest). The end result is a contextual, step-by-step roadmap that behaves less like a rigid calendar and more like an intuitive local guide.

---

## Technical Design

### Data Structures & Schema  
The system uses strict YAML contracts to define properties for locations, itineraries, and the user's operational constraints. 

```yaml  
trip_parameters:
  location: string
  duration_days: integer
  accommodation_required: boolean  # User intake from Step 1
  staying_at:  # user might input from step 1, or might be fetched. 
    name: string
    location: { lat: float, lng: float }

locations_schema:  # fetched from google maps MCP server
  name: string  
  coordinates:  
    lat: float  
    lng: float  
  category: string        # e.g., historical, dining, nature, leisure, transit  
  priority: integer       # Scale 1-5 (5 being absolute must-visit)  
  estimated_duration_min: integer  # Average time spent inside the location

itinerary_constraints:  
  meals:  
    breakfast: { start: "07:00", end: "09:30", duration_min: 45 }  
    lunch: { start: "12:00", end: "14:30", duration_min: 60 }  
    dinner: { start: "18:30", end: "21:30", duration_min: 60 }  
  buffer_time_min: 15     # Slack padding added between consecutive events  
  max_walking_distance_km_daily: 12.0
```

---

## BDD Scenarios:  
### Scenario: User provides complete initial travel details with no accommodation requirement  
* **Given** the Itinerary Agent is in a "READY" state  
* **When** the user provides the following trip details:  
  | Field | Value |  
  | :--- | :--- |  
  | Destination | Paris |  
  | Duration | 3 days |  
  | Acommodation Required | No |
  | Staying At | Hotel Paris at avenue 3 | 
* **Then** the agent should validate the input as complete  
* **And** the agent should transition to a "THINKING" state

---

### Scenario: User provides complete initial travel details with accommodation requirement  
* **Given** the Itinerary Agent is in a "READY" state  
* **When** the user provides the following trip details:  
  | Field | Value |  
  | :--- | :--- |  
  | Destination | Paris |  
  | Duration | 3 days |  
  | Acommodation Required | Yes | 
* **Then** the agent should validate the input as complete  
* **And** the agent should transition to a "THINKING" state

---

### Scenario: Agent successfully charts an optimal itinerary with meal and rest breaks along with suggesting a staying place
* **Given** the agent has accepted valid trip details for "Paris" for "3 days"  with "yes" for accommodation required and no fixed input for staying at
* **When** the agent processes the geography and logistics of the destination
* **Then** it should identify the hotels or staying places grouped by geographic proximity to city centre. 
* **And** the agent should display the list of top 5 amicable places to stay with a varied range of budgets, to choose on of them as an input to staying_at.
* And once the user selects a place, the agent must query the Google Maps MCP to retrieve and store its coordinates {lat, lng} in the staying_at schema [user flow].
---

### Scenario: Agent successfully charts an optimal itinerary with meal and rest breaks for given staying place
* **Given** the agent has accepted valid trip details for "Paris" for "3 days" staying at "Hotel Paris at avenue 3"
* **When** the agent processes the geography and logistics of the destination as well as finalizes the location of the staying place
* **Then** it should identify points of interest grouped by geographic proximity to staying place
* **And** it should generate a timeline for Day 1, Day 2, and Day 3 that enforces:  
  | Constraint | Rule |  
  | :--- | :--- |  
  | Breakfast Break | Required between 7:00 AM and 9:30 AM |  
  | Lunch Break | Required between 12:00 PM and 2:30 PM |  
  | Dinner Break | Required between 6:30 PM and 9:30 PM |  
  | Night Rest | Minimum 8 hours of downtime |  
* **And** the travel time between consecutive attractions on the same day must be minimized  
* **And** the agent should display the finalized itinerary in a clean, structured format

---

### Scenario: User requests a modification that fits optimally  
* **Given** the agent has displayed a 3-day itinerary for "Paris"  
* **When** the user requests to add "The Louvre Museum" to the itinerary  
* **And** the agent determines the new location can fit within the meal and rest constraints  
* **Then** the agent should recalculate the daily routes optimally  
* **And** it should display the updated itinerary to the user

---

### Scenario: User requests too many modifications, triggering a rejection prompt  
* **Given** the agent has displayed a 1-day itinerary for "Paris"  
* **When** the user requests to add 5 new far-apart attractions to the itinerary  
* **And** the agent determines it is mathematically impossible to visit them all while respecting meal and rest constraints  
* **Then** the agent must not modify the itinerary  
* **And** the agent should prompt the user with a message: "I cannot fit all of these places into your timeline without cutting into your rest or meals. Please choose 2 or 3 places to remove from your request."  
