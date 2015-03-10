dj-sso-server
==============
``dj-sso-server`` is a Django application that provides Single Sign-on feature for your project.

The ``dj-sso-server`` application works as a **SSO provider** , you can use ``dj-sso-client`` (https://github.com/feifangit/dj-sso-client) as the **SSO client** in other projects need SSO.


Installation
------------
Install by command ``pip install dj-sso-server``

The dependent package ``dj-api-auth`` (https://github.com/feifangit/dj-api-auth) will be installed automatically. 


How it works
-------------
- Based on the ``dj-api-auth`` module, we can create an API key with SSO related APIs initially included. All the API communications between ``dj-sso-server`` and ``dj-sso-client`` are protected by ``dj-api-auth``
- The API key will also be bind with a **host** which is used to limit the origin of SSO requests. 
- SSO work flow with ``dj-sso-client``

	1. Firstly, ``dj-sso-client`` applies a **request key** via API ``reqeusttoken/`` on ``dj-sso-server``
	2. The **request key** in ``dj-sso-server`` side will be kept in cache for 5 minutes, so the whole SSO login process should be done in 5 minutes.
	3. With the **request key**, ``dj-sso-client`` redirects user to SSO login page on SSO provider, and get **auth token** if login success. ``dj-sso-server`` will 

		- verify the request origin
		- verify **request key** validity (expired?)
		- save user information in cache 

	4. ``dj-sso-client`` verifies the **auth token** with ``dj-sso-server`` via API ``authtoken/``, and get a ``SSOUser`` object. 
	5. ``dj-sso-server`` delete the **request key** from cache once the ``authtoken/`` is called.

- If there's an already logged-in account on ``dj-sso-server`` (say, the project where SSO provider is placed also provides other features, and there's a valid cookies in browser side and valid session on server side), user can select to continue with that logged account.
- SSO login through ``dj-sso-server`` with not affect the login status on ``dj-sso-server``.


Attention
----------
Since **request keys** are stored in cache waiting for verification or expiration. If you have multiple application process running in your deployment (gunicorn etc.), please use proper cache system that can be shared between processes. 

Memcached and Redis are both great for caching, be aware, the **Local-memory caching** (``django.core.cache.backends.locmem.LocMemCache``) is a toy for local debugging.


Add ``dj-sso-server`` to project
--------------------------------
1. Add ``djapiauth`` and ``djssoserver`` to ``INSTALLED_APPS`` in ``sttings.py``
2. Assign an URL to the module

.. code-block:: python
	
	# add auth for a browser-oriented view
	url(r'^sso/', include("djssoserver.urls"))
	#...


Settings
--------
- **SSO_SERVER_USER_MODEL_TO_DICT_CLS**
	- optional, a path to JSON encoder class
	- the default encoder processes ``datetime``, ``date``, ``time`` and ``decimal.Decimal``

	.. code-block:: python
		
		# DjangoJSONEncoder from Django 1.7 source code
		class DjangoJSONEncoder(json.JSONEncoder):
		    """
		    JSONEncoder subclass that knows how to encode date/time and decimal types.
		    """

		    def default(self, o):
		        # See "Date Time String Format" in the ECMA-262 specification.
		        if isinstance(o, datetime.datetime):
		            r = o.isoformat()
		            if o.microsecond:
		                r = r[:23] + r[26:]
		            if r.endswith('+00:00'):
		                r = r[:-6] + 'Z'
		            return r
		        elif isinstance(o, datetime.date):
		            return o.isoformat()
		        elif isinstance(o, datetime.time):
		            if is_aware(o):
		                raise ValueError("JSON can't represent timezone-aware times.")
		            r = o.isoformat()
		            if o.microsecond:
		                r = r[:12]
		            return r
		        elif isinstance(o, decimal.Decimal):
		            return str(o)
		        else:
		            return super(DjangoJSONEncoder, self).default(o)


Scan API
---------
In order to discover and manage APIs, after ``dj-sso-server`` is added in an accessible ``urls.py``, run command ``python manage.py reloadentrypoints`` to collect APIs to database.


Create API key for SSO
-----------------------
1. From your admin site, create an API key at ``Single sign-on/SSO credential``. All SSO related APIs will assigned to this API Key automatically.
2. After the API key for SSO is ready, you can assign more APIs for this API key at ``API Auth/Credential`` from admin site


Customize SSO login page
------------------------
You can add styles to your own SSO login page. simply create ``djsso/ssologin.html`` under the ``templates`` folder. Revamp it by imitating the 
`original page  
<https://github.com/feifangit/dj-sso-server/blob/master/djsso/templates/djsso/ssologin.html>`_


SSOUser object
---------------
``dj-sso-client`` gets a ``SSOUser`` object whatever the User model is used in SSO provider project.

See detail in README file of ``dj-sso-client`` (https://github.com/feifangit/dj-sso-client)



DEMO
-----
We have a SSO provider application running on Heroku (https://dj-sso-sample.herokuapp.com/).

**Source code**: under ``example`` folder

To try the demo out, check out the README file of ``dj-sso-client`` (https://github.com/feifangit/dj-sso-client)
