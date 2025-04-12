import threading
import time
import random
from queue import Queue

# set up all the variables
door_semaphore = threading.Semaphore(2)
manager_semaphore = threading.Semaphore(1)
safe_semaphore = threading.Semaphore(2)
customer_queue = Queue()
queue_condition = threading.Condition()
bank_open = threading.Event()
customers_served = 0
customers_served_lock = threading.Lock()


# classes for the tellers
class Teller(threading.Thread):
    def __init__(self, id):
        #not shared resources
        threading.Thread.__init__(self)
        self.id = id
        self.available = threading.Event()
        self.available.set()  # initially available
        self.current_customer = None
        self.customer_assigned = threading.Event()
        self.transaction_complete = threading.Event()
        self.manager_sem = manager_semaphore
        self.safe_sem = safe_semaphore
        self.transaction_type = None

    def run(self):
        print(f"Teller {self.id} []: ready to serve")
        print(f"Teller {self.id} []: waiting for a customer")
        while True:
            #acquire the lock for queue_condition to make sure you're the only one accessing it
            with queue_condition:
                while customer_queue.empty():
                    if customers_served >= 50:
                        return
                    # release the lock and wait
                    queue_condition.wait()
                #once a customer is ready, take the customer
                self.customer_assigned.wait()
                # Get transaction type from customer
                print(f"Teller {self.id} [{self.current_customer.id}]: serving a customer")
                print(f"Teller {self.id} [{self.current_customer.id}]: asks for transaction")
                self.transaction_type = self.current_customer.transaction_type
                print(f"Teller {self.id} [{self.current_customer.id}]: handling {self.transaction_type} transaction")

    def assign_customer(self, customer):
        self.current_customer = customer
        self.customer_assigned.set()  # assigns customer to teller thread
        self.available.clear()  # marks teller as not available


# this is the class for customer threads
class Customer(threading.Thread):
    def __init__(self, teller_id, manager_semaphore, safe_semaphore):
        threading.Thread.__init__(self)
        self.id = id
        self.transaction_type = random.choice(["deposit", "withdraw"])
        self.teller_ready = threading.Event()  # is teller ready for transaction
        self.transaction_received = threading.Event()  # did teller receive transaction
        self.transaction_done = threading.Event()  # is transaction done
    def run(self):
        global customers_served

        # Wait for bank to open
        bank_open.wait()

        #milliseconds to wait
        delay = random.randint(0, 100) / 1000

        # goes to the bank
        print(f"Customer {self.id} []: going to bank")
        time.sleep(delay)

        # only two customers at allowed through the doors are once and once they enter they stand in line
        door_semaphore.acquire()
        print(f"Customer {self.id} []: entering bank")
        door_semaphore.release()
        print(f"Customer {self.id} []: getting in line")
        # find available teller
        teller = None
        while not teller:
            for t in tellers:
                #if the tellers are available then take the first one
                if t.available.is_set() and t.available.wait(timeout=0):
                    print(f"Customer {self.id} []: selecting a teller")
                    teller = t
                    print(f"Customer {self.id} [Teller {teller.id}]: selects teller")
                    break
            else:
                # wait in the teller queue
                with queue_condition:
                    customer_queue.put(self)
                    queue_condition.wait()
                    #wait till assigned a teller
                    if self.assigned_teller:
                        teller = self.assigned_teller
                        print(f"Customer {self.id} [Teller {teller.id}]: selects teller")
                        break

            # assigns itself to the teller
            teller.assign_customer(self)
            print(f"Customer {self.id} [Teller {teller.id}]: introduces itself")

            self.teller_ready.wait()
            self.transaction_done.wait()





        # this increments the number of saved customers at the end
        global customers_served_lock
        with customers_served_lock:
            customers_served += 1


# Create tellers
tellers = [Teller(i, manager_semaphore, safe_semaphore) for i in range(3)]

if __name__ == "__main__":
    # Start tellers
    for teller in tellers:
        teller.start()

    # Wait for bank to open (all tellers ready)
    bank_open.wait()

    # Create and start customers
    customers = [Customer(i) for i in range(50)]
    for customer in customers:
        customer.start()

    # Wait for all customers to complete
    for customer in customers:
        customer.join()
    # Tell tellers to finish
    for teller in tellers:
        teller.customer_assigned.set()  # Wake them up to check exit condition
        teller.join()
    # wait for the tellers to finish after since they'll be working after
    for i, teller in enumerate(tellers):
        print(f"Teller {i} []: leaving for the day")
        teller.join()

    #basically program finished type beat
    print("The bank closes for the day.")

