import curses

text = """Hello world!
This is a tiny text editor.
Edit me!"""

cursor = 0


def draw(screen):
    screen.clear()

    display = text[:cursor] + "|" + text[cursor:]

    for row, line in enumerate(display.split("\n")):
        screen.addstr(row, 0, line)

    screen.addstr(
        len(display.split("\n")) + 1,
        0,
        "← → Move   Type Insert   Backspace Delete   Enter New Line   Esc Quit"
    )

    screen.refresh()


def main(screen):
    global text, cursor

    while True:
        draw(screen)

        key = screen.getch()

        if key == 27:
            break

        elif key == curses.KEY_LEFT:
            if cursor > 0:
                cursor -= 1

        elif key == curses.KEY_RIGHT:
            if cursor < len(text):
                cursor += 1

        elif key in (8, 127, curses.KEY_BACKSPACE):
            if cursor > 0:
                text = text[:cursor-1] + text[cursor:]
                cursor -= 1

        elif key == 10:
            text = text[:cursor] + "\n" + text[cursor:]
            cursor += 1

        elif 32 <= key <= 126:
            text = text[:cursor] + chr(key) + text[cursor:]
            cursor += 1

        elif key == curses.KEY_UP:
            split_text = text.split("\n")

            idx1 = 0
            idx2 = 0
            cur_line = 0

            for i in range(len(split_text)):
                idx1 = idx2
                idx2 += len(split_text[i]) + 1
                if cursor <= idx2:
                    cur_line = i
                    break

            if cur_line > 0:
                prev_line_start = idx1 - len(split_text[cur_line - 1]) - 1
                cursor = prev_line_start + min(cursor - idx1, len(split_text[cur_line - 1]))

        elif key == curses.KEY_DOWN:
            split_text = text.split("\n")

            idx1 = 0
            idx2 = 0
            cur_line = 0

            for i in range(len(split_text)):
                idx1 = idx2
                idx2 += len(split_text[i]) + 1
                if cursor <= idx2:
                    cur_line = i
                    break

            if cur_line < len(split_text) - 1:
                next_line_start = idx2
                cursor = next_line_start + min(cursor - idx1, len(split_text[cur_line + 1]))


curses.wrapper(main)