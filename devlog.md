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

## **04-08-2025 12:01PM Session**

Today I want to implement the basic interaction between the teller and the customer


## **04-08-2025 12:17PM Session**
I have the basic interaction implemented using threads and semaphores but I need to talk 
to make sure what I've done so far is correct. I simulated it using 50 customers, 3 
tellers, and only 5 customers allowed in the bank at a time (similar to how they'll 
only be allowed to access the safe 2 at a time)

## **04-12-2025 4:17PM Session**
God bless the deadline has been extended so I'll try to get most of the work done today. What I've thought 
about since the last session is how I want to set up the program. I'll probably do it all in 
one class and since we don't need a logger this time around that simplifies it a little 
bit.

## **04-12-2025 4:35PM Session**
Working on fixing the output for the tellers and creating proper semaphores + threads that I need 
for the setup. 

