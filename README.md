# <img width="50" height="50" alt="logo" src="https://github.com/user-attachments/assets/6a17e535-3b68-4932-9fc3-7c423cb63b8d" /> Wayfinder - Agentic Travel Itinerary Planner
A very basic agentic AI-based travel itinerary planner that matches user requirements, recommending places to stay and must-visit places listed out in a schedule, considering enough rest and less burnout. 
Watch the demonstration for WayFinder Agent here: [Project-Pitch]()

## 📌 Problem Statement
- **The Hassle of Travel Planning:** Traditional travel planning is tedious. Handling fragmented data across 10+ tabs, rigid static itineraries, and an inability to handle sudden real-time changes.

- **Why Static AI Fails:** A standard LLM chatbot isn't enough. It cannot handle complex multi-step reasoning and may not suggest timelines that align with enough rest and time for food. 

- **The Goal:** Defining an agent that could keep all these things in mind and have the ability to chart out schedules with less burnout, covering nearby places in a single day with enough gaps for taking rest, might be a possible solution for this.

## 🚀 The Solution & Agentic Capabilities
Now, I don't sit for long hours calculating distances and putting places to visit on day 1, day 2, and so on; I need to ask WayFinder to do that for me. The MCP (for this project, I have used a mock MCP server), which can be integrated with the Google Maps MCP Server, provides real-time data and up-to-date location status. 
Agentic features will remember all constraints, chart out the itinerary, and refine it spontaneously if required. 
- **Auto-suggest accommodations:** Locates best places to stay over, with all budget categories, and allows the user to choose from them. Also works if accommodations are pre-specified.
- **Autonomy:** Makes decisions without constant user prompting, based on clustering nearby locations and also calculating transit times for real-time mapping. Further, allocates enough time for nightly rest and hours for breakfast, lunch, and dinner. 
- **Dynamic Replanning:** Handles changes like "What if day 2 rains?" and charts out the modified plan, again abiding by all the constraints.

## 🏗️ Architecture & Workflow
<img width="1412" height="634" alt="agent workflow" src="https://github.com/user-attachments/assets/c771a856-6b78-477d-b688-ac8d936f4ca3" />

The flow of WayFinder supports two major paths:
1. **When the user has provided a place for accommodation**: It simply begins by drafting the first version of the itinerary for the provided specifications.
2. **When the user has not provided any accommodation**: It adds a step in between and first fixes the place of stay, then begins to draft the itinerary later.

## 📦 Component Breakdown
To view things on the technical side from an agentic perspective, here is a breakdown of the entire agentic system of my WayFinder. We follow the equation Agent = Model + Harness. 
1. **Model**: This is the part that executes the defined thinking logic. For this purpose, I have used the basic model to integrate with Antigravity IDE, Gemini 3.5 Flash (Medium).
2. **Harness**: This is the scaffolding or the thinking logic. This is the structured path I have defined for my model to follow, so it does not hallucinate or take unnecessary steps.

The harness includes the following prospects:
- **Agent Specifications [itinerary_creator.md](specs/itinerary_creator.md) File:** This includes the specifications of how the agent should behave and what schemas it will be encountering. Multiple scenarios are defined in a BDD or Behavior-Driven Development methodology using the Gherkin format, "Given -> When -> And -> Then".
- **Agent Harness Configuration [AGENTS.md](AGENTS.md) File:** This consists of the workflow, core operational rules, persona to be maintained, and finally the skill index, including all skills it can use.
- **MCP Tools via [Mock-MCP-Server](mcp/mock_maps_server.py):** I originally intended to use the Google Maps MCP Server to fetch the details of locations, to calculate distances, and cluster locations, but due to constraints, I had to go for a mock MCP server Python file, having the details for a few hotels and the must-visit locations in only two places: Paris and Lyon. To launch this, we have a [configuration](.antigravity/config.json) JSON file.
- **Agent skills:** Also mentioned in the agents.md file, these skills will help the agent follow specific instructions without overloading itself and keeping the desk clean through progressive disclosure and dynamic context handling. We have used three major skills:
  1. **[staying-place-generator](.agent/skills/staying-place-generator/SKILL.md):** used when the accommodation has not been provided by the user.
  2. **[itinerary-generator](.agent/skills/itinerary-generator/SKILL.md):** used to generate the itinerary draft for given user requirements.
  3. **[itinerary-refiner](.agent/skills/itinerary-refiner/SKILL.md):** used when the user wishes to modify it spontaneously.
- Security aspects: Security is important so that the agent does not drift away or cross boundaries it must not. So we implement 5 major measures:
  1. **[Sandboxing](https://antigravity.google/docs/ide/settings#terminal-sandboxing)**: Enabling this feature in Antigravity IDE makes the whole execution isolated and does not pose problems to the original production or deployment sites.
  2. **[Policy Server](.agent/skills/itinerary-refiner/scripts/policy_server.py):** Performs the security and semantic safety checks, ensuring the LLM follows the safety policies.
  3. **[Context Resolver](.agent/skills/itinerary-refiner/scripts/context_resolver.py):** Helps keep PII or Personally Identifiable Information like API keys, credentials, or even names as environment variables for protection.
  4. **[Policies YAML](policies.yaml):** Defines structural gating by specifying exactly which tools are allowed for each role and environment to prevent unauthorized access.
  5. **[Vibe Diff MD](.agent/skills/itinerary-refiner/assets/vibe_diff.md):** Acts as a Human-In-The-Loop (HITL) checkpoint, translating complex code back into a plain-English summary, so I can verify the proposed execution matches my original intent before providing cryptographic consent.

The diagram below summarizes the entire agentic architecture I've built:

<img width="1232" height="1136" alt="agent architecture" src="https://github.com/user-attachments/assets/0c78f340-798a-4fbe-a74e-4895d637f16f" />

### 📃Agent Skills:
To better explain how I've structured these three simple skills, here is an overview of each of them: 
#### 1. staying-place-generator Skill:
- Query the MCP for top-rated accommodations near the destination's city center.
- Execute [rank-accommodations-script](.agent/skills/staying-place-generator/scripts/rank_accommodations.py) to filter and rank the top 5 results into varied budget options using [budget-categories.md](.agent/skills/staying-place-generator/references/budget_categories.md) to filter by rating and budget variety.
- Present options to the user using [accommodations-template.md](.agent/skills/staying-place-generator/assets/accommodation_options_template.md).
- Once a choice is made, update the staying_at schema to insert the accommodation location.

#### 2. itinerary-generator Skill:
- Loads accommodation coordinates as an anchor from the shared session state.
- POI Discovery: Query MCP for the top 20 points of interest within the user-defined radius (15–40km) of the anchor.
- Pass POIs and anchor to [cluster-locations.py](.agent/skills/itinerary-generator/scripts/cluster_locations.py) for clustering nearby locations together.
- Use [travel-priorities.md](.agent/skills/itinerary-generator/references/travel_priorities.md) to select the best 3–4 stops per day from the clusters.
- Generate the plan using [itinerary-template.md](.agent/skills/itinerary-generator/assets/itinerary_template.md).

#### 3. itinerary-refiner Skill:
- Context Resolution: Run [context-resolver.py](.agent/skills/itinerary-refiner/scripts/context_resolver.py) to map accommodation and user preference locations to active session state.
- Before calling any maps or calculation tools, invoke [policy-server.py](.agent/skills/itinerary-refiner/scripts/policy_server.py) to ensure the action is permitted under policies.yaml.
- Run [validate-updates.py](.agent/skills/itinerary-refiner/scripts/validate_updates.py) to check for violations of "Human-Centric Buffer Standards".
- If a rule is violated, return the template from [conflict-message.md](.agent/skills/itinerary-refiner/assets/conflict_message.md).
- For final itinerary commits, present the [vibe-diff.md](.agent/skills/itinerary-refiner/assets/vibe_diff.md) and wait for 'APPROVED' status.

## 🛠️ Tech Stack & Tools
- **LLM / Core AI:** Google Gemini API (gemini-3.5-flash)
- **Agent Framework:** Custom Python implementation
- **External Tools/APIs:** Google Maps API _(not included in current project version)_

## ⚙️ Installation & Setup Instructions
I must say this: WayFinder is currently a really raw agentic structure I've built, but since I've done it from scratch, I can show how I manipulate the basic thinking of the model so that I get what I want. 

Step-1: Install [Antigravity IDE](https://antigravity.google/download). Follow the instructions and sign in through your Google account. The free version will do.

Step-2: Fork my GitHub project into a local folder on your laptop.

Step-3: Open Antigravity in this folder and open the agent or the chatbox (which might already be open) by using the shortcut Ctrl + L.

Step-4: Type "I want to go on a trip to Paris/Lyon for 2/3/5 days, and I need/don't need accommodation." 

That's pretty much how I've got it running up!
But to analyze and summarize what I've done is to mend the wiring. 

## 📊 Evaluation & Results
Although I have this basic agent running, I found no reiterations to run. I have recorded a few demonstration videos for different user prompts:
1. "I want to go on a trip to Lyon, France.": [Video - Lyon - 2 Day Trip - No Accommodation](lyon-2d-no-acc.mp4)
2. "I want to plan a trip to Paris for 2 days": [Video - Paris - 2 Day Trip - No Accommodation](paris-2d-no-acc.mp4)
3. "I am having a few important meetings in the afternoon hours, so I would like the Eiffel Tower to be shifted to night.": [Video - Paris - 2 Day Trip - Refinement](paris-2d-refined.mp4)
4. "Plan me a trip to Lyon. I am already accommodated at a hotel called 'Place des Terreaux'. Plan it for 4 days": [Video - Lyon - 4 Day Trip - With Accommodation](lyon-4d-with-acc)

Although they take some time to analyze and provide results, the results they provide are pretty much considerable and perfectly aligned with my stated constraints. Here are two sample itineraries that my agent generated:
- [Lyon-Trip-Itinerary](lyon_trip_itinerary.md)
- [Paris-Trip-Itinerary](paris_trip_itinerary.md)

## 🔮 Future Roadmap
Summing up, this really requires a LOT of toning and perfection. I aimed to succeed in understanding the creation of agentic structures, at least the basic foundation of them, which I successfully captured. There are a lot of things that run through my mind for improvement, but I am facing a crunch here with deadlines, so I list them out for my WayFinder 2.0:
- **_A2UI concepts_** for better itinerary templates and modification: You see the visiting places structured out in a template you really like, and you can modify anything there itself!
- **_Accommodation Bookings_**: I wonder if I can include the transaction protocols to book the hotel rooms from WayFinder itself! I have this crazy idea of giving users a discount or 1+1 free offers on something, which might make this more interesting.
- **_Tickets and travel reservations_**: This might be slightly related to the above point, but it is with respect to the tickets and reservations that some visiting places might require. This might include stating things that release beforehand, say something like bookings in advance. I could also charge a promotion fee from the hotels or tourism places that would become another source of income to me!
- **_Google Maps and Accommodation MCP Servers_**: This should have been included in this version, but I am still figuring things out, so this shall be a major comeback in WayFinder 2.0. They will act as databases with dynamic context for me to book accommodations, or at the least, they could redirect to the supported websites. 
- **_Transactional Protocols_**: This would become a requirement for the 2nd and 3rd point I've mentioned above. We need implementations of the A2A (Agent-to-Agent) protocol for marketing my agent, AP2 (Agents Payments Protocol), and UCP (Universal Commerce Protocol) for financial transaction purposes. 

## 👥 Acknowledgments
This has been a great learning experience for me. Thank you, Kaggle and Google, for giving amazing resources and helping me try different things out once in a while! Looking for my WayFinder 2.0 ideas to find me soon!
