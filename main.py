"""
To simulate two systems, we us theading and queues.
We use two threads to represent each system and four queues to represent each line of communication.
"""
import threading
import queue
import calculator
from Interfaces import Interfaces
import time

def aggregator_thread(arinc_to_agg, arinc_to_cal, afdx_to_agg, afdx_to_cal, user_to_agg):
    while True:
        if not user_to_agg.empty():
            user_input = user_to_agg.get()
            altitude_desiree = user_input[0] if user_input != '' else None
            taux_monte = user_input[1] if user_input != '' else None
            angle_attaque = user_input[2] if user_input != '' else None 
        if not arinc_to_agg.empty():
            
            close= gui._window()
            if close == False:
                exit(0)
        
    
    
def calculator_thread(arinc_to_agg, arinc_to_cal, afdx_to_agg, afdx_to_cal):
    last_frame = time.monotonic()

    while True:
        if not (arinc_to_agg.empty() and afdx_to_agg.empty()):
            arinc_from_cal = arinc_to_agg.get()
            afdx_from_cal = afdx_to_agg.get()
            
            #TODO: Check if messages are the same (Redondance)
            # If same chose value of arinc4
            # If not discard
        
        # Appel de la fonction qui reçois les inputs de l'utilisateur 
        calculator.lire_input(var)

        # Fonction du temps
        now = time.monotonic() 
        dt = now - last_frame
        last_frame = now

        # Appel de la fonction qui déterminera le prochain état
        #prochain_etat(var, dt)
        print(prochain_etat(var, dt))

        # Rafraichissement
        time.sleep(0.005)
        # print(var) # Juste pour les tests
        afdx_to_cal.put(message)
        arinc_to_cal.put(message)
    # arinc_to_agg.put(message)
    # arinc_to_cal.get()
    # afdx_to_agg.put(message)
    # afdx_to_cal.get()
    pass

def input_t(gui, user_to_agg):
    while True:
        close, values = gui.input_window()
        if close == False:
            exit(0)
        else:
            user_to_agg(values)


if __name__ == "__main__":
    gui = Interfaces()

    # Create two queues for each direction of communication, one for each protocol
    arinc_to_agg = queue.Queue()
    arinc_to_cal = queue.Queue()
    afdx_to_agg = queue.Queue()
    afdx_to_cal = queue.Queue()
    user_to_agg = queue.Queue()

    aggregator_thread = threading.Thread(target=aggregator_thread, args=(arinc_to_agg, afdx_to_cal, afdx_to_agg, arinc_to_cal))
    calculator_thread = threading.Thread(target=calculator_thread, args=(afdx_to_agg, arinc_to_cal, arinc_to_agg, afdx_to_cal))
    input_t = threading.Thread(target=input_t, args=(gui,))

    # Start the threads
    aggregator_thread.start()
    calculator_thread.start()
    input_t.start()

    # Wait for the threads to finish
    aggregator_thread.join()
    calculator_thread.join()
    input_t.join()
