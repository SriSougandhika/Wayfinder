# Wayfinder - Agentic Travel Itinerary Planner
A very basic agentic AI-based travel itinerary planner that matches user requirements, recommending places to stay and must-visit places listed out in a schedule, considering enough rest and less burnout. 

## 📌 Problem Statement
- **The Hassle of Travel Planning:** Traditional travel planning is tedious. Handling fragmented data across 10+ tabs, rigid static itineraries, and an inability to handle sudden real-time changes.

- **Why Static AI Fails:** A standard LLM chatbot isn't enough. It cannot handle complex multi-step reasoning and may not suggest timelines that align with enough rest and time for food. 

- **The Goal:** Defining an agent that could keep all these things in mind and have the ability to chart out schedules with less burnout, covering nearby places in a single day with enough gaps for taking rest, might be a possible solution for this.

## 🚀 The Solution & Agentic Capabilities
Now, I don't sit for long hours calculating distances and putting places to visit on day 1, day 2, and so on; I need to ask the agent to do that for me. The MCP (for this project, I have used a mock MCP server), which can be integrated with the Google Maps MCP Server, provides real-time data and up-to-date location status. 
Agentic features will remember all constraints, chart out the itinerary, and refine it spontaneously if required. 
- **Auto-suggest accommodations:** Locates best places to stay over, with all budget categories, and allows the user to choose from them. Also works if accommodations are pre-specified.
- **Autonomy:** Makes decisions without constant user prompting, based on clustering nearby locations and also calculating transit times for real-time mapping. Further, allocates enough time for nightly rest and hours for breakfast, lunch, and dinner. 
- **Dynamic Replanning:** Handles changes like "What if day 2 rains?" and charts out the modified plan, again abiding by all the constraints.

## 🏗️ Architecture & Workflow
<img width="1412" height="634" alt="agent workflow" src="https://github.com/user-attachments/assets/c771a856-6b78-477d-b688-ac8d936f4ca3" />
