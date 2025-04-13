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
global customers_served
customers_served = 0
customers_served_lock = threading.Lock()


#Teller class to handle everything on that end
class Teller(threading.Thread):
    def __init__(self, teller_id):
        super().__init__()
        self.id = teller_id
        self.available = True
        self.current_customer = None
        self.customer_assigned = threading.Event()
        self.transaction_complete = threading.Event()

    def run(self):
        global customers_served

        while customers_served < 50:
            print(f"Teller {self.id} []:  ready to serve.")
            if self.id == 2:
                bank_open.set()  # simulate that when the last teller is ready, bank opens
            print(f"Teller {self.id} []:  waiting for customer.")

            with queue_condition:
                while customer_queue.empty() and customers_served < 50:
                    #wait for customer
                    queue_condition.wait()
                if customers_served >= 50:
                    return

                self.current_customer = customer_queue.get()
                self.available = False
                # Assign yourself to the customer
                self.current_customer.assigned_teller = self
                self.current_customer.assigned_event.set()
                print(f"Teller {self.id} [Customer {self.current_customer.id}]: serving a customer ")
                print(f"Teller {self.id} [Customer {self.current_customer.id}]: asks for transaction ")
                print(f"Customer {self.current_customer.id} [Teller {self.id}]: asks for {self.current_customer.transaction_type} transaction")

            # Service the customer

            print(f"Teller {self.id} [Customer {self.current_customer.id}]: Hello!")
            time.sleep(random.uniform(0.50, 1.0))  # Transaction time
            print(f"Teller {self.id} [Customer {self.current_customer.id}]: Transaction complete")

            should_exit = False
            # Check completion AFTER transaction
            with customers_served_lock:
                customers_served += 1
                should_exit = (customers_served >= 50)
                if should_exit:
                    with queue_condition:
                        queue_condition.notify_all()

            self.available = True
            self.current_customer = None

            if should_exit:
                return





class Customer(threading.Thread):
    def __init__(self, customer_id):
        super().__init__()
        self.id = customer_id
        self.transaction_type = random.choice(["deposit", "withdraw"])
        self.assigned_teller = None
        self.assigned_event = threading.Event()

    def run(self):
        # Wait for bank to open
        bank_open.wait()

        # milliseconds to wait
        delay = random.randint(0, 100) / 1000
        print(f"Customer {self.id} []: wants to perform a {self.transaction_type} transaction")
        time.sleep(delay)
        # goes to the bank
        print(f"Customer {self.id} []: going to bank")

        # only two customers at allowed through the doors are once and once they enter they stand in line
        door_semaphore.acquire()
        print(f"Customer {self.id} []: entering bank")
        door_semaphore.release()

        # put yourself in a line and wait
        with queue_condition:
            customer_queue.put(self)
            print(f"Customer {self.id} []: getting in line")
            queue_condition.notify_all()

        # wait for a teller to be assigned
        self.assigned_event.wait()
        print(f"Customer {self.id} [Teller {self.assigned_teller.id}]: selects teller")
        print(f"Customer {self.id} [Teller {self.assigned_teller.id}]: introduces itself")





#Main class to create the threads
if __name__ == "__main__":

    #create 3 tellers
    global tellers
    tellers = [Teller(i) for i in range(3)]

   # Start tellers
    for teller in tellers:
        teller.start()

    #open the bank
    bank_open.wait()


   # Create and start customers
    global customers
    customers = [Customer(i) for i in range(50)]

    for customer in customers:
        customer.start()

    # Wait for all transactions to complete
    while True:
        with customers_served_lock:
            if customers_served >= 50:
                break
        time.sleep(0.1)

    # Wait for all customers to complete
    for customer in customers:
        customer.join()

   # wait for the tellers to finish after since they'll be working after
    for i, teller in enumerate(tellers):
        teller.join()
        print(f"Teller {i} []: leaving for the day")


    bank_open.clear()
   #basically program finished type beat
    print("The bank closes for the day.")





