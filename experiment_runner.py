import csv
import time
from agent import Mouse
from environment import generate_maze
from levels import MAZE_SIZES

# List of AI methods to test
AI_METHODS = ["random", "greedy", "a_star"]
NUM_RUNS = 30

# CSV Header
CSV_HEADER = ["level", "ai_method", "run", "steps", "time_ms"]

def run_experiments():
    with open("results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADER)

        for level_index, maze_size in enumerate(MAZE_SIZES):
            maze = generate_maze(*maze_size)
            cheese_pos = (maze_size[0] - 1, maze_size[1] - 1)

            for ai_method in AI_METHODS:
                for run in range(1, NUM_RUNS + 1):
                    mouse = Mouse(start_pos=(0, 0))
                    mouse.set_mode(ai_method, cheese_pos, maze)

                    start_time = time.perf_counter()
                    steps = 0

                    while mouse.position != cheese_pos and steps < 1000:
                        mouse.move(maze)
                        steps += 1

                    elapsed_time_ms = (time.perf_counter() - start_time) * 1000  # Convert to ms

                    # Save results
                    writer.writerow([
                        level_index + 1,
                        ai_method,
                        run,
                        steps,
                        round(elapsed_time_ms, 2)
                    ])

                    print(f"Level {level_index + 1}, {ai_method}, Run {run}: {steps} steps, {round(elapsed_time_ms, 2)}ms")

if __name__ == "__main__":
    run_experiments()
