import pygame
from graph import Node, Graph
from random import randint, random


WIDTH = 1000
HEIGHT = 1000
NUM_X = 50
NUM_Y = 50


def generate_grid(width: int, height: int, num_x: int, num_y: int) -> list[[Node, ...], ...]:
    """
    Given the dimensions and number density of grid points in the desired grid, this function creates a set
    with Nodes corresponding to each grid point

    :param width: Width of grid to be generated
    :param height: Height of grid to be generated
    :param num_x: X Spacing of grid points
    :param num_y: Y spacing of grid points
    :return: Set including Nodes corresponding to each grid point in the generated grid
    """
    grid = []
    rect_width = width/num_x
    rect_height = height/num_y
    obstacle_chance = 0.4

    for row in range(num_x):
        columns = []
        for col in range(num_y):
            pos_x = row*rect_width
            pos_y = col*rect_height

            if random() < obstacle_chance:
                node_type = 'Obstacle'
            else:
                node_type = 'Unexpanded'

            node = Node((pos_x, pos_y), width=rect_width, height=rect_height, i=row, j=col, node_type=node_type)
            columns.append(node)
        grid.append(columns)
    return grid


def get_node_at_point(grid: list[[Node, ...], ...], point: tuple[float, float]) -> Node:
    """
    Finds the node that contains the provided point
    :param grid: set of nodes to look through
    :param point: point contained within the given node
    :return: Node that contains the point specified
    """
    # This is pretty inefficient atm, but it runs like twice and I can improve it later
    for row in grid:
        for node in row:
            if node.rect.collidepoint(point):
                return node
    else:  # Only executes if all nodes are looped over
        raise Exception(f'No node found containing point {point}')


def setup_problem(width, height, num_x, num_y):
    start_loc = (randint(1, WIDTH // 2), randint(1, HEIGHT // 2))
    goal_loc = (randint(WIDTH // 2, WIDTH), randint(HEIGHT // 2, HEIGHT))
    nodes = generate_grid(WIDTH, HEIGHT, NUM_X, NUM_Y)
    start_node = get_node_at_point(nodes, start_loc)
    goal_node = get_node_at_point(nodes, goal_loc)

    start_node.g = 0
    start_node.set_h(goal_node)

    return Graph(start_node, goal_node, nodes)


def main():
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    # Setup 'problem' (grid, start and ending nodes, and obstacles)
    graph = setup_problem(WIDTH, HEIGHT, NUM_X, NUM_Y)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    graph = setup_problem(WIDTH, HEIGHT, NUM_X, NUM_Y)

        graph.search_step()

        screen.fill('black')

        graph.draw_graph(screen)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
