import json
import time
import csv
from random import randint

def create_config(data_structure, rows, cols):
    """ Generate a single configuration file with random entrances and exits. """
    entrances = [[randint(0, rows-1), -1], [randint(0, rows-1), cols]]
    exits = [[randint(0, rows-1), -1], [randint(0, rows-1), cols]]
    config = {
        "dataStructure": data_structure,
        "rowNum": rows,
        "colNum": cols,
        "entrances": entrances,
        "exits": exits,
        "generator": "recur",
        "visualise": False
    }
    return config

def run_maze(config):
    from maze.maze import Maze
    from maze.arrayMaze import ArrayMaze
    from maze.graphMaze import GraphMaze
    from maze.util import Coordinates
    from generation.recurBackGenerator import RecurBackMazeGenerator

    ds_approach = config['dataStructure']
    rowNum = config['rowNum']
    colNum = config['colNum']
    entrances = config['entrances']
    exits = config['exits']

    if ds_approach == 'array':
        maze = ArrayMaze(rowNum, colNum)
    elif ds_approach in ['adjlist', 'adjmat']:
        maze = GraphMaze(rowNum, colNum, ds_approach)

    for [r, c] in entrances:
        maze.addEntrance(Coordinates(r, c))
    for [r, c] in exits:
        maze.addExit(Coordinates(r, c))

    generator = RecurBackMazeGenerator()
    start_time = time.perf_counter()
    generator.generateMaze(maze)
    end_time = time.perf_counter()

    return end_time - start_time

def test_maze_performance(data_structures, sizes_or_shapes, num_runs, test_type='size'):
    filename = f'maze_{test_type}_performance.csv'
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        headers = ['Data Structure', 'Configuration'] + [f'Run {i + 1}' for i in range(num_runs)] + ['Average Time (s)']
        writer.writerow(headers)

        for ds in data_structures:
            for config in sizes_or_shapes:
                if test_type == 'size':
                    rows, cols = config, config
                    config_label = f"{config}x{config}"
                else:
                    rows, cols = config
                    config_label = f"{rows}x{cols}"

                runtimes = []
                for run in range(num_runs):
                    maze_config = create_config(ds, rows, cols)
                    runtime = run_maze(maze_config)
                    runtimes.append(runtime)

                avg_runtime = sum(runtimes) / num_runs
                writer.writerow([ds, config_label] + runtimes + [avg_runtime])
                print(f"{ds} {config_label}: Avg. Runtime = {avg_runtime:.4f} seconds")

if __name__ == '__main__':
    data_structures = ['array', 'adjlist', 'adjmat']
    num_runs = 20
    sizes = [10, 20, 30, 40, 50, 100, 200]
    shapes = [(10, 10), (100, 1), (1, 100), (50, 2), (25, 4), (20, 5)]

    print("Testing by Increasing Sizes:")
    test_maze_performance(data_structures, sizes, num_runs, test_type='size')

    print("\nTesting by Varying Shapes:")
    test_maze_performance(data_structures, shapes, num_runs, test_type='shape')
