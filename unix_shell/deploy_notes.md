
Gunicorn
========
Automatic worker process management. Simple Python conﬁgurations.
a Python WSGI HTTP Server for UNIX, uses a pre-fork worker model. Pre-forking basically means a master creates forks which handle each request. A fork is a completely separate *nix process

Django implements WSGI spec, coming with a light-weight web server used for development.
It is used just for that, it is not made to handle lots of requests or load at any given time.
This needs e.g. Gunicorn or uWSGI.

It is strongly recommend to use Gunicorn behind a proxy server.
Gunicorn is designed to be an application server that sits behind a reverse proxy server that handles load balancing, caching, and preventing direct access to internal resources.    che, to accept HTTP requests.
The reason why people run Nginx and Gunicorn together is that in addition to being a web server,
Nginx can also proxy connections to Gunicorn which brings certain performance benefits

Both Nginx and Gunicorn handle the request. Basically, Nginx will receive the request and if it's a dynamic request then it will give that request to Gunicorn, which will process it, and then return a response to Nginx which then forwards the response back to the original client.
This results in two first tiers of the classic "three tier architecture". The webserver e.g. Nginx will handle many requests for images and static resources. Requests that need to be dynamically generated will then be passed on to the application server e.g Gunicorn. As an aside, the third of the three tiers is the database)


Misc. Deployment Notes
======================

To find all socket files on your system run:
sudo find / -type s


unrelated/general term - An idempotent task is a task that, if stopped midway, doesn't change the state of the system in any way. The task either makes full changes to the system or none at all.

