# Project 2 Development Log

## **04-06-2025 6:58PM Session**
This project will be simulating a bank system with a teller and customers. Currently, I'm 
confused as to where to begin so I'll start researching on possible ways to approach this program 
and like last time, I plan to program using python.

## **04-06-2025 7:12PM Session**
This is what I currently understand from the project. I have 3 tellers (so three threads for them), 
50 customers (so 50 threads for them?), the shared resources are safe, manager, and door but safe 
and manager need to be protected by semaphores. 
1. Customers can only make deposits or withdraws
2. No customers can enter the bank before it's open 
3. If not free teller then customer must wait in line (i think I'll implement this with a queue)
4. If customer wants to make withdraw -> teller contacts bank manager -> only one teller at a time (semaphores)
5. Only 2 people can access the safe at a time (semaphores)
6. I need some sort of random method to simulate a teller getting permission from the maanger 
7. all the tellers and customers need unique ideas 


Next time, I'll follow the instructions and start by simulating a simple transaction between them for right now. Overall, 
this session was helpful in understanding the base requirements and by next section I hope to have a basic customer, teller 
interaction completed. 