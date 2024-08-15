import curses

# Define the home screen function
def show_menu(stdscr, draw_game):
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

        # Get screen dimensions
        height, width = stdscr.getmaxyx()

        # Calculate start positions
        ascii_y_start = max((height - len(ascii_art)) // 4, 0)
        menu_y_start = ascii_y_start + len(ascii_art) + 3

        # Adjust if ASCII art is too tall for the screen
        visible_art = ascii_art[:max(height - menu_y_start, 0)]
        if not visible_art:
            visible_art = ascii_art[:]

        # Center the ASCII art
        for i, line in enumerate(visible_art):
            try:
                stdscr.addstr(ascii_y_start + i, (width - len(line)) // 2, line)
            except curses.error:
                pass

        # Draw a border around the menu
        border_padding = 2
        border_width = max(len(row) for row in menu) + border_padding * 2
        border_x_start = (width - border_width) // 2

        for i in range(len(menu) + 4):
            if i == 0 or i == len(menu) + 3:
                try:
                    stdscr.addstr(menu_y_start + i, border_x_start, '+' + '-' * (border_width - 2) + '+')
                except curses.error:
                    pass
            else:
                try:
                    stdscr.addstr(menu_y_start + i, border_x_start, '|')
                    stdscr.addstr(menu_y_start + i, border_x_start + border_width - 1, '|')
                except curses.error:
                    pass

        # Print the menu options centered within the border
        for idx, row in enumerate(menu):
            x = border_x_start + border_padding
            y = menu_y_start + 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                try:
                    stdscr.addstr(y, x, row.center(border_width - border_padding * 2))
                except curses.error:
                    pass
                stdscr.attroff(curses.color_pair(1))
            else:
                try:
                    stdscr.addstr(y, x, row.center(border_width - border_padding * 2))
                except curses.error:
                    pass

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                # Start game
                return draw_game(stdscr)
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
        try:
            stdscr.addstr(idx + 1, 0, line)
        except curses.error as e:
            pass
    stdscr.getch()  # Wait for any key press

