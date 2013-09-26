import bisect 
import hashlib



def get_hash(value):
    return int(hashlib.sha1(value).hexdigest(),16)%1000000/1000000.0

def makeHashTable(machines = 1,replicas = 1):
    return sorted([(i,j,get_hash(str(i)+"+"+str(j)))   for i in xrange(0,machines) for j in xrange(0,replicas) ],key = lambda x:x[2])

def calculateMachineNo(hashTable,key):
    hashKey = get_hash(key)
    machineNo = bisect.bisect_left([i[2] for i in hashTable ],hashKey)
    if(machineNo == len(hashTable)):
        return hashKey,0
    else:
        return hashKey,hashTable[machineNo][0]
    













if __name__=="__main__":
    print "Enter the number of Machines",
    machines = input()
    print "Enter the number of Replicas",
    replicas = input()
    hashTable = makeHashTable(machines,replicas)
    print "(machine,replica,hash value):"
    for i in hashTable:
        print i
    while(1):
        print "Please enter a key, or (a) to add machine:",
        newMachineOrKey = raw_input()
        if not newMachineOrKey:
            print "Enter a valid string"
            continue
        if(newMachineOrKey == 'a'):
            machines = machines+1
            listNew = [ (machines,i,get_hash(str(machines)+"+"+str(i))) for i in xrange(0,replicas)]
            #print listNew
            for i in listNew:
                hashTable.append(i)
            hashTable.sort(key = lambda x:x[2])
            print "New Hash Has Been Alloted"
            for i in hashTable:
                print i
        elif(newMachineOrKey=='q'):
            exit()
        else:
            value,machine = calculateMachineNo(hashTable,newMachineOrKey)
            print "hash(Key: "+newMachineOrKey+") = "  +str(value)+", Goes to machine "+str(machine) 

