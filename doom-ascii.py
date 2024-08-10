import curses
import math

# Maps
sm_game_map = [
    "########",
    "#......#",
    "#......#",
    "#......#",
    "###..###",
    "#......#",
    "#......#",
    "########"
]
md_game_map = [
    "########################",
    "#..........#...........#",
    "#..........#...........#",
    "#..#####...###..######..",
    "#..........#...........#",
    "#..........#...........#",
    "###..####..###..######..",
    "#..........#...........#",
    "#..........#...........#",
    "###..##########..#####..",
    "#..........#...........#",
    "#..........#...........#",
    "#..#####...###..######..",
    "#..........#...........#",
    "#..........#...........#",
    "########################"
]
lg_game_map = [
    "########################################",
    "#...........#............#.............#",
    "#...........#............#.............#",
    "#..######...#####..#######..######..####",
    "#...........#............#.............#",
    "#...........#............#.............#",
    "###..#####..#####..#######..######..####",
    "#...........#............#.............#",
    "#...........#............#.............#",
    "###..#############..######..######..####",
    "#...........#............#.............#",
    "#...........#............#.............#",
    "#..######...#####..#######..######..####",
    "#...........#............#.............#",
    "#...........#............#.............#",
    "########################################"
]
game_map = [
    "################################################################",
    "#..................#............................#..............#",
    "#..####..########..#..#######..########..#######..######..######",
    "#..#..#..#.......#.....#.....#.#........#.#.....#.#....#..#.....",
    "#..#..#..#.......#######.#####.#######..#.#.#####.#.####..####..",
    "#..#..#..#.............#.#.....#........#.#.....#.#....#..#.....",
    "#..#..#..#..##########.#.#.....##########.#######.#.####..######",
    "#..#..#.................#........................#.............#",
    "####..####################..########################..######..##",
    "#..............#.............#..............#.........#......#..",
    "#..#########..#..###########.#..#########..#..######..#######..#",
    "#.............#..............#............#.........#..........#",
    "########################..####..####################..####..####",
    "#...............#................#..................#...........",
    "#..###########..#..#############.#.###############..###########.",
    "#..............#.#..............#.................#............#",
    "#..##########..#.#..##########..#.###############..##########..#",
    "#.............#.#.............#.#.................#...........#",
    "####################..###########################..#########..##",
    "#................#....................#.........................#",
    "#.#############..#..###############..#.###############..#########",
    "#.#...........#..#.#...............#.#...............#.........#",
    "#.#..#######..#..#.#.###########..#.#..##########..##..######..#",
    "#.#..#.....#..#..#.#...........#..#.#..#.........#..#...........#",
    "#.###..###..##..#.#.#########..#.###..#..#########.#########..##",
    "#.........#.#....#.............#.#......#.................#.....#",
    "################################################################"
]

# Constants for player
player_x = 1.5
player_y = 1.5
player_angle = 0.0
fov = math.pi / 4  
max_depth = 16  

# Player stats
player_health = 100
current_level = 1

# Shading characters
shading_characters = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

# Shading function
def calculate_shade(distance_to_wall, max_depth):
    # Calculate index based on distance to wall, adjusted for non-linear attenuation
    index = int((distance_to_wall / max_depth) * (len(shading_characters) - 1))
    index = max(0, min(index, len(shading_characters) - 1))
    return shading_characters[index]

# Minimap function
def draw_minimap(buffer, player_x, player_y, offset_x, offset_y, map_scale=2):
    # Calculate the minimap dimensions
    map_height = len(game_map) // map_scale
    map_width = len(game_map[0]) // map_scale
    
    for row in range(0, len(game_map), map_scale):
        for col in range(0, len(game_map[0]), map_scale):
            char = game_map[row][col]
            if int(player_y) == row and int(player_x) == col:
                char = '0'  # Use a distinct player icon
            elif char == '#':
                char = '$'  # Use a distinct wall character

            buffer_row = offset_y + row // map_scale
            buffer_col = offset_x + col // map_scale

            # Ensure we don't draw outside the buffer limits
            if 0 <= buffer_row < map_height and 0 <= buffer_col < map_width:
                buffer[buffer_row][buffer_col] = char


# Function to initialize the curses window
def draw_game(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.timeout(100)  # Refresh rate in milliseconds

    # Minimap toggle flag
    show_minimap = False

    global player_x, player_y, player_angle

    while True:
        # Clear the screen
        stdscr.clear()

        # Get screen dimensions
        screen_height, screen_width = stdscr.getmaxyx()

        # Create a screen buffer
        screen_buffer = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]

        
        # If toggled on, draw map
        if show_minimap:
            draw_minimap(screen_buffer, player_x, player_y, offset_x=0, offset_y=0, map_scale=2)
            

        # Render the 3D view
        for ray in range(screen_width):
            # Calculate ray angle
            ray_angle = (player_angle - fov / 2.0) + (ray / screen_width) * fov

            # Calculate distance to wall
            distance_to_wall = 0
            hit_wall = False

            eye_x = math.sin(ray_angle)
            eye_y = math.cos(ray_angle)

            while not hit_wall and distance_to_wall < max_depth:
                distance_to_wall += 0.1
                test_x = int(player_x + eye_x * distance_to_wall)
                test_y = int(player_y + eye_y * distance_to_wall)

                # Test if ray is out of bounds
                if test_x < 0 or test_x >= len(game_map[0]) or test_y < 0 or test_y >= len(game_map):
                    hit_wall = True
                    distance_to_wall = max_depth
                else:
                    # Check if ray has hit the wall
                    if game_map[test_y][test_x] == '#':
                        hit_wall = True

            # Calculate distance-based shading
            shade = calculate_shade(distance_to_wall, max_depth)

            # Calculate ceiling and floor
            ceiling = int(screen_height / 2.0 - screen_height / distance_to_wall)
            floor = screen_height - ceiling

            # Draw the column in the screen buffer
            for y in range(screen_height):
                if y < ceiling:
                    if y < len(game_map) and ray < len(game_map[0]):
                        continue  # Skip over where the map is displayed
                    screen_buffer[y][ray] = ' '
                elif ceiling <= y <= floor:
                    screen_buffer[y][ray] = shade
                else:
                    screen_buffer[y][ray] = '.'

        # Draw the HUD at the top of the screen
        hud_text = f"Health: {player_health}  Level: {current_level}"
        stdscr.addstr(0, screen_width - len(hud_text) - 2, hud_text)

        # Convert the screen buffer to strings and print
        for line in screen_buffer:
            try:
                stdscr.addstr(''.join(line))
            except curses.error:
                pass

        # Get user input
        key = stdscr.getch()

        # Handle player movement and controls
        if key == ord('w'):
            player_x += math.sin(player_angle) * 0.1
            player_y += math.cos(player_angle) * 0.1
            # Collision detection
            if game_map[int(player_y)][int(player_x)] == '#':
                player_x -= math.sin(player_angle) * 0.1
                player_y -= math.cos(player_angle) * 0.1
        if key == ord('s'):
            player_x -= math.sin(player_angle) * 0.1
            player_y -= math.cos(player_angle) * 0.1
            # Collision detection
            if game_map[int(player_y)][int(player_x)] == '#':
                player_x += math.sin(player_angle) * 0.1
                player_y += math.cos(player_angle) * 0.1
        if key == ord('a'):
            player_angle -= 0.1
        if key == ord('d'):
            player_angle += 0.1

        # Toggle minimap visibility with 'm'
        if key == ord('m'):
            show_minimap = not show_minimap

        # Quit the game if 'q' is pressed
        if key == ord('q'):
            break

# Define the home screen function
def show_menu(stdscr):
    current_row = 0
    menu = ['Start Game', 'Instructions', 'Exit']

    ascii_art = [
        r"__/\\\\\\\\\\\\____________________________________________________",
        r" _\/\\\////////\\\__________________________________________________",
        r"  _\/\\\______\//\\\_________________________________________________",
        r"   _\/\\\_______\/\\\_____/\\\\\________/\\\\\_______/\\\\\__/\\\\\___",
        r"    _\/\\\_______\/\\\___/\\\///\\\____/\\\///\\\___/\\\///\\\\\///\\\_",
        r"     _\/\\\_______\/\\\__/\\\__\//\\\__/\\\__\//\\\_\/\\\_\//\\\__\/\\\_",
        r"      _\/\\\_______/\\\__\//\\\__/\\\__\//\\\__/\\\__\/\\\__\/\\\__\/\\\_",
        r"       _\/\\\\\\\\\\\\/____\///\\\\\/____\///\\\\\/___\/\\\__\/\\\__\/\\\_",
        r"        _\////////////________\/////________\/////_____\///___\///___\///__",
        r" _____________________________________________________________",
        r"  _____________________________________________________________",
        r"   ______________________/\\\___________________________________",
        r"    _____________________\///___/\\/\\\\\\_______________________",
        r"     ______________________/\\\_\/\\\////\\\______________________",
        r"      _____________________\/\\\_\/\\\__\//\\\_____________________",
        r"       _____________________\/\\\_\/\\\___\/\\\_____________________",
        r"        _____________________\/\\\_\/\\\___\/\\\_____________________",
        r"         _____________________\///__\///____\///______________________",
        r"",
        r"_____/\\\\\\\\\________/\\\\\\\\\\\__________/\\\\\\\\\__/\\\\\\\\\\\__/\\\\\\\\\\_",
        r" ___/\\\\\\\\\\\\\____/\\\/////////\\\_____/\\\////////__\/////\\\///__\/////\\\///__",
        r"  __/\\\/////////\\\__\//\\\______\///____/\\\/_______________\/\\\_________\/\\\_____",
        r"   _\/\\\_______\/\\\___\////\\\__________/\\\_________________\/\\\_________\/\\\_____",
        r"    _\/\\\\\\\\\\\\\\\______\////\\\______\/\\\_________________\/\\\_________\/\\\_____",
        r"     _\/\\\/////////\\\_________\////\\\___\//\\\________________\/\\\_________\/\\\_____",
        r"      _\/\\\_______\/\\\__/\\\______\//\\\___\///\\\______________\/\\\_________\/\\\_____",
        r"       _\/\\\_______\/\\\_\///\\\\\\\\\\\/______\////\\\\\\\\\__/\\\\\\\\\\\__/\\\\\\\\\\_",
        r"        _\///________\///____\///////////___________\/////////__\///////////__\//////////__",
    ]

    while True:
        stdscr.clear()

        # Print menu and instructions
        stdscr.addstr(0, 0, "Home Screen", curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(1, 0, "Use arrow keys to navigate and Enter to select", curses.A_DIM)

        # Print the menu options
        for idx, row in enumerate(menu):
            x = 0
            y = 3 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        # Print ascii title
        for i, line in enumerate(ascii_art):
            stdscr.addstr(len(menu) + 5 + i, 0, line)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                # Start game
                return  draw_game(stdscr)
            elif current_row == 1:
                # Show instructions
                show_instructions(stdscr)
            elif current_row == 2:
                # Exit
                break

        stdscr.refresh()

def show_instructions(stdscr):
    stdscr.clear()
    instructions = [
        "Instructions:",
        "Move with W, A, S, D.",
        "Navigate the maze and avoid obstacles.",
        "Press Q to quit the game.",
        "",
        "Press any key to return to the menu."
    ]
    for idx, line in enumerate(instructions):
        stdscr.addstr(idx + 1, 0, line)
    stdscr.getch()  # Wait for any key press

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    show_menu(stdscr)

curses.wrapper(main)
