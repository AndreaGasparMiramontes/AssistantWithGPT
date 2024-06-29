from pynput.keyboard import Key, Controller

keyboard = Controller()

def get_weather():
    return("38")

def pause():
    global keyboard
    keyboard.press(Key.media_play_pause)
    return("True")

def next():
    global keyboard
    keyboard.press(Key.media_next)
    return("True")

def previous():
    global keyboard
    keyboard.press(Key.media_previous)
    return("True")

def volume_down():
    global keyboard
    for a in range (5):
        keyboard.press(Key.media_volume_down)
        time.sleep(1)
        keyboard.release(Key.media_volume_down) 
    return("True")

def volume_up():
    global keyboard
    for a in range (5):
        keyboard.press(Key.media_volume_up)
        time.sleep(1)
        keyboard.release(Key.media_volume_up) 
    return("True")