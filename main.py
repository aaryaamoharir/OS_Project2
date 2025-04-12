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

# classes for the tellers
class Teller(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        print(f"Teller {self.id} []: ready to serve")
        print(f"Teller {self.id} []: waiting for a customer")
        while True:
            time.sleep(0.1)  # this is the simulate the sleep time
            if customers_served >= 50:
                break

# this is the class for customer threads
class Customer(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        global customers_served

        # choose a transaction to do 0: withdrawl and 1:deposit
        transaction_id = random.randint(0, 1)
        if( transaction_id == 0):
            print(f"Customer {self.id} []: wants to perform this a withdrawal transaction")
        if( transaction_id == 1):
            print(f"Customer {self.id} []: wants to perform this a deposit transaction")

        #goes to the bank
        print(f"Customer {self.id} []: going to bank")

        #only two customers at allowed through the doors are once and once they enter they stand in line
        door_semaphore.acquire()
        print(f"Customer {self.id} []: entering bank")
        door_semaphore.release()
        print(f"Customer {self.id} []: getting in line")

        # they wave hi to the teller
        teller_id = random.randint(0, 2)  # Randomly select a teller
        print(f"Customer {self.id} [Teller {teller_id}]: Waves hi")

        # and then they leave the bank
        print(f"Customer {self.id} [Customer {self.id}]: Leaving bank")


        # this increments the number of saved customers
        global customers_served_lock
        with customers_served_lock:
            customers_served += 1


# global variables assuming we have 50 customers
customers_served = 0
customers_served_lock = threading.Lock()

# create and start teller threads
tellers = [Teller(i) for i in range(3)]
for teller in tellers:
    teller.start()

# create customer threads
customers = [Customer(i) for i in range(50)]
for customer in customers:
    customer.start()

# wait for the customers to finish
for customer in customers:
    customer.join()

print("All customers have waved hi and left.")

# wait for the tellers to finish after since they'll be working after
for i, teller in enumerate(tellers):
    teller.join()
    print(f"Teller {i} []: leaving for the day")

#basically program finished type beat
print("The bank closes for the day.")

