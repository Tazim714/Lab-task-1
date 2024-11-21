import pygame
import sys

# Make sure to update the path to where agent.py and environment.py are located
# sys.path.append('path_to_directory_containing_agent_and_environment')

from agent import Agent
from environment import Environment

# Initialize Pygame
pygame.init()

# Constants for the display and environment setup
GRID_SIZE = 20
NUM_TASKS = 10  # Specify the number of tasks
NUM_BARRIERS = 30  # Specify the number of barriers
WINDOW_WIDTH = 1000  # Increased window width for task information
WINDOW_HEIGHT = 600
GRID_PIXEL_SIZE = 30

# Setup the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Added space for task info
pygame.display.set_caption('Pathfinding Simulation')

# Create environment and agent with the specified number of tasks and barriers
environment = Environment(GRID_SIZE, NUM_TASKS, NUM_BARRIERS)
agent = Agent(environment, GRID_PIXEL_SIZE)

def draw_task_info():
    """Draw task information directly on the screen."""
    font = pygame.font.Font(None, 36)
    # Task status text
    task_status_text = f"Tasks Completed: {agent.task_completed}"
    position_text = f"Position: ({agent.position[0]}, {agent.position[1]})"
    completed_tasks_text = f"Completed Tasks: {', '.join(map(str, agent.completed_tasks))}"

    # Rendering the text
    task_status_surface = font.render(task_status_text, True, (0, 0, 0))
    position_surface = font.render(position_text, True, (0, 0, 0))
    completed_tasks_surface = font.render(completed_tasks_text, True, (0, 0, 0))

    # Display the text on the right side of the screen (within bounds)
    screen.blit(task_status_surface, (GRID_SIZE * GRID_PIXEL_SIZE + 20, 20))
    screen.blit(position_surface, (GRID_SIZE * GRID_PIXEL_SIZE + 20, 60))
    screen.blit(completed_tasks_surface, (GRID_SIZE * GRID_PIXEL_SIZE + 20, 100))

def draw_grid_with_numbers():
    """Draw the grid and task numbers where the agent will go."""
    font = pygame.font.Font(None, 36)
    
    # Draw grid and tasks (green) and barriers (red)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * GRID_PIXEL_SIZE, y * GRID_PIXEL_SIZE, GRID_PIXEL_SIZE, GRID_PIXEL_SIZE)
            if environment.grid[x][y] == 1:
                pygame.draw.rect(screen, (200, 0, 0), rect)  # Barriers are red
            elif environment.grid[x][y] == 2:
                pygame.draw.rect(screen, (0, 200, 0), rect)  # Tasks are green
                # Display the task number on green cells
                task_number = environment.task_locations.get((x, y), None)
                if task_number:
                    task_number_surface = font.render(str(task_number), True, (0, 0, 0))
                    screen.blit(task_number_surface, (x * GRID_PIXEL_SIZE + GRID_PIXEL_SIZE // 3, y * GRID_PIXEL_SIZE + GRID_PIXEL_SIZE // 3))
            elif environment.grid[x][y] == 0:
                pygame.draw.rect(screen, (255, 255, 255), rect)  # Completed tasks turn white
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid lines

def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    simulation_started = False
    last_move_time = 0
    MOVEMENT_DELAY = 1000  # 1 second between moves

    button_rect = pygame.Rect(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50, 140, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos) and not simulation_started:
                simulation_started = True

        screen.fill((255, 255, 255))  # Background color

        # Draw grid with task numbers and green color
        draw_grid_with_numbers()

        # Draw agent
        agent.draw(screen)

        # Draw the task information directly on the screen (no extra panel)
        draw_task_info()

        # Draw the start button if simulation hasn't started
        if not simulation_started:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                button_color = (0, 255, 0)  # Hover color
            else:
                button_color = (0, 200, 0)  # Normal color
            pygame.draw.rect(screen, button_color, button_rect)
            button_text = font.render("Start", True, (255, 255, 255))
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)
        else:
            # Automatic movement with delay
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > MOVEMENT_DELAY:
                if not agent.moving and environment.task_locations:
                    # Find the nearest task
                    agent.find_nearest_task()
                elif agent.moving:
                    agent.move()
                    # Remove the task number and green color once the task is completed
                    current_pos = tuple(agent.position)
                    if current_pos in environment.task_locations:
                        task_number = environment.task_locations.pop(current_pos)
                        environment.grid[agent.position[0]][agent.position[1]] = 0  # Change grid to white after completion
                        agent.completed_tasks.append(task_number)
                        agent.task_completed += 1
                last_move_time = current_time

        # Update the display
        pygame.display.flip()

    # Quit Pygame properly
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
