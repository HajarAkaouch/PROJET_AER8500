"""
To simulate two systems, we us theading and queues.
We use two threads to represent each system and four queues to represent each line of communication.
"""
import threading
import queue
import Calculator
import Interface

Calculator.boucle_principale()

def aggregator_thread(arinc_to_agg, arinc_to_cal, afdx_to_agg, afdx_to_cal):
    arinc_to_agg.get()
    arinc_to_cal.put(message)
    afdx_to_agg.get()
    afdx_to_cal.put(message)
    pass
    
def calculator_thread(arinc_to_agg, arinc_to_cal, afdx_to_agg, afdx_to_cal):
    arinc_to_agg.put(message)
    arinc_to_cal.get()
    afdx_to_agg.put(message)
    afdx_to_cal.get()
    pass

def user_terminal_thread():
    pass

# Create two queues for each direction of communication, one for each protocol
arinc_to_agg = queue.Queue()
arinc_to_cal = queue.Queue()
afdx_to_agg = queue.Queue()
afdx_to_cal = queue.Queue()


aggregator_thread = threading.Thread(target=aggregator_thread, args=(arinc_to_agg, afdx_to_cal, afdx_to_agg, arinc_to_cal))
calculator_thread = threading.Thread(target=calculator_thread, args=(afdx_to_agg, arinc_to_cal, arinc_to_agg, afdx_to_cal))
user_terminal_thread = threading.Thread(target=user_terminal_thread, args=())

# Start the threads
aggregator_thread.start()
calculator_thread.start()

# Wait for the threads to finish
aggregator_thread.join()
calculator_thread.join()
