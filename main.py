import threading
import time
import random

# let's assume only 5 customers are allowed inside at one
door_semaphore = threading.Semaphore(5)

# classes for the tellers
class Teller(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        print(f"Teller {self.id} [Teller {self.id}]: Ready to greet customers")
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

        # this is them entering through the door
        print(f"Customer {self.id} [Customer {self.id}]: Waiting to enter bank")
        door_semaphore.acquire()
        print(f"Customer {self.id} [Customer {self.id}]: Entered bank")

        # they wave hi to the teller
        teller_id = random.randint(0, 2)  # Randomly select a teller
        print(f"Customer {self.id} [Teller {teller_id}]: Waves hi")

        # and then they leave the bank
        print(f"Customer {self.id} [Customer {self.id}]: Leaving bank")
        door_semaphore.release()

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
for teller in tellers:
    teller.join()

#basically program finished type beat
print("Bank is now closed.")

