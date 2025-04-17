import curses

menu = ['Iniciar', 'Configurações', 'Sair']

def main(stdscr):
    curses.curs_set(0)
    current_row = 0

    def print_menu():
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for i, item in enumerate(menu):
            x = w//2 - len(item)//2
            y = h//2 - len(menu)//2 + i
            if i == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, item)
        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    print_menu()

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, ord('\n')]:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Você selecionou: {menu[current_row]}")
            stdscr.refresh()
            stdscr.getch()
            if menu[current_row] == 'Sair':
                break
        print_menu()

if __name__ == '__main__':
    curses.wrapper(main)
