In tradition Hashing the keys go to the respective machine based on the hashing 
function (Say hash(key) mod n).If the  hash function is reasonably good the 
keys will be distributed uniformly very well.But the problem starts when there
is a need to add a new machine to the cluster.The hashing function changes to Say
hash(key) mod (n+1) .This will lead to entirely random and completely new 
distribution of the keys across the machines.

This problem can be solved using consistent hashing whereby the hashed values 
are wrapped along a circle whereby every key goes to the machine in a clockwise
fashion.Now suppose a new machine is to be added to the cluster.This will lead 
moving of 1/n of the keys on a average.

The way I implemented the consistent hashing is by using the hashlib library of 
python to first make a hash table of all the machines and their replicas in a 
circular fashion.Each machine was identifed by a unique number between [0,1].

Now whenever a new key-value pair came the hash value of the machine was calculated by 
the same hash function and the key-value pair went into the machine in a clockwise 
fashion to the machine with next value in the hash table.

Whenever a new machine was added its hash values were calculated with the same hash 
function and the value was added to the hash table again.Now subsequent key-value 
pairs went to the machine based on the new hash table.


Kumar Rishabh
201102103
