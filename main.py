"""
To simulate two systems, we us theading and queues.
We use two threads to represent each system and four queues to represent each line of communication.
"""
import threading
import queue
import calculator
import Interfaces

def aggregator_thread(arinc_to_agg, arinc_to_cal, afdx_to_agg, afdx_to_cal):
    while True:
        if not (arinc_to_agg.empty() and afdx_to_agg.empty()):
            arinc_from_cal = arinc_to_agg.get()
            afdx_from_cal = afdx_to_agg.get()
            #TODO: Check if messages are the same (Redondance)
            # If same chose value of arinc
            # If not discard
        
            

        afdx_to_cal.put(message)
        arinc_to_cal.put(message)
    
    
def calculator_thread(arinc_to_agg, arinc_to_cal, afdx_to_agg, afdx_to_cal):
    calculator.boucle_principale()
    arinc_to_agg.put(message)
    arinc_to_cal.get()
    afdx_to_agg.put(message)
    afdx_to_cal.get()
    pass

def input(gui):
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
    input = threading.Thread(target=input, args=(gui))

    # Start the threads
    aggregator_thread.start()
    calculator_thread.start()

    # Wait for the threads to finish
    aggregator_thread.join()
    calculator_thread.join()
