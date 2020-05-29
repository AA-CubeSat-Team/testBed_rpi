
import csv 
import time

kk = 0

header = ['entry', 'time', 'type1', 'type2'] 

file = open('output.csv', 'w', newline ='') 
with file:   
    write = csv.writer(file) 
    write.writerow([header[0], header[1], header[2], header[3]]) 



kk = kk + 1
ts = time.gmtime()
time1 = time.strftime("%H:%M:%S %Z", ts)

reply1 = [101, 201]                                                  # reply input from spi.xfer

row1_ll = [[kk], [time1], reply1]
row1  = [val for sublist in row1_ll for val in sublist]             # flattens list-of-lists into single list

file = open('output.csv', 'a', newline ='') 
with file:   
    write = csv.writer(file) 
    write.writerow([row1[0], row1[1], row1[2], row1[3]]) 



# GOAL: given list (SPI output) write a new row in existing CSV file
# TO DO: 
#   o   not able to make list into row without indexing each entry (if unique, fine to do)
#   o   able to interpret spi.xfer output? may need to treat reply list first
#   o   configure such that input data is self-contained list
#   x   need to create unique CSV infrastructure for each data request?
#   x   call as a function every time data is requested from RWA?
#   x   need to create CSV outside of request loop, so that each time called adds row to pre-existing CSV  
#   x   need to set kk=0 outside loop, also need unique counters for each type of function since each has own CSV   

# IMPLEMENTATION: 
#   create CSV
#   writerow(header)
#   spi.xfer request to RWA
#   reply = spi.xfer()    assume reply is a list
#   row1 = [kk, time1, [reply]]
#   append CSV
#

# open file in "w - write" mode to create CSV file in current directory 
# open file in "a - append" mode to add rows to the bottom of the CSV file

# spi.xfer returns data as list of bytes represented as integers