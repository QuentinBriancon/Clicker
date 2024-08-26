from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
from time import sleep


position_cible = (2384, 327)
state = False

def get_position_cible():
    mouse = Controller()
    print ("Current position: " + str(mouse.position))
    global position_cible
    position_cible = mouse.position

def effectuer_clic():
    global state
    while state == True:
        mouse = Controller()
        mouse.position = position_cible
        mouse.click(Button.left, 5)
        sleep (0.01)

def on_press(key):
    global state
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        if key == keyboard.Key.f2:
            if state == True:
                state = False
                return
            else:
                state = True
                thread = threading.Thread(target=effectuer_clic)
                thread.start()
                
        elif key == keyboard.Key.f3:
            get_position_cible()

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()

