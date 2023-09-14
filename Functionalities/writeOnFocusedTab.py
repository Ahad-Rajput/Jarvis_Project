import pygetwindow as gw
import pyautogui
import time


# Getting Focused Window
def get_focused_window():
    try:
        return gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]
    except IndexError:
        return None


def writeOnTab(query):
    text_to_write = query.replace("write", "").strip()
    if text_to_write:
        print(f"Writing: {text_to_write}")
        focused_window = get_focused_window()
        if focused_window:
            focused_window.activate()
            time.sleep(1)  # Wait for the window to activate
            pyautogui.write(text_to_write)