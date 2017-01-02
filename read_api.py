
import sys
import csv

from nsone import NSONE
from nsone.rest.errors import AuthException
from twisted.internet import defer
from twisted.internet import reactor

def handleSuccess(*args):
    print "Success. Shutting down"
    reactor.stop()

def handleError(failure):
    print(failure)
    reactor.stop()


@defer.inlineCallbacks
def main(fname,key):
   # connect the nsone API
   nsone = NSONE(apiKey=key)

   # Create a dictionary to store type of records and their attributes
   services = {'A':'add_A','MX':'add_MX','TXT':'add_TXT','CNAME':'add_CNAME'}

 
   with open(fname) as csvfile:
       # Read csv
       reader = csv.DictReader(csvfile)

       for row in reader:
           # Just print the zone and record data    
           print(row['Name'], row['Zone'], row['Type'], row['TTL'], row['Data'])
           
           try:
               # Try creating a zone 
               zone = nsone.createZone(row['Zone'], nx_ttl=row['TTL'])
               print("Created a new zone %s"%(row['Zone']))
            
           except Exception, R:
               # Dismiss  - zone exists - load one
               zone = nsone.loadZone(row['Zone'])
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

 

if __name__=='__main__':
   fname = sys.argv[1] 
   key = sys.argv[2] 
   m = main(fname,key)

   m.addCallback(handleSuccess)
   m.addErrback(handleError)
   reactor.run()
