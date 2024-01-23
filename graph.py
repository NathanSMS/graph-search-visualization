from __future__ import annotations
from math import sqrt
import pygame


class Node:
    def __init__(self, state: tuple[float, float], width: float, height: float, i: int, j: int, node_type: str = 'Unexpanded'):
        self.i = i
        self.j = j
        self.state = state
        self.width = width
        self.height = height
        self.rect = pygame.Rect(state, (width, height))
        self.surface = pygame.Surface((width, height))
        self.g = None
        self.h = None
        self.parent = None
        self.node_type = node_type

    def __repr__(self):
        return f'i: {self.i}, j: {self.j}, g: {self.g}, h: {self.h}'

    def backtrack(self):
        path = [self]
        ancestor = self.parent
        while ancestor is not None:
            path.append(ancestor)
            ancestor = ancestor.parent
        return path

    def set_h(self, goal_node: Node) -> None:
        """
        Sets node h value to L2 norm distance between node and goal
        :param goal_node: Node representing goal state
        :return: None
        """
        sq_dist = 0
        # For each dimension in state
        for dim in zip(self.state, goal_node.state):
            # add square distance
            sq_dist += (dim[0] - dim[1])**2
        self.h = sqrt(sq_dist)

    def calc_f(self, mode: str, goal_node: Node):
        if self.h is None:
            self.set_h(goal_node)
        mode = mode.upper()  # Make sure input is all caps
        if mode == 'DFS':
            ...
        elif mode == 'BFS':
            ...
        elif mode == 'UCS':
            ...
        elif mode == 'A*':
            return self.g + self.h
        else:
            raise NotImplementedError

    def update_parent(self, prospective_parent: Node, travel_cost: float) -> None:
        # If self has no parent or if prospective parent gives a cheaper path than the current parent
        # then update the parent and cost
        if self.parent is None and self.node_type != 'Start':
            self.parent = prospective_parent
            self.g = prospective_parent.g + travel_cost
        elif self.g > prospective_parent.g + travel_cost:
            self.parent = prospective_parent
            self.g = prospective_parent.g + travel_cost

    def draw(self, global_screen: pygame.display) -> None:
        node_type_dict = {'Unexpanded': (52, 52, 52),
                          'Fringe': (255, 255, 0),
                          'Expanded': (255, 255, 255),
                          'Start': (0, 255, 0),
                          'Goal': (255, 0, 0),
                          'Obstacle': (0, 0, 0),
                          'Path': (0, 0, 255)}  # Sets color based on type of node
        color = node_type_dict[self.node_type]

        # Draws a slightly smaller rectangle of color with black edges to emphasize grid lines
        inner_surf = pygame.Surface((self.width*0.9, self.height*0.9))  # Inner rects dimensions are 90% of outer
        inner_surf.fill(color)
        self.surface.fill((0, 0, 0))
        self.surface.blit(inner_surf, (0.05*self.width, 0.05*self.height))  # Spaced in the center of rect
        global_screen.blit(self.surface, self.state)


class Graph:
    def __init__(self, start_node: Node, goal_node: Node, nodes: list[[Node, ...], [Node, ...], ...]):
        self.start_node = start_node
        start_node.node_type = 'Start'

        self.goal_node = goal_node
        goal_node.node_type = 'Goal'

        self.grid = nodes

        # Add all nodes from the grid to the unexpanded nodes set, then remove the start node
        self.unexpanded_nodes = set()
        for row in self.grid:
            self.unexpanded_nodes.update(set(row))
        self.unexpanded_nodes.discard(start_node)

        self.expanded_nodes = set()
        self.fringe = {start_node}  # Fringe will always start as start_node and this will be first expanded node
        self.mode = 'A*'
        self.path = []
        self.isSearching = True

    def set_search_mode(self, mode: str):
        valid_modes = {'A*', 'BFS', 'DFS', 'UCS'}
        if mode.upper() in valid_modes:
            self.mode = mode

    def search_step(self):
        if self.isSearching:
            lowest_cost_node = None

            if self.fringe:  # If the fringe is not empty
                for node in self.fringe:  # Iterate through all nodes in fringe to find lowest cost node
                    if lowest_cost_node is None:
                        lowest_cost_node = node
                    elif node.calc_f(mode=self.mode, goal_node=self.goal_node) < lowest_cost_node.calc_f(mode=self.mode,
                                                                                                         goal_node=self.goal_node):
                        lowest_cost_node = node

                if lowest_cost_node is self.goal_node:  # Ending condition for A* is if goal node is up to be expanded
                    # Backtrack to get path
                    self.path = lowest_cost_node.backtrack()
                    for node in self.path:
                        if node is not self.goal_node and node is not self.start_node:
                            node.node_type = 'Path'
                    self.isSearching = False
                    print('Goal Node Found!')
                else:
                    self.expand_node(lowest_cost_node)

            else:  # If the fringe is empty
                self.isSearching = False
                print('No path exists between the start and goal node')

    def draw_graph(self, global_screen):
        for row in self.grid:
            for node in row:
                node.draw(global_screen)

    def expand_node(self, node: Node):
        # Remove node from fringe and add to expanded nodes
        self.fringe.discard(node)
        self.expanded_nodes.add(node)

        # Get all neighbors of node
        neighbors = []
        if node is not self.start_node and node is not self.goal_node:
            node.node_type = 'Expanded'

        # Get valid neighbors for node
        # -1 and +2 because range() includes the start but excludes the end
        for i in range(node.i - 1, node.i + 2):
            for j in range(node.j - 1, node.j + 2):
                # Assign cost to node depending on if its directly adjacent or diagonal to passed node
                if (node.i == i) and (node.j == j):
                    continue  # Don't add the passed node to neighbors
                elif (i == -1) or (j == -1):
                    continue
                elif (node.i != i) and (node.j != j):
                    cost = 1.4  # If node is diagonal in the grid cost should be sqrt(2), 1.4 is close enough
                else:
                    cost = 1
                try:
                    curr_neighbor = self.grid[i][j]
                except IndexError:
                    continue

                # If neighbor hasn't been expanded yet, add to fringe
                if curr_neighbor not in self.expanded_nodes and curr_neighbor.node_type != 'Obstacle':
                    # Change nodes current cost to the cost of getting to this node from start plus cost
                    if curr_neighbor is not self.goal_node:
                        curr_neighbor.node_type = 'Fringe'
                    self.fringe.add(curr_neighbor)

                curr_neighbor.update_parent(node, travel_cost=cost)


if __name__ == '__main__':
    screen = pygame.display.set_mode((1000, 1000))
