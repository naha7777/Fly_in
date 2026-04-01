_This project has been created as part of the 42 curriculum by anacharp_

# Fly_in

## Description

**Fly_in** is a routing system that manages a fleet of drones and guides them safely from a *start zone* to an *end zone* in the **fewest possible simulation turns**. It enforces capacity constraints at every step — both on the zones drones occupy and the connections they travel through — while respecting the specific movement rules of each zone type.

---

### Zone types

| Type | Behavior |
|------|----------|
| **Blocked** | Impassable — no drone may ever enter. Any path using it is invalid. |
| **Restricted** | Costs 2 turns to enter. The drone occupies the incoming connection during transit and must arrive at the destination on the next turn — it cannot wait on the connection. |
| **Priority** | Costs 1 turn. Must be prioritized in pathfinding when it does not increase the total turn count. |
| **Normal** | Default type (applied automatically when no type is specified). Costs 1 turn. |

---

### Zone & connection attributes

| Entity | Attributes | Default capacity |
|--------|------------|-----------------|
| **Zone** | name, color, coordinates, type, max_drones | 1 drone |
| **Connection** | name, source zone, target zone, max_link_capacity | 1 drone |

---

### Occupancy rules

- By default, a zone may contain at most **1 drone** per turn.
- The **start zone** is an exception: all drones begin here and may share the space initially.
- The **end zone** is an exception: multiple drones can arrive and are considered delivered.
- Drones moving out of a zone free up capacity for that same turn.

---

### Goal

Move **all drones** from the start zone to the end zone in the fewest possible turns. Before planning any route, the system verifies that a valid path exists through the graph of connections. At every turn, zone and connection capacities are respected — no zone or connection may hold more drones than its configured maximum simultaneously.

## Instructions

Install uv, virtual environment and dependencies :
```bash
make install
```
Execution :
```bash
uv run python fly_in.py map.txt
```
or
```bash
make run
```
`make run` use the first easy map, to test other map you will need to modifie the Makefile or the map itself.

## Algorithm Explanation

### Pathfinding approach

The routing system uses **Edmonds-Karp** (BFS-based Ford-Fulkerson) to compute the maximum flow through the zone network before the simulation starts.

Each zone is split into two nodes (`zone_in` and `zone_out`) connected by an internal edge whose capacity equals the zone's `max_drones`. This technique, called **node splitting**, allows the algorithm to treat zone occupancy constraints exactly like connection capacity constraints inside a single unified matrix.

The capacity matrix **C** is built as follows:
- For each zone: `C[zone_in][zone_out] = max_drones`
- For each connection: `C[zone_A_out][zone_B_in] = max_link_capacity` (bidirectional)
- `blocked` zones are never added to the matrix
- `start` and `end` zones use `nb_drones` as their internal capacity since they are exceptions to the occupancy rules

Edmonds-Karp then runs BFS repeatedly on the residual graph until no augmenting path exists, producing a flow matrix **F** that encodes how many drones can simultaneously traverse each edge. Paths are extracted from F by running a secondary BFS that follows only edges where `F[u][v] > 0`, draining the flow after each extraction.

The result is an ordered list of paths — one per drone slot — that collectively respect every capacity constraint in the map.

### Turn-based simulation

Once paths are assigned to drones, the simulation proceeds turn by turn:
- Each drone advances to the next zone on its path if capacity allows
- `restricted` zones cost **2 turns**: the drone occupies the incoming connection for one turn before entering
- `priority` zones cost **1 turn** and are preferred during path assignment
- If a drone cannot move (zone full), it waits in place and is omitted from that turn's output
- The simulation ends when all drones have reached the end zone

## Visual Representation

The simulation provides two complementary outputs, one is built with **Arcade**.

### Terminal output

First the terminal prints the standard simulation output as required by the subject:
- Each line represents one turn: `D1-zone D2-zone ...`
- Stationary drones are omitted from the output
Together these two outputs give a complete picture of the simulation: the terminal provides a precise log of every movement, while the graphical interface makes it immediately intuitive to understand how drones flow through the network and where bottlenecks occur.

### Graphical interface
With the terminal output, i created a graphical interface displays the zone network using the coordinates defined in the map file:
- Each zone is drawn as a **colored circle** using the color specified in its metadata (or black if a color is not specified)
- Connections are drawn as **edges** between nodes
- Each drone is represented as a **little black circle** that moves along the edges turn by turn
- Name's zone are under the zones
- Zone's capacity max capacity and occupancy are written upper the zones
The current turn number is displayed in the window header

## Input and output examples
For this input :
```bash
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

This is the expected output :
```bash
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

## Resources
### Documentation
#### Algorithme d'Edmonds-Karp
- https://www.youtube.com/watch?v=eLcdEcIjijs
- https://cp-algorithms.com/graph/edmonds_karp.html#:~:text=Edmonds%2DKarp%20algorithm%20is%20just,independently%20of%20the%20maximal%20flow.
- https://fr.wikipedia.org/wiki/Algorithme_d%27Edmonds-Karp
- https://www.youtube.com/watch?v=M6Mq_jRqblQ
- https://github.com/anxiaonong/Maxflow-Algorithms/blob/master/Edmonds-Karp%20Algorithm.py

#### Arcade
- https://api.arcade.academy/en/stable/
- https://realpython.com/platformer-python-arcade/#installing-python-arcade

### AI Usage
AI was used for the following tasks :
- help for debugging
- help for translation (docstrings, readme)
- help understanding mypy
- better understanding certain things in Python
- help resolving arcade versions problems
