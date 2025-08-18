
1. Breadth-First Search (BFS) - The Level-by-Level Explorer

The Core Idea: BFS explores the graph in expanding circles. It starts at the beginning and explores all its immediate neighbors first. Then, for each of those neighbors, it explores their immediate neighbors, and so on. It checks everything one step away, then everything two steps away, then three, ensuring it doesn't get too far from the start too quickly.

Analogy: Finding a Classmate in a School 
Imagine you're looking for a friend in a multi-story school building. Using a BFS approach, you would:

    Search the entire floor you are currently on (Level 1).

    If you don't find them, you go up to the next floor and search that entire floor (Level 2).

    You continue this process, completely searching each floor before moving to the next.

This guarantees that you'll find your friend on the closest possible floor to your starting point.

How It Works Technically:

    It uses a Queue data structure, which is "First-In, First-Out" (FIFO).

    You add the starting state to the queue.

    Then you loop: take the first item out of the queue, check if it's the goal, and if not, add all of its unvisited neighbors to the back of the queue.

Key Characteristics:

    Completeness: Yes. If a solution exists, BFS is guaranteed to find it.

    Optimality: Yes. It will always find the shortest path (the one with the fewest steps) first. This is its greatest strength.

    Memory: Very high. BFS must store every node at the current level of the search tree in memory. If the search space is wide, this can consume a huge amount of RAM.

2. Depth-First Search (DFS) - The Deep Diver

The Core Idea: DFS is an aggressive, single-minded explorer. It picks one path and follows it as deep as it can go. If it hits a dead end or a previously visited state, it backtracks to the last choice it made and tries the next available path.

Analogy: Solving a Maze 
Imagine you're in a corn maze. Using a DFS approach, you would:

    Pick a path and keep walking down it, always taking the first available turn.

    You continue until you hit a dead end.

    When you hit a dead end, you walk back to your last intersection and take the next path you haven't tried yet.

    You repeat this until you find the exit.

You might find the exit quickly, or you might explore a very long, winding path on the wrong side of the maze first.

How It Works Technically:

    It uses a Stack data structure, which is "Last-In, First-Out" (LIFO).

    You push the starting state onto the stack.

    Then you loop: pop an item from the stack, check if it's the goal, and if not, push all of its unvisited neighbors onto the top of the stack.

Key Characteristics:

    Completeness: No. In an infinite graph (or one with cycles), DFS can get stuck going down an infinitely long path and never find a solution, even if one exists. It is complete for finite graphs.

    Optimality: No. The first solution it finds is unlikely to be the shortest one. It depends entirely on which path it happens to explore first.

    Memory: Very low. DFS only needs to store the current path it's exploring. This makes it extremely memory-efficient compared to BFS.

3. Iterative Deepening DFS (ID-DFS) - The Best of Both Worlds

The Core Idea: ID-DFS is a hybrid strategy that combines the strengths of BFS and DFS. It wants the guaranteed shortest path of BFS but with the low memory usage of DFS. It achieves this by running DFS multiple times, but with a limited depth.

Analogy: A Search and Rescue Operation 
Imagine a rescue team searching a collapsed building floor by floor. Using an ID-DFS approach, they would:

    Run 1 (Limit = 0): Search only the ground floor.

    Run 2 (Limit = 1): Restart and search the ground floor AND the 1st floor.

    Run 3 (Limit = 2): Restart again and search the ground, 1st, and 2nd floors.

This seems repetitive, but it ensures they find a survivor on the lowest possible floor (shortest path) without needing a huge team to search all floors simultaneously (low memory).

How It Works Technically:

    It uses a loop that controls a depth_limit.

    Inside the loop, it performs a complete DFS, but it's not allowed to explore any deeper than the depth_limit.

    If no solution is found, the depth_limit is increased by one, and the entire DFS process starts over from the beginning.

Key Characteristics:

    Completeness: Yes. Like BFS, it is guaranteed to find a solution if one exists.

    Optimality: Yes. Because it explores level by level, it finds the shortest path, just like BFS.

    Memory: Very low. Since each iteration is just a depth-limited DFS, it has the same excellent memory profile as DFS.




### Breadth-First Search (BFS) Pseudocode

BFS uses a **queue** (First-In, First-Out) to explore level by level, guaranteeing the shortest path.

```
FUNCTION solve_with_bfs():
  // 1. Initialization
  CREATE a queue
  CREATE a list to track visited_states
  CREATE startState with values (0, 0)
  
  ADD startState to queue
  ADD startState to visited_states

  // 2. Main Loop
  // The loop continues as long as there are states to explore.
  LOOP while queue is not empty:
    // a. Get the next state to check from the FRONT of the queue.
    currentState = REMOVE front item from queue

    // b. Goal Check
    IF currentState is the goal (e.g., contains 2 liters) THEN
      DISPLAY "Solution Found!"
      RECONSTRUCT and PRINT path from startState to currentState
      RETURN // Exit the function
    END IF

    // c. Generate Neighbors
    // Find all possible next states from the current one.
    FOR EACH possible_action (Fill, Empty, Pour):
      nextState = APPLY action to currentState
      
      // d. Add to Queue if New
      // Only explore this new state if we haven't seen it before.
      IF nextState has not been visited THEN
        ADD nextState to visited_states
        ADD nextState to the BACK of the queue
      END IF
    END FOR
  END LOOP

  // 3. No Solution
  // If the loop finishes, it means we explored everything without success.
  DISPLAY "No solution found."
END FUNCTION
```

-----

### Depth-First Search (DFS) Pseudocode

DFS uses a **stack** (Last-In, First-Out) to explore one path as deeply as possible before backtracking.

```
FUNCTION solve_with_dfs():
  // 1. Initialization
  CREATE a stack
  CREATE a list to track visited_states
  CREATE startState with values (0, 0)

  ADD startState to stack
  ADD startState to visited_states

  // 2. Main Loop
  // The loop continues as long as there are paths to explore.
  LOOP while stack is not empty:
    // a. Get the next state from the TOP of the stack.
    currentState = REMOVE top item from stack

    // b. Goal Check
    IF currentState is the goal THEN
      DISPLAY "Solution Found!"
      RECONSTRUCT and PRINT path from startState to currentState
      RETURNFUNCTION
    END IF

    // c. Generate Neighbors
    FOR EACH possible_action (Fill, Empty, Pour):
      nextState = APPLY action to currentState

      // d. Add to Stack if New
      // The only difference from BFS is adding to a stack instead of a queue.
      IF nextState has not been visited THEN
        ADD nextState to visited_states
        ADD nextState to the TOP of the stack
      END IF
    END FOR
  END LOOP

  // 3. No Solution
  DISPLAY "No solution found."
END FUNCTION
```

-----

### Iterative Deepening DFS (ID-DFS) Pseudocode


```
FUNCTION solve_with_iddfs():
  // 1. Outer Loop for Depth
  // Start with a depth limit of 0 and increase it indefinitely.
  FOR depth_limit from 0 to infinity:
    // a. Run a Depth-Limited Search (DLS) for the current limit.
    found_solution = CALL depth_limited_search(depth_limit)

    // b. Check Result
    IF found_solution is TRUE THEN
      RETURN // The DLS function will have already printed the path.
    END IF
  END FOR
END FUNCTION


 depth_limited_search(limit):
  // This is just like DFS, but with one extra check.
  
  // 1. Initialization
  CREATE a stack
  CREATE a list to track visited_states for THIS iteration
  CREATE startState with values (0, 0) and depth 0

  ADD startState to stack
  ADD startState to visited_states

  // 2. Main Loop
  LOOP while stack is not empty:
    currentState = REMOVE top item from stack

    // a. Goal Check
    IF currentState is the goal THEN
      DISPLAY "Solution Found at depth", limit
      RECONSTRUCT and PRINT path
      RETURN TRUE // Signal that we found it.
    END IF

    // b. Depth Check (The Key Difference)
    // Only generate neighbors if we are within the depth limit.
    IF currentState.depth < limit THEN
      FOR EACH possible_action:
        nextState = APPLY action to currentState
        IF nextState has not been visited THEN
          ADD nextState to visited_states
          ADD nextState to the TOP of the stack
        END IF
      END FOR
    END IF
  END LOOP

  // 3. No solution found at this depth
  RETURN FALSE // Signal to the main ID-DFS loop to increase the limit.
END FUNCTION
```