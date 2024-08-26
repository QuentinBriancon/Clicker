from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
from time import sleep



positions_cibles = []  # Liste des positions cibles
current_target_index = 0  # Index de la position cible actuelle
state = False
clic_interval = 0.01  # Intervalle entre les clics en secondes
max_positions = 4  # Nombre maximum de positions cibles
clic_thread = None  # Thread pour les clics




def get_position_cible():
    global positions_cibles
    mouse = Controller()
    print("Current position: " + str(mouse.position))
    if len(positions_cibles) < max_positions:
        positions_cibles.append(mouse.position)
        print(f"Position cible ajoutée: {mouse.position}")
    else:
        print("Maximum de positions cibles atteint.")

def set_clic_interval(value):
    global clic_interval
    try:
        clic_interval = float(value)
        print(f"Intervalle entre les clics défini à: {clic_interval} secondes")
    except ValueError:
        print("Valeur d'intervalle invalide.")
        
def reset_positions():
    global positions_cibles
    positions_cibles = []  # Réinitialise à aucune position
    print("Positions cibles réinitialisées.")
        
def effectuer_clic():
    global state, current_target_index, positions_cibles
    mouse = Controller()
    while state:
        if positions_cibles:
            position_cible = positions_cibles[current_target_index]
            mouse.position = position_cible
        else:
            position_cible = mouse.position  # Utilise la position actuelle si aucune position cible
        mouse.click(Button.left, 5)
        sleep(clic_interval)
        # Passer à la position cible suivante
        if positions_cibles:
            current_target_index = (current_target_index + 1) % len(positions_cibles)

def on_press(key):
    global state, current_target_index, clic_thread
    try:
        print('Alphanumeric key {0} pressed'.format(key.char))  
    except AttributeError:
        print('Special key {0} pressed'.format(key))
        if key == keyboard.Key.f2:
            if state:
                state = False
                if clic_thread:
                    clic_thread.join() # Attend la fin du thread avant de continuer
                    clic_thread = None
                current_target_index = 0  # Réinitialise l'index des positions cibles
                print("Arrêt des clics.")
            else:
                state = True
                print("Démarrage des clics.")
                clic_thread = threading.Thread(target=effectuer_clic)
                clic_thread.start()
 

                
        elif key == keyboard.Key.f3:
            get_position_cible()
        
        elif key == keyboard.Key.f4:
            reset_positions()
            
        elif key == keyboard.Key.f5:
            # Demander à l'utilisateur de saisir un nouvel intervalle de clic
            user_input = input("Entrez le nouvel intervalle de r clic en secondes: ")
            set_clic_interval(user_input)
            
        elif key == keyboard.Key.f12:           
            print("F2: Démarrer/Arrêter les clics")
            print("F3: Ajouter une position cible")
            print("F4: Réinitialiser les positions cibles")
            print("F5: Définir l'intervalle entre les clics")
            print("F12: Afficher l'aide")
            print("ESC: Quitter")
        
            



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

