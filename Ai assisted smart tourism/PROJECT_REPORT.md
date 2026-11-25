# Project Report: AI-Based Smart Tourism and Travel Management System

## 1. Introduction
Tourism planning requires travelers to discover destinations, compare options, organize daily activities and estimate expenses. This project provides a unified prototype to support those tasks.

## 2. Problem Statement
Travelers may need to consult multiple sources to find destination information and manually organize an itinerary and budget. This process can be time-consuming, especially when travel interests, duration and spending limits differ.

## 3. Objectives
- Provide searchable destination information.
- Generate a day-wise itinerary using destination, duration and interests.
- Estimate an approximate trip budget.
- Answer common travel-planning questions.
- Save and manage generated trip plans.

## 4. Proposed Solution and Novelty
The system combines destination discovery, preference-based itinerary generation, budget estimation, a travel assistant and persistent trip storage in one web interface. The recommendation logic reorders destination highlights based on selected interests and produces a structured plan.

## 5. Tools and Technologies
- Python: application logic
- Streamlit: interactive web interface
- SQLite: local persistent storage
- VS Code: development environment
- ChatGPT or another AI coding assistant: may be used to explain, scaffold, debug and document code; record the actual prompts used by the team.

## 6. System Architecture
User → Streamlit UI → AI/recommendation engine → destination data → itinerary and budget output → SQLite trip storage.

## 7. Modules
1. Home dashboard
2. Destination explorer
3. AI trip planner
4. Travel assistant
5. Saved trips manager
6. Project information

## 8. Testing
| Test case | Expected result |
|---|---|
| Open application | Home page loads |
| Filter destinations | Matching destinations appear |
| Search an unknown place | No-results message appears |
| Generate itinerary | Day-wise activities and budget appear |
| Save a trip | Record appears in My Saved Trips |
| Delete a trip | Record disappears |
| Ask packing question | Packing guidance appears |

## 9. Results
The prototype demonstrates destination filtering, itinerary generation, budget estimation, assistant responses and SQLite-based trip management. Add genuine screenshots from the running application before final submission.

## 10. Limitations
The destination catalogue is small and static. Prices and seasons are illustrative. The assistant is rule-based and does not fetch live data or book travel.

## 11. Future Enhancements
Integrate a generative AI API, live maps and route optimization, real-time weather, verified hotel/transport APIs, multilingual support, authentication and admin analytics.

## 12. Conclusion
The project demonstrates how an AI-oriented travel management workflow can bring destination discovery, itinerary planning, budget estimation and trip storage into one application.
