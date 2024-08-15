import curses
import math
import random

from maps import sm_game_map, md_game_map, lg_game_map, xl_game_map
from menu import show_menu

# Constants for player
player_x = 1.5
player_y = 1.5
player_angle = 0.0
fov = math.pi / 4
max_depth = 16
move_speed = 0.1
turn_speed = 0.1

game_map = xl_game_map

# Player stats
player_health = 100
current_level = 1


# Enemy definitions
enemies = [
    {'x': 3.5, 'y': 3.5, 'symbol': 'X', 'health': 50},
    {'x': 10.5, 'y': 8.5, 'symbol': '@', 'health': 50},
]

# Shading characters
shading_characters = ['.', ':', '-']

# Initialize colors
def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)    # Walls
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)  # Gun
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Vertical edges
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Floors/Ceilings
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Enemies

# Calculate shading
def calculate_shade(distance_to_wall):
    max_shade_index = len(shading_characters) - 1
    index = int((distance_to_wall / max_depth) * max_shade_index)
    index = max(0, min(index, max_shade_index))
    return shading_characters[index]


# Check if a vertical edge should be drawn
def should_draw_vertical_edge(x, y):
    if x > 0 and game_map[y][x - 1] == ' ':
        return True  # Edge on the left
    if x < len(game_map[0]) - 1 and game_map[y][x + 1] == ' ':
        return True  # Edge on the rightmm
    return False

# Basic enemy AI movement
def move_enemies():
    for enemy in enemies:
        move_dir = random.choice(['up', 'down', 'left', 'right'])
        if move_dir == 'up' and game_map[int(enemy['y'] - move_speed)][int(enemy['x'])] != '#':
            enemy['y'] -= move_speed
        elif move_dir == 'down' and game_map[int(enemy['y'] + move_speed)][int(enemy['x'])] != '#':
            enemy['y'] += move_speed
        elif move_dir == 'left' and game_map[int(enemy['y'])][int(enemy['x'] - move_speed)] != '#':
            enemy['x'] -= move_speed
        elif move_dir == 'right' and game_map[int(enemy['y'])][int(enemy['x'] + move_speed)] != '#':
            enemy['x'] += move_speed

# Draw game loop
def draw_game(stdscr):

    init_colors()

    global player_x, player_y, player_angle
    show_minimap = False  # Control minimap visibility

    while True:
        stdscr.clear()

        # Get screen dimensions
        screen_height, screen_width = stdscr.getmaxyx()


        # Render the 3D view
        for ray in range(screen_width):
            ray_angle = (player_angle - fov / 2.0) + (ray / screen_width) * fov
            distance_to_wall = 0
            hit_wall = False
            hit_enemy = None
            vertical_edge = False

            eye_x = math.sin(ray_angle)
            eye_y = math.cos(ray_angle)

            while not hit_wall and distance_to_wall < max_depth:
                distance_to_wall += 0.1
                test_x = int(player_x + eye_x * distance_to_wall)
                test_y = int(player_y + eye_y * distance_to_wall)

                if test_x < 0 or test_x >= len(game_map[0]) or test_y < 0 or test_y >= len(game_map):
                    hit_wall = True
                    distance_to_wall = max_depth
                elif game_map[test_y][test_x] == '#':
                    hit_wall = True
                    vertical_edge = should_draw_vertical_edge(test_x, test_y)
                else:
                    for enemy in enemies:
                        if int(enemy['x']) == test_x and int(enemy['y']) == test_y:
                            hit_enemy = enemy
                            hit_wall = True

            if distance_to_wall <= max_depth / 4.0:
                color_pair = curses.color_pair(1)
            elif distance_to_wall <= max_depth / 2.0:
                color_pair = curses.color_pair(1)
            else:
                color_pair = curses.color_pair(1)

            ceiling = int(screen_height / 2.0 - screen_height / distance_to_wall)
            floor = screen_height - ceiling
            shade = calculate_shade(distance_to_wall)

            for y in range(screen_height):
                if y < ceiling:
                    try:
                        stdscr.addch(y, ray, ' ', curses.color_pair(4))
                    except curses.error as e:
                        pass
                elif ceiling <= y <= floor:
                    if hit_enemy:
                        try:
                            stdscr.addch(y, ray, hit_enemy['symbol'], curses.color_pair(5))
                        except curses.error as e:
                            pass
                    elif vertical_edge:
                        try:
                            stdscr.addch(y, ray, '|', curses.color_pair(3))
                        except curses.error as e:
                            pass
                    else:
                        try:
                            stdscr.addch(y, ray, shade, color_pair)
                        except curses.error as e:
                            pass
                else:
                    try:
                        stdscr.addch(y, ray, '.', curses.color_pair(4))
                    except curses.error as e:
                        pass

        for enemy in enemies:
            if show_minimap:
                try:
                    stdscr.addch(int(enemy['y']), int(enemy['x']), enemy['symbol'], curses.color_pair(5))
                except curses.error as e:
                    pass
                


        hud_text = f"Health: {player_health}  Level: {current_level}"
        stdscr.addstr(0, screen_width - len(hud_text) - 2, hud_text)

        gun_representation = [
            "*%@@",  
            "@*%@@%",  
            "@@#@%@@#",  
            "@@#@%@@@",  
            "@@@@#%%%@@#",  
            "*%%@@@+@#@@@@#",  
            "@%@@@##@%@@@@%",  
            "@%@@@@#*#%@@%%#",  
            "@@%%@@@#+#%%%%%@",  
            "@%@@@@%#+*#%%%%@",  
            "%@%@@@%#-#%%%@@@",  
            "@@@@@@@%+#%@@@%@",  
        ]
        
        hand_representation = [
            "=-+#@@%@@@%%**%@@@%@",  
            "------#@@@%%%#++%%@@@@",  
            "------==+@@@@%#==%@@@@@@",  
            "==--:--===#@@@@%+:%%@@@@@",  
            "*=--=-==*%@@@%# #%@@@@@",  
            "=--:--==+**#@@@@% +%%@@@@",  
            ":+-----==***#%@@@@- #@@@@@@",  
            "#==--==++*##%%@@@@= *%@@@@@",  
            "#+=--==*##%%%%%%@@# -@%%%@@",  
        ]
        
        for i, line in enumerate(gun_representation):
            stdscr.addstr(screen_height - len(gun_representation) - len(hand_representation) + i, screen_width // 2 - len(line) // 2, line, curses.color_pair(1))

        for i, line in enumerate(hand_representation):
            stdscr.addstr(screen_height - len(hand_representation) + i, screen_width // 2 - len(line) // 2, line, curses.color_pair(2))

        stdscr.refresh()

        move_enemies()

        key = stdscr.getch()

        if key == ord('w'):
            new_x = player_x + math.sin(player_angle) * move_speed
            new_y = player_y + math.cos(player_angle) * move_speed
            if game_map[int(new_y)][int(new_x)] != '#':
                player_x = new_x
                player_y = new_y
        if key == ord('s'):
            new_x = player_x - math.sin(player_angle) * move_speed
            new_y = player_y - math.cos(player_angle) * move_speed
            if game_map[int(new_y)][int(new_x)] != '#':
                player_x = new_x
                player_y = new_y
        if key == ord('a'):
            player_angle -= turn_speed
        if key == ord('d'):
            player_angle += turn_speed

        if key == ord('m'):
            show_minimap = not show_minimap

        if key == ord('q'):
            break

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    init_colors()  # Initialize colors
    show_menu(stdscr, draw_game)  # Call the show_menu function

curses.wrapper(main)
