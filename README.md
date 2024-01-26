# 2D Graph Search Algorithm Visualizer

This is a PyGame application for showing the process behind common
graph search algorithms such as A-Star, Depth First Search (DFS), Breath-First Search (BFS), Uniform-Cost Search, 
and Disjkstra's Algorithm (Only A-Star implemented at the moment). The applications generates a 2D grid of specified
size, chooses random starting and goal positions, randomly fills the grid with obstacles, and shows the fringe, 
expanded nodes, and unexpanded nodes through each step in the search. 

## Motivation

I was looking for a project to work on to stay active in programming that I would be able to easily scale up and build 
upon while also keeping up to date with higher level computer science topics. A graph search visualizer ticked all the boxes
as I'll be able to implement multiple algorithms, add UI elements, and work on optimization.

## Future work / Contributing

As of right now, I have yet to implement DFS, BFS, UCS, and Dijkstra's as options in the
graph search. This will consist simply of adding the necessary code to calculate the g, h, and f values corresponding to 
each algorithm.

The application could be improved with better UI such as a starting window where you're able to select which algorithm to be used,
change the window size, change the generated grid size, or even possibly choose different colors for the node highlighting

This may be more of a graphical issue depending on interpretation, but at the moment the algorithm can move through walls diagonally.
Adding a check into the Graph.expand_node() function that checks if both adjacent nodes are obstacles for corner nodes can remedy this.

The final improvement I can come up with at the moment is a better way to generate obstacles. Currently any non-start and non-goal
node is randomly chosen as an obstacle or not when the grid is generated. This approach does not guarantee that a path 
exists between the start and goal nodes, and leads to less than ideal asthetics. A maze generation algorithm would be a great addition,
particularly like the one featured in [this series by The Coding Train](https://www.youtube.com/watch?v=HyK_Q5rrcr4)