`socket`
--------
The Python standard library module provides a low-level networking interface. This interface is common across different programming languages since it uses OS-level system calls.
A socket represents an endpoint of a network communication, and can be in one of several states:

`Ready`, the initial state. `Bound`, meaning that it has been bound to an address ready for incoming connections
`Listening`, meaning that it is listening for incoming connections
`Open`, meaning that it is ready for sending and receiving data;
`Closed`, meaning that it is no longer active.

Python provides two levels of access to network services. At a low level, you can access the basic socket support in the underlying operating system. At higher-level access to specific application-level network protocols, such as FTP, HTTP,

**Socket interfaces**

A socket programming interface provides the routines required for interprocess communication between applications, either on the local system or spread in a distributed, TCP/IP based network environment.
Besides TCP/IP based sockets, UNIX systems provide socket interfaces for interprocess communication (IPC) within the local UNIX host itself.

TCP/IP is the best-known transport protocol (In the OSI layer model). FTP is a protocol at a higher level used to get/put data files from/to a remote host system. HTTP is another
protocol at a a higher level (application level). Client/server (distributed) applications communicating over an enterprise intranet or the internet use the TCP/IP socket programming interface in establishing peer-to-peer communication.

A TCP connection is defined by two endpoints aka sockets.
An endpoint (socket) is defined by the combination of a network address and a port identifier. Note that address/port does not completely identify a socket. The purpose of ports is to differentiate multiple endpoints on a given network address. You could say that a port is a virtualised endpoint. This virtualisation makes multiple concurrent connections on a single network interface possible.
Web servers normally use port 80, SMTP uses port 25, FTP uses port 20.

    It is the socket pair (the 4-tuple consisting of the client IP address, client port number, server IP address, and server port number) that specifies the two endpoints that uniquely identifies each TCP connection in an internet. (TCP-IP Illustrated Volume 1, W. Richard Stevens)
    A connection is fully specified by the pair of sockets at the ends. A local socket may participate in many connections to different foreign sockets.

A single listening port can accept more than one connection simultaneously.

To reiterate: Sockets are the endpoints of a bidirectional communications channel. Sockets may communicate within a process, between processes on the same machine, or between processes on different continents. Sockets may be implemented over a number of different channel types: Unix domain sockets, TCP, UDP etc.

The definition of socket is not helpful from a programming perspective because it is not the same as a socket object, which is the endpoint of a particular connection. To a programmer, and most of this question's audience are programmers, this is a vital functional difference.

To create a socket, you must use the socket.socket() function available in socket module, which has the general syntax −

    s = socket.socket (socket_family, socket_type, protocol=0)

Once you have socket object, then you can use required functions to create your client or server program.
Once you have a socket open, you can read from it like any IO object. When done, remember to close it, as you would close a file.

    #server.py
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.bind((host, port))
    s.listen(5)
    while True:
       c, addr = s.accept()
       print('Got connection from', addr)
       c.send(b'Thank you for connecting')
       c.close()

    #client.py
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, 12345))
    print (s.recv(1024))
    s.close()

**Websockets**

They are normal sockets with some framing and an HTTP-compatible handshake. The HTTP-compatible handshake is just to allow WebSocket connection on the same port that a webserver is running on.

HTTP is a stateless protocol, which means that the connection between the browser and the server is lost once the transaction ends. The opening and closing creates overhead, and the other limitation with HTTP was that it was a “pull” paradigm. The browser would request or pull information from servers, but the server couldn’t push data to the browser when it wanted to. This means that browsers would have to poll the server for new information by repeating requests.
For more real time interaction, or real time transfer or streaming of data, HTTP and REST aren’t the best suited protocol and abstraction combination. This is where Sockets and WebSockets shine.

Weather station tutorial
------------------------
[Article link](https://stackabuse.com/basic-socket-programming-in-python/). For simplicity, our example server only outputs the received data to stdout. The idea behind the client/server application is a sensor in a weather station, which collects temperature data over time and sends the collected data to a server application, where the data gets processed further.

Both parties communicate with each other by writing to or reading from the network socket. In this case both the client and the server run on the same computer.

**Server**

With the help of the `listen()` method the server listens for incoming connections on the specified port. In the `while` loop the server waits for incoming requests and accepts them using the `accept()` method. The data submitted by the client is read via `recv()` method as chunks of 64 bytes

    import socket

    # create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    local_hostname = socket.gethostname()
    ip_address = socket.gethostbyname(local_hostname)
    print(f"working on {local_hostname} ({socket.getfqdn()}) with {ip_address}")
    server_address = (ip_address, 23456)
    print(f'starting up on {server_address} port 23456')
    sock.bind(server_address)
    # listen for incoming connections (server mode) with one connection at a time
    sock.listen(1)

    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print ('connection from', client_address)
            while True:
                data = connection.recv(64)
                if data:
                    print(f'Data: {data}')
                else:
                    print("no more data.")
                    break
        finally:
            connection.close()

**Client**

code is mostly similar to the server side, except for the usage of the socket - the client uses the `connect()` method, instead. In a for loop the temperature data is sent to the server using the `sendall()` method.

    import socket
    import time

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    local_hostname = socket.gethostname()
    local_fqdn = socket.getfqdn()
    ip_address = socket.gethostbyname(local_hostname)
    server_address = (ip_address, 23456)
    sock.connect(server_address)
    print(f'connecting to {local_hostname} ({local_fqdn}) with {ip_address}')

    # define example data to be sent to the server
    temperature_data = ["15", "22", "21", "26", "25", "19"]
    for entry in temperature_data:
        print(f'data: {entry}')
        new_data = str(f"temp: {entry}\n").encode("utf-8")
        sock.sendall(new_data)
        time.sleep(2)
    sock.close()

Python threads are plain old POSIX threads. As OS-level threads (pthreads, windows threads, or such) they rely on OS scheduling. Note that python threads will not distribute among cores, due to the semantics of the GIL.

Since the threads created by Python are normal OS threads, the OS is responsible for supervising these threads and scheduling aspects. The interpreter does the book keeping on which thread is running when the context switch happens etc.
The GIL is needed since each running thread spawned by the interpreter requires exclusive access to data structures.
Because of GIL, there is considerable lag time that is attributed to communication (thread signalling), GIL battle, thread wake up time and GIL acquisition.

**WebSockets - More**

WebSocket is a full-duplex communication channel over one single TCP-type connection. It is an independent TCP-type protocol and its only association to HTTP is that its handshake is intepreted by HTTP servers as an Upgrade request. HTTP 1.1 introduced an “Upgrade” header field and this connection “Upgrade” must be sent by the client (in other words, this “Upgrade” header is sent by SocketIO javascript client to tell the server that this is a WebSocket connection)

A protocol like HTTP uses a (BSD socket) socket for only one transfer. The client sends the request, then reads the reply and the socket is discarded. This means that a HTTP client can detect the end of the reply by receiving 0 bytes.

For WebSocket, once a connection is established, the client and server can send WebSocket data or text frames back and forth in full-duplex mode. The data itself is minimally framed, containing a small header and the payload. WebSocket transmissions are described as “messages” where a single message can optionally be splitted across several data frames. This can allow for sending of messages where initial data is available but the complete length of the message is unknown (it sends one data frame after another until the end is reached and marked with the FIN bit).

**Socket.IO**

Socket.IO is a javascript library for real-time web applications. It has two parts

1) a client side library that runs in the browser; and
2) a server-side library for node.js.

Both components have identitical API and are event-driven. There are implementations for the server-side library in other languages e.g. gevent-socketio - https://github.com/abourget/gevent-socketio




Gevent and Greenlets
--------------------

Gevent is the use of simple, sequential programming in python to achieve scalability provided by asynchronous IO and lightweight multi-threading (as opposed to the callback-style of programming using Twisted’s Deferred).

It is built on top of libevent/libev (for asynchronous I/O) and greenlets (lightweight cooperative multi-threading).

The job of libevent/libev is to handle event loops. As we will learn in the SocketIO sections later on, our SocketIOServer is an event loop which can emit specific results, on the occurrence of specific events. This is essentially how our SocketIOServer instance will know when to send a message to the client, hence real-time streaming of data from the server to the client, on the occurrence of specific events.

**libevent/libev**

The libevent API provides a mechanism to execute a callback function when a specific event occurs on a file descriptor or after a timeout has been reached. It also supports callbacks triggered by signals and regular timeouts. from 1.0 onwards, gevent is based on libev.

**gevent with I/O operations**

gevent’s greenlet does not give us magical powers to suddenly achieve parallelism. There will only be one greenlet running in a particular process at any time.
Because of this, CPU-bound apps do not gain any performance gain from using gevent (or python’s standard threading).

gevent is only useful for solving I/O bottlenecks. Because our gevent python application is trapped between a http connection, a database and perhaps a cache and/or messaging server, gevent is useful for us.

Note, gevent does not handle regular file read-write (I/O) well. File I/O does not really work the asynchronous way. It blocks! Expect your application to block on file I/O, so load every file you need up front before handling requests or do file I/O in a separate process (Pipes support non-blocking I/O).

Here’s a simple example of how we can make use of gevent’s I/O performance advantage in our code. In a typical web request-respond cycle, we may want to run concurrent jobs that

1) retrieve data source from a particular database,
2) make a get request to a 3rd party (or even in-house) API on a different application that returns us json,
3) instantiates an SMTP connection to send out an email,

We would like to execute them in a concurrent way where the tasks will switch away if it encounters an I/O bottleneck in one of the above I/O jobs. So we can write:

    def handle_view(request):
        jobs = []
        jobs.append(gevent.spawn(orm_call, 'Andy'))
        jobs.append(gevent.spawn(call_facebook_graph_api, 14213))
        jobs.append(gevent.spawn(email, 'me@mysite.com'))
        gevent.joinall()

A switch between the two subtasks is known as a context switch. A context switch in gevent is done through *yielding*. In this example we have two contexts which yield to each other through invoking `gevent.sleep(0)`

    def foo():
        print('Running in foo')
        gevent.sleep(0)
        print('Explicit context switch to foo again')

    def bar():
        print('Explicit context to bar')
        gevent.sleep(0)
        print('Implicit context switch back to bar')

    # Block until all threads complete.
    gevent.joinall([
        gevent.spawn(foo),
        gevent.spawn(bar),
    ])

![](./images/flow.gif)

[Further reading: http://sdiehl.github.io/gevent-tutorial/](http://sdiehl.github.io/gevent-tutorial/)

**Summary**

1) gevent helps us to reduce the overheads associated with threading to a minium. (greenlets)
2) event helps us avoid resource wastage during I/O by using asynchronous, event-based I/O. (libev)
3) gevent is well suited for concurrency with webservers, databases, caches, messaging frameworks as these are I/O-bound
4) The exception to I/O performance gain is file I/O. Load file upfront or execute file I/O in a separate process
5) gevent is not a solution for multicore CPU-bound programs

In python, we implement greenlets via the gevent package and we implement pthreads via python’s built-in threading module.

Greenlets are a lightweight cooperative threads - different from conventional POSIX threads (pthreads). They can be described as coroutine (cooperative routines).
POSIX threads use the operating system’s native ability to manage multithreaded processes. When we run pthreads, the kernel schedules and manages the various threads that make up the process.

Green threads emulate multithreaded environments without relying on any native operating system capabilities. Green threads run code in user space that manages and schedules threads.

You can think of greenlets more like cooperative threads. What this means is that there is no scheduler pre-emptively switching between your threads at any given moment - instead your greenlets voluntarily/explicitly give up control to one another at specified points in your code.

Does the GIL affect them? Can there be more than one greenlet running at a time?
Only one code path is running at a time - the advantage is you have ultimate control over which one that is.

*side note*: both processes and threads are independent sequences of execution. The typical difference is that threads (of the same process) run in a shared memory space, while processes run in separate memory spaces.
Threads require less overhead than "forking" or spawning a new process because the system does not initialize a new system virtual memory space and environment for the process.

Most servers limit the size of their worker pools to a relatively low number of concurrent threads, due to the high overhead involved in switching between and creating new threads. While threads are cheap compared to processes (forks), they are still expensive to create for each new connection.

The gevent module adds greenlets to the mix. Greenlets behave similar to traditional threads, but are very cheap to create. A gevent-based server can spawn thousands of greenlets (one for each connection) with almost no overhead. Blocking individual greenlets has no impact on the servers ability to accept new requests. The number of concurrent connections is virtually unlimited.
To summarize:

*pthreads*

Can switch between threads pre-emptively, switching control from a running thread to a non-running thread at any time

Can run more than one thread on multicore machines. However python’s GIL means concurrency is only effective for I/O-bound programs

Race conditions can occur when implementing multi-threading code. Use locks to manage mutex to avoid race conditions.

*greenlets*

Only switch when control is explicitly given up by a thread - when using yield() or wait() - or when a thread performs a I/O blocking operation such as read or write

Can only run on one single CPU and is useful for I/O-bound programs

There’s no possibility of two threads of control accessing the same shared memory at the same time for greenlets so there will not be any race conditions.

    from greenlet import greenlet

    def test1():
        print 12
        gr2.switch()
        print 34


    def test2():
        print 56
        gr1.switch()
        print 78

    gr1 = greenlet(test1)
    gr2 = greenlet(test2)
    gr1.switch()

Consider this synthetic example of task function which is non-deterministic (i.e. its output is not guaranteed to give the same result for the same inputs), whereby the task function pauses for sometime (analogy to web request):

    def task(pid):
        """ Some non-deterministic task """
        gevent.sleep(random.randint(0,2)*0.001)
        print('Task %s done' % pid)

    def synchronous():
        for i in range(1,10):
            task(i)

    def asynchronous():
        threads = [gevent.spawn(task, i) for i in xrange(10)]
        # Block until all threads complete.
        gevent.joinall(threads)

    print('Synchronous:')
    synchronous()

    print('Asynchronous:')
    asynchronous()

    Synchronous:
    Task 1 done
    Task 2 done
    Task 3 done
    ...

    Asynchronous:
    Task 1 done
    Task 5 done
    Task 6 done
    ...

*gevent.spawn* wraps up the given function inside of a Greenlet thread. The list of initialized greenlets are stored in the array threads which is passed to the `gevent.joinall` function which blocks the current program to run all the given greenlets. The execution will step forward only when all the greenlets terminate.

The important fact to notice is that the order of execution in the async case is essentially random and that the total execution time in the async case is much less than the sync case.

The perennial problem involved with concurrency is known as a race condition. Simply put, a race condition occurs when two concurrent threads / processes depend on some shared resource but also attempt to modify this value.
The best approach to this is to simply avoid all global state at all times.

*Program Shutdown*

Greenlets that fail to yield when the main program receives a SIGQUIT - so called "zombie processes" which need to be killed from outside of the Python interpreter.

    def run_forever():
        gevent.sleep(1000)

    if __name__ == '__main__':
        gevent.signal(signal.SIGQUIT, gevent.kill)
        thread = gevent.spawn(run_forever)
        thread.join()

*Queues*

Queues are ordered sets of data that have the usual put / get operations but are written in a way such that they can be safely manipulated across Greenlets.

For example if one Greenlet grabs an item off of the queue, the same item will not be grabbed by another Greenlet executing simultaneously.

    import gevent
    from gevent.queue import Queue

    tasks = Queue()

    def worker(n):
        while not tasks.empty():
            task = tasks.get()
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0)

        print('Quitting time!')

    def boss():
        for i in xrange(1,25):
            tasks.put_nowait(i)

    gevent.spawn(boss).join()

    gevent.joinall([
        gevent.spawn(worker, 'steve'),
        gevent.spawn(worker, 'john'),
        gevent.spawn(worker, 'nancy'),
    ])

    Worker steve got task 1
    Worker john got task 2
    Worker nancy got task 3
    Worker steve got task 4
    Worker john got task 5
    Worker nancy got task 6
    ...
    Quitting time!
    Quitting time!
    Quitting time!

*Timeouts*

Timeouts are a constraint on the runtime of a block of code or a Greenlet.

    seconds = 10
    timeout = Timeout(seconds)
    timeout.start()

    def wait():
        gevent.sleep(10)

    try:
        gevent.spawn(wait).join()
    except Timeout:
        print('Could not complete')

They can also be used with a context manager, in a `with` statement.

*Greenlet State*

Like any other segment of code, Greenlets can fail in various ways. A greenlet may fail to throw an exception, fail to halt or consume too many system resources.
The internal state of a greenlet is generally a time-dependent parameter. There are a number of flags on greenlets which let you monitor the state of the thread, e.g. `started`, `ready()`, `successful()` etc

*Monkey patching*

If you see: `from gevent import monkey` and `monkey.patch_all()`, this goes through and monkeypatches Python's stdlib, "green"-ing the libraries as it goes.

**Python sockets**

Python’s standard socket module can easily be used to create a socket for IPC (Inter-Process Communication).

When a socket is created, an endpoint for communication becomes available and a corresponding file descriptor is returned - an abstract indicator for accessing a file with an integer value of 0, 1 or 2 corresponding to stdin, stdout or stderr.

Our webservers can be implemented in whatever language but the basis from which data is passed between each other via the HTTP (TCP) protocol rest upon sockets. Sockets are the fundamental building block from which HTTP, HTTPS, FTP, SMTP protocols (all of these are TCP-type protocols) are defined.

**Long Polling**

Unlike websockets it works in all browsers pretty consistently & does "push" data very well.

The technique around long-polling essentially just means that, rather than quickly finishing a request & closing out the connection, the server starts the response but never closes the connection. To the client, it looks like things are taking a long time to load, but to the server, you're stalling for time/data.

    import gevent
    from gevent.queue import Queue, Empty
    from gevent.pywsgi import WSGIServer
    import simplejson as json

    data_source = Queue()

    def producer():
        while True:
            data_source.put_nowait('Hello World')
            gevent.sleep(1)

    def ajax_endpoint(environ, start_response):
        status = '200 OK'
        headers = [
            ('Content-Type', 'application/json')
        ]

        start_response(status, headers)

        while True:
            try:
                datum = data_source.get(timeout=5)
                yield json.dumps(datum) + '\n'
            except Empty:
                pass

    gevent.spawn(producer)
    WSGIServer(('', 8000), ajax_endpoint).serve_forever()
