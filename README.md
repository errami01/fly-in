*This project has been created as part of the 42 curriculum by aberrami*
# Fly-in
## Description
Fly-in is a drone traffic simulation system designed to coordinate the movement of multiple drones through a network of interconnected hubs.

The objective of the project is to safely route drones from a designated start hub to a destination hub while respecting operational constraints such as:

- Hub capacities
- Connection capacities
- Priority and restricted zones
- Simultaneous drone movement
- Traffic congestion management

The system parses a network map description, builds an internal graph representation, computes optimal routes, and executes a turn-based simulation that moves drones through the network.

A visualization module provides a graphical representation of the network and simulation replay, allowing users to observe drone movements, network utilization, and capacity constraints in real time.
## Features
### Network Parsing
The parser supports:

- Drone count definition
- Start and end hubs
- Standard hubs
- Priority hubs
- Restricted hubs
- Connection capacities
- Hub capacities
- Hub color metadata

Example:
```bash
nb_drones: 3

start_hub: start 0 0 
end_hub: end 10 10 
hub: A 1 1 [zone=priority color=red max_drones=2]

connection: start-A [max_link_capacity=2] 
connection: A-end
```
### Pathfinding

The system computes routes using Dijkstra's shortest path algorithm.

Additional support exists for generating alternative paths in order to:

- Distribute traffic
- Reduce congestion
- Increase network utilization
- Support multiple simultaneous drones

### Drone Simulation

The simulation engine supports:

- Simultaneous drone movement
- Turn-based execution
- Hub capacity constraints
- Connection capacity constraints
- Restricted-zone transit handling
- Multiple drones sharing routes when capacities allow
- Traffic conflict resolution

Each simulation turn evaluates all drones and determines which moves can be executed without violating network constraints.

### Replay System

Every simulation turn is recorded.

Recorded information includes:

- Turn number
- Executed drone moves
- Route progression

The replay system allows deterministic playback of completed simulations.

### Visualization

A Pygame-based visualization module displays:

- Network graph
- Hub locations
- Connections
- Drone positions
- Turn counter
- Replay controls

The visualization can replay completed simulations step-by-step or automatically.

## Instructions
### Requirements
- Python 3.10+
- uv

### Installation
Clone the repository:
```bash
git clone <repository-url> fly-in
cd fly-in
```
Install dependencies:
```bash
uv sync
```
### Running the Simulation
Execute a map file:
```bash
uv run python -m src.main maps/example.txt
```
### Visual Mode

Run the simulation with graphical replay:
```bash
uv run python -m src.main maps/example.txt --visual
```
Key     |	Action
|------:|---------
SPACE	|Advance one turn
P	    |Play / Pause replay
R	    |Reset replay
ESC	    |Quit

### Build Validation

Run project checks:
```bash
make lint
```
Run the complete project:
```bash
make run MAP=maps/example.txt
```
## Algorithm Choices and Implementation Strategy
### Graph Representation

The drone network is represented as an undirected graph.

Nodes represent hubs and zones.

Edges represent connections between hubs.

This representation was chosen because:

- It allows efficient shortest-path algorithms.
- It naturally models transportation networks.
- It simplifies capacity and occupancy tracking.

### Dijkstra Shortest Path

Dijkstra's algorithm was selected because:

- Edge costs are non-negative.
- The network is relatively small.
- Optimal shortest paths are required.

Advantages:

- Deterministic results
- Efficient execution
- Easy integration with capacity-aware routing

Time complexity:

O((V + E) log V)
where:

- V = number of hubs
- E = number of connections

### Alternative Route Generation

Multiple candidate routes are generated to prevent all drones from selecting the same path.

This improves:

- Throughput
- Network utilization
- Congestion avoidance

Route scoring considers:

- Path cost
- Hub capacities
- Network bottlenecks
- Existing route assignments

### Turn-Based Simulation

A turn-based model was selected because it:

- Matches the project specification
- Simplifies collision detection
- Makes capacity validation deterministic
- Enables replay generation

Each turn performs:

1. Route planning
2. Move validation
3. Capacity checking
4. State updates
5. Replay recording

### Capacity Management

The simulation validates:

* Hub Capacity

occupancy <= max_drones

This prevents overcrowding inside hubs.

* Connection Capacity

usage <= max_link_capacity

This prevents excessive traffic on network links.

### Restricted Zone Handling

Restricted zones require drones to remain in transit for additional turns.

The simulation tracks:

- Transit state
- Transit destination
- Connection occupancy

This accurately models slower movement through restricted areas.

## Visual Representation
### Network Graph

The visualization displays the complete drone network.

Each hub is represented by:

- Position
- Name
- Color metadata

Each connection is represented by a line between hubs.

### Drone Visualization

Drones are displayed directly on the graph.

This allows users to observe:

- Route selection
- Traffic distribution
- Congestion effects
- Arrival progress

### Replay Controls

Replay controls allow users to:

- Pause execution
- Advance manually
- Restart simulations

This is useful for debugging and analyzing traffic decisions.

### User Experience Benefits

The visualization significantly improves usability by:

- Making drone movements easier to understand
- Highlighting capacity constraints
- Showing congestion visually
- Providing deterministic replay
- Supporting debugging and validation

Without visualization, understanding multi-drone interactions would require manually analyzing simulation logs.

## Resources
### Youtube Tutorials and Articles
- Real Python – Graph Algorithms
- Python Priority Queue Documentation
- Pygame Getting Started Guide

### Use of AI
Artificial Intelligence tools were used as a development assistant during the project.

AI assistance was used for:

- Architecture discussions
- Design reviews
- Algorithm validation
- Refactoring suggestions
- Debugging support
- Visualization design ideas
- Documentation preparation

All implementation decisions, testing, debugging, integration, and final validation were performed by the author.

AI-generated suggestions were reviewed, adapted, and verified before inclusion in the final project.
