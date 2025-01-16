import pygame
import math
import matplotlib.pyplot as plt
from components import LineFollowingRobot

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Line Following Robot with PID Feedback")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROBOT_COLOR = (255, 0, 0)

line_points = [(100, 300), (200, 300), (300, 300), (400, 300), (500, 300), (600, 300)]
line_width = 5

robot = LineFollowingRobot(k_p=0.1, k_i=0.001, k_d=0.01, set_point=0, base_speed=0.5)

class LineData:
    def is_on_line(self, position, offset):
        sensor_pos = (position[0] + offset[0], position[1] + offset[1])
        _, dist = get_closest_point_on_line(sensor_pos)
        return dist < 5

def get_closest_point_on_line(position):
    x, y = position
    min_dist = float('inf')
    closest_point = None
    
    for i in range(len(line_points) - 1):
        p1 = line_points[i]
        p2 = line_points[i + 1]
        
        line_vec = (p2[0] - p1[0], p2[1] - p1[1])
        point_vec = (x - p1[0], y - p1[1])
        line_len = math.sqrt(line_vec[0]**2 + line_vec[1]**2)
        
        if line_len == 0:
            continue
            
        unit_line = (line_vec[0]/line_len, line_vec[1]/line_len)
        projection_len = point_vec[0]*unit_line[0] + point_vec[1]*unit_line[1]
        projection_len = max(0, min(line_len, projection_len))
        
        closest = (
            p1[0] + unit_line[0]*projection_len,
            p1[1] + unit_line[1]*projection_len
        )
        
        dist = math.sqrt((x - closest[0])**2 + (y - closest[1])**2)
        if dist < min_dist:
            min_dist = dist
            closest_point = closest
            
    return closest_point, min_dist

line_data = LineData()
running = True
clock = pygame.time.Clock()

error_list = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if math.dist(robot.position, line_points[-1]) < 5:
        print("Reached the end of the line!")
        running = False
        continue

    left_sensor, right_sensor = robot.simulate_sensors(line_data)
    error = robot.calculate_error(left_sensor, right_sensor)
    error_list.append(error)
    robot.update_position(error)

    # Render the scene
    screen.fill(WHITE)
    pygame.draw.lines(screen, BLACK, False, line_points, line_width)
    pygame.draw.circle(screen, ROBOT_COLOR, (int(robot.position[0]), int(robot.position[1])), 5)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# Plot error after pygame simulation ends
plt.plot(error_list, label='Error')
plt.xlabel('Time Step')
plt.ylabel('Error')
plt.title('Error Over Time')
plt.legend()
plt.show()
