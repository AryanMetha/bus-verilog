Say N =10 = number of nodes ;

step 1: generating the erdros reyni graph : each edge exists with probabilty=0.1 

step 2: node strucutre: 
 so for each node we will have a corresponding 10 bit string  where the ith element =1 if that node has an edge with the ith phase node (ki =1 for ith node -edge with itself)
  additionally each node will also have two 16 bit variables : phase value and current sum 
 all nodes are conected by a 16 bit bus where they can publish their current phase or read others phase
                                                                                                                                         
step 3: control unit
control unit will take in input as clock and ready pulse and give out  a N(=10) bit string which will be one hot encoded ( the element which is 1 will correspond to the node which is current publishing)
 this 10 bit input is also passed into an encoder to convert it into 4 bit number ( one to 10) which is also recevied by each pahse node telling it which node is currently pusblishing)
   (so in total each phase node gets 5 bit input from control - one command bit and 4 bits for telling it the id of the piublisher)
    the node then decieds whetehr or not to add the value on the bus to its current sum based on the id it receives and the 10 bit edge encoding it has telling it whether or not it has an edge with the publishing node

    the control unit keep cycling through the one hot encoded input N' times (sufficient for convergence )
step 4: solve the maxcut problem using the values of the phases obtained
                                                                                                                                      
                                                                                                                                         

                                                                                                                                         
