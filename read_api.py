
import sys
import csv

from nsone import NSONE
from twisted.internet import defer
from twisted.internet import reactor,task
from twisted.internet.task import react

def handleMainSuccess(*args):
    print "Success. Shutting down"
    reactor.stop()
    return
   
def handleMainError(failure):
    print(failure)
    reactor.stop()
    return

def handleSuccess(*args):
    print "Success. Shutting down"
    return

def handleError(failure):
    print(failure)
    return


@defer.inlineCallbacks
def read_record(key,row):
    # Create a dictionary to store type of records and their attributes  
    nsone = NSONE(apiKey=key)
    services = {'A':'add_A','MX':'add_MX','TXT':'add_TXT','CNAME':'add_CNAME'}

    try:
        # Try creating a zone
        zone = yield nsone.createZone(row['Zone'], nx_ttl=row['TTL'])
        print("Created a new zone %s"%(row['Zone']))

    except Exception, R:
        # Dismiss  - zone exists - load one
        zone = yield nsone.loadZone(row['Zone'])
        print("Zone %s already exists - loading"%(row['Zone']))

           # we get the attribute dynamically to make it compact
    func = getattr(zone,services[row['Type']])

    try:
        # call the add_X based on selection from dictionary
        func(row['Zone'],row['Data'])
        print("Added %s record %s %s"%(row['Type'],row['Zone'],row['Data']))

    except Exception, R:
        # Dismiss existing - nothing done, move on
        print("Dismissed %s record %s %s"%(row['Type'],row['Zone'],row['Data']))
          
    qps = yield zone.qps()
    defer.returnValue(qps)


def main(fname,key):
   # connect the nsone API

   tasks  = []

   with open(fname) as csvfile:
       # Read csv
       reader = csv.DictReader(csvfile)

       for row in reader:
           # Just print the zone and record data    
           print(row['Name'], row['Zone'], row['Type'], row['TTL'], row['Data'])
           #d = task.deferLater(reactor, 0.05, read_record,key,row)
           r = read_record(key,row)
           tasks.append(r)
           dl = defer.DeferredList(tasks)

           d.addCallback(handleSuccess)
           d.addErrback(handleError) 

     
if __name__=='__main__':
   fname = sys.argv[1] 
   key = sys.argv[2] 

   d = task.deferLater(reactor, 0.5, main, fname, key)
   d.addCallback(handleMainSuccess)
   d.addErrback(handleMainError)
   reactor.run()


