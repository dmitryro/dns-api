
import sys
import csv

from nsone import NSONE
from twisted.internet import defer
from twisted.internet import reactor

def handleSuccess(*args):
    print "Success. Shutting down"
    reactor.stop()

def handleError(failure):
    print(failure)
    reactor.stop()

@defer.inlineCallbacks
def main(fname):
   # connect the nsone API
   nsone = NSONE(apiKey='YmZB3gnt2MxolyCCKMOR')

   # Open the csv file, parse and populate
   
   with open(fname) as csvfile:
       reader = csv.DictReader(csvfile)

       for row in reader:
           print(row['Name'], row['Zone'], row['Type'], row['TTL'], row['Data'])
           
           try:
               zone = nsone.addZone(row['Zone'], nx_ttl=row['TTL'])
               print("Created ne zone %s"%(row['Zone']))

           except Exception, R:
               zone = nsone.loadZone(row['Zone'])
               print("Zone %s already exists - loading"%(row['Zone']))
           
           if row['Type']=='A':
               try:
                   zone.add_A(row['Zone'],row['Data']) 
                   print("Added A record %s %s"%(row['Zone'],row['Data']))    
               except Exception, R:
                   print("Dismissed A  record %s %s"%(row['Zone'],row['Data']))
  
           elif row['Type']=='CNAME':
               try:
                   zone.add_CNAME(row['Zone'],row['Data'])
                   print("Added CNAME record %s %s"%(row['Zone'],row['Data']))
               except Exception, R:
                   print("Dismissed CNAME  record %s %s"%(row['Zone'],row['Data']))

           elif row['Type']=='TXT':
               try:
                   zone.add_TXT(row['Zone'],row['Data'])
                   print("Added TXT record %s %s"%(row['Zone'],row['Data']))
               except Exception, R:
                   print("Dismissed TXT  record %s %s"%(row['Zone'],row['Data']))

           elif row['Type']=='MX':
               try:
                   zone.add_MX(row['Zone'],row['Data'])
                   print("Added MX record %s %s"%(row['Zone'],row['Data']))
               except Exception, R:
                   print("Dismissed MX  record %s %s"%(row['Zone'],row['Data']))

 
 
                #zone = nsone.addZone(row['Zone'], nx_ttl=row['TTL'])            
#
 #              print(zone)

if __name__=='__main__':
   fname = sys.argv[1]  
   m = main(fname)
   m.addCallback(handleSuccess)
   m.addErrback(handleError)
   reactor.run()
