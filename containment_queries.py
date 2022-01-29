#NIKOS KARIOTIS

import sys
import ast
import time

transactions = []
queries = []

def build_transactions(content):
    global transactions
    
    for line in content:
        transaction = []
        for i in range(len(line)):
            transaction.append(line[i])
        transactions.append(transaction)

   
def build_queries(content):
    global queries

    for line in content:
        querie = []
        for i in range(len(line)):
            querie.append(line[i])
        queries.append(querie)


def naive(qnum):
    global transactions,queries
    results = set()
    
    if(qnum == -1):
        start = time.time()
        
        for querie in queries:
            for ID in range(len(transactions)):
                if(set(querie).issubset(set(transactions[ID]))):
                    results.add(ID)
        end = time.time()
        print("Naive Method computation time = " + str(end-start))
    else:
        querie = queries[qnum]
        start = time.time()
        for ID in range(len(transactions)):
            if(set(querie).issubset(transactions[ID])):
                results.add(ID)
        end = time.time()
        print("Naive method result:" + "\n" + str(results))
        print("Naive Method computation time = " + str(end-start))


def construct_sigfile(transactions):
    transactions_len = len(transactions)
    sigfile = [0 for i in range(len(transactions))]
    for i in range(len(transactions)):
        length = max(transactions[i])
        bitmap_arr = ["0" for j in range(length + 1)]
        for obj in transactions[i]:
            bitmap_arr[length - obj] = "1"
       
        
        bitmap = int("".join(bitmap_arr),base = 2)
           
        sigfile[i] = bitmap
        
    return sigfile


def exact_signature_file(qnum,sigfileTxt):
    global transactions,queries
   
    results = set()
    sigfile = construct_sigfile(transactions)
    
    if(qnum == -1):
        bitmap_queries = []
        
        for querie in queries:
            length = max(querie)
            bitmap_arr = ["0" for j in range(length + 1)]
    
            for obj in querie:
                bitmap_arr[length - obj] = "1"
        
            bitmap = int("".join(bitmap_arr),base = 2)
            bitmap_queries.append(bitmap)

        start = time.time()
        for querie_bitmap in bitmap_queries:
            for ID in range(len(sigfile)):
                if((bin(querie_bitmap & sigfile[ID])) == bin(querie_bitmap)):
                    results.add(ID)
        end = time.time()
        print("Signature file computation time = " + str(end-start))
        
    else:
        querie = queries[qnum]
        length = max(querie)
        bitmap_arr = ["0" for i in range(length + 1)]
        for obj in querie:
            bitmap_arr[length - obj] = "1"
        
        bitmap = int("".join(bitmap_arr),base = 2)
        start = time.time()
       
        for ID in range(len(sigfile)):
            if((bin(bitmap & sigfile[ID])) == bin(bitmap)):

                results.add(ID)

        end = time.time()    
       

        print("Signature file result:" + "\n" + str(results))
        print("Signature file computation time = " + str(end-start))

    for bitmap in sigfile: #writes the sigfile.txt
        sigfileTxt.write(str(bitmap) + "\n")

        
def construct_obj_arr():
    global transactions
    objects = []
    for transaction in range(len(transactions)):
        for elem in range(len(transactions[transaction])):
            if(transactions[transaction][elem] not in objects):
                objects.append(transactions[transaction][elem])
                    
    return objects


def construct_bitslice(transactions):
    objects = construct_obj_arr()
    dictionary = {}
    bitslice = {}
    for i in range(len(objects)):
        dictionary[objects[i]] = ["0" for j in range(len(transactions))]
    
    for k in range(len(transactions)):
        for l in range(len(transactions[k])):
            if(transactions[k][l] in dictionary):
               bitmap = dictionary.get(transactions[k][l])
               length = len(bitmap)
               bitmap[(length - 1) - k] = "1"
    
    for key in dictionary:
        arr = dictionary.get(key)
        bitmap = int("".join(arr),base = 2)
        bitslice[key] = bitmap

    return bitslice
    

def exact_bitslice_signature_file(qnum,bitsliceTxt):
    global transactions,queries
    
    bitslice = construct_bitslice(transactions)
    results = set()

    if(qnum == -1):
        tmp = bitslice.get(queries[0][0])
        start = time.time()

        for i in range(len(queries)):
            for j in range(len(queries[i])):
                next_q = bitslice.get(queries[i][j])
                tmp = bin(next_q & tmp)
                tmp = int(tmp,2)
                
        tmp = bin(tmp)      
        res = list(tmp)  
        for index, value in enumerate(reversed(res)):
            if(value == "1"):
                results.add(index)
        end = time.time()

        
        print("Bitsliced Signature file computation time = " + str(end-start))
        
    else:
        querie = queries[qnum]
        tmp = bitslice.get(querie[0])
        start = time.time()
        
        for i in range(1,len(querie)):
            next_q = bitslice.get(querie[i])
            tmp = bin(next_q & tmp)
            tmp = int(tmp,2)

        tmp = bin(tmp)
        res = list(tmp)
        for index, value in enumerate(reversed(res)):
            if(value == "1"):
                results.add(index)
        end = time.time()
        
        print("Bitsliced Signature file result:" + "\n" + str(results))
        print("Bitsliced Signature file computation time = " + str(end-start))

    
    for key in sorted(bitslice.keys()):
        bitmap = bitslice.get(key)
        bitsliceTxt.write(str(key) + ":  " + str(bitmap) + "\n")
        

def construct_inv_file(transactions):
    objects = construct_obj_arr()
    dictionary = {}
    for i in range(len(objects)):
        dictionary[objects[i]] = []

    for k in range(len(transactions)):
        for l in range(len(transactions[k])):
            if((transactions[k][l] in dictionary) and (k not in dictionary[transactions[k][l]])):
                dictionary[transactions[k][l]].append(k)

    return dictionary

def mergeArrays(arr1, arr2, n1, n2):
    arr3 = []
    i = 0
    j = 0
 
    while ((i < n1) and (j < n2)):
        if (arr1[i] < arr2[j]):
            i = i + 1
        elif(arr1[i] > arr2[j]):
            j = j + 1
        else:
            arr3.append(arr1[i])
            i = i + 1
            j = j + 1

    return arr3


def inverted_file(qnum,invfileTxt):
    global transactions,queries
    
    inv = construct_inv_file(transactions)
    results = set()
    
    if(qnum == -1):
        tmp = inv.get(queries[0][0])
        start = time.time()

        for i in range(len(queries)):
            for j in range(len(queries[i])):
                next_q = inv.get(queries[i][j])
                tmp = mergeArrays(tmp,next_q,len(tmp),len(next_q))

        end = time.time()
                                  
        for k in tmp:
            results.add(k)
        
        print("Inverted file computation time = " + str(end-start))
    else:
        querie = queries[qnum]
        tmp = inv.get(querie[0])
        
        start = time.time()
        
        for i in range(1,len(querie)):
            next_q = inv.get(querie[i])
            tmp = mergeArrays(tmp,next_q,len(tmp),len(next_q))

        end = time.time()    
        for k in tmp:
            results.add(k)

            
        print("Inverted file result:" + "\n" + str(results))
        print("Inverted file computation time = " + str(end-start))
        
    for key in sorted(inv.keys()):
        inv_arr = inv.get(key)
        invfileTxt.write(str(key) + ":  " + str(inv_arr) + "\n")

        
def main(argv):
    global transactions
    sigfile = open("sigfile.txt" , "w")
    bitslice = open("bitslice.txt" , "w")
    invfile = open("invfile.txt" , "w")
    filename1 = argv[1]
    filename2 = argv[2]
    qnum = int(argv[3])
    method = int(argv[4])
    transactions_file = open(filename1 , "r")
    queries_file = open(filename2 , "r")
    file1_content = []
    file2_content = []
    
    for l1 in transactions_file:
        tmp = ast.literal_eval(l1)
        file1_content.append(tmp)

    for l2 in queries_file:
        tmp = ast.literal_eval(l2)
        file2_content.append(tmp)
  
    build_transactions(file1_content)
    build_queries(file2_content)

    if(method == 0):
        naive(qnum)
    elif(method == 1):
        exact_signature_file(qnum,sigfile)
    elif(method == 2):
        exact_bitslice_signature_file(qnum,bitslice)
    elif(method == 3):
        inverted_file(qnum,invfile)
    elif(method == -1):
        naive(qnum)
        exact_signature_file(qnum,sigfile)
        exact_bitslice_signature_file(qnum,bitslice)
        inverted_file(qnum,invfile)
    else:
        print("Wrong choice")

    transactions_file.close()
    queries_file.close()
    sigfile.close()
    bitslice.close()
    invfile.close()
    
if __name__ == "__main__":
    main(sys.argv)
