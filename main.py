"""
To simulate two systems, we us theading and queues.
We use two threads to represent each system and four queues to represent each line of communication.
"""
import threading
import queue

def aggregator(arinc_to_agg, arinc_to_cal, afdx_to_agg, afdx_to_cal):
    # arinc_to_agg.get()
    # arinc_to_cal.put(message)
    # afdx_to_agg.get()
    # afdx_to_cal.put(message)
    pass
    
def calculator(arinc_to_agg, arinc_to_cal, afdx_to_agg, afdx_to_cal):
    # arinc_to_agg.put(message)
    # arinc_to_cal.get()
    # afdx_to_agg.put(message)
    # afdx_to_cal.get()
    pass

# Create two queues for each direction of communication, one for each protocol
arinc_to_agg = queue.Queue()
arinc_to_cal = queue.Queue()
afdx_to_agg = queue.Queue()
afdx_to_cal = queue.Queue()


aggregator = threading.Thread(target=aggregator, args=(arinc_to_agg, afdx_to_cal, afdx_to_agg, arinc_to_cal))
calculator = threading.Thread(target=calculator, args=(afdx_to_agg, arinc_to_cal, arinc_to_agg, afdx_to_cal))

# Start the threads
aggregator.start()
calculator.start()

# Wait for the threads to finish
aggregator.join()
calculator.join()
