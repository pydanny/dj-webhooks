.. :changelog:

History
-------

0.2.2 (2014-05-??)
+++++++++++++++++++

* Added identifier field to WebhookTarget
* Added identifier argument to orm and redisq senders.
* Added South migrations for Django=<1.6.
* Declared coding in all Python modules. 
* Added verbose names to models

0.2.1 (2014-05-17)
++++++++++++++++++

* Removed conf.py file as it just added abstraction.
* Created exlicitly importable hooks. Makes settings management easier.
* Removed utils.py since we no longer do fancy dynamic imports (see previous bullet).
* Coverage now at 100%


0.2.0 (2014-05-15)
++++++++++++++++++

* Refactored the senders to be very extendable.
* Added an ORM based sender.
* Added a redis based sender that uses django-rq.
* Added a `redis-hook` decorator.
* Added admin views.
* Ramped up test coverage to 89%.
* setup.py now includes all dependencies.


0.1.0 (2014-05-12)
++++++++++++++++++

* First release on PyPI.