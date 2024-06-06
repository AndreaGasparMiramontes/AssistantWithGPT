from pynput.keyboard import Key, Controller

keyboard = Controller()

def get_weather():
    return("38")

def pause():
    global keyboard
    keyboard.press(Key.media_play_pause)
    return("True")