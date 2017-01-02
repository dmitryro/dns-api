==============================
NS1 read api
==============================



How to install
--------------

Run ``python setup.py install`` to install,
or place ``read_api.py`` on your Python path.

You can also install it with: ``pip install dns-api -r requirements.txt``
while placing dns-api==1.0.0 in your  ``requirements.txt``

How to run
--------------
Execute
``read_api.py data.csv apikey``
where ``data.csv`` is the path to the csv file containing the records to
load and ``apikey`` is the NSONE api key from NS1

Twisted Version
---------------
Twisted v.16.6.0 is used with this module. Please note that some of the
older version modules might be backward incompatible.

