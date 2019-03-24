Microservices architecture
--------------------------
Building (or breaking up) an application into smaller, discrete pieces that exist independently from one another.

Advantages include:

- More efficient troubleshooting and maintenance. Whereas changes to a monolithic application put the entire system at risk, microservices allow you to isolate services independently.
- Allow greater speed and agility in development and deployment. Instead of QA, acceptance testing, and deploying to production
the entire app each time any change or update is made, you only need to update the service component,
which is independently deployable from other services that form the application.
- Improved scalability and reduced infrastructure costs from the ability to scale individual services as needed rather than the entire app.
- Greater technology flexibility as no need to run an entire application with the same languages, tools, and platforms
- Greater team flexibility; the software team can be split into smaller teams so each team can release new features at their own rate

Microservices should be loosely coupled components, components that you can test independently.
Individual modules are responsible for highly defined and discrete tasks and communicate with other modules through simple,
universally accessible APIs.

**Docker and microservices**

Container technologies are a kind of enabler of a microservice architecture since containers are designed to be pared down
to the minimal viable pieces needed to run whatever the one thing the container is designed to do, rather than packing
multiple functions into the same machine.

**Getting started with microservices architecture: best practices**

The separation of concerns between services is defined as “service boundaries”.
Service boundaries are closely tied to business demands and organizational hierarchy boundaries.
Some example service boundaries might be “payment processing” and “user authentication” services.

Step 1: Start with a monolith

Microservices do add exponential overhead and complexity to manage. For this reason it is much less overhead for new projects
to keep all the code and logic within a single codebase as it's makes it easier to move the boundaries of the different
modules of your application. Microservices work well when you have a good grasp of the roles of the different services
required by your system. They're much more difficult to handle if the core requirements of an application are still being
worked out. It's indeed quite costly to redefine service interactions, APIs and data structures in microservices
A word of caution though as building a monolith can quickly lead to complicated code that will be hard to break down in smaller
pieces. Try as much as you can to have clear modules identified so that you can extract them later out of the monolith.
You can also start by separating the logic from your web UI and make sure that it interacts with your backend via a
RESTful API over HTTP.

Step 2: Split the monolith

When you've identified the boundaries of your services and when you've reorganized teams, this can be commenced.
Keep communication between services simple with a RESTful API. See following section on inter-process communication.





Inter-process communication
----------------------------
Two ways to communicate between the microservices:

- Synchronous - that is, each service calls directly the other microservice , which results in dependency between the services
- Asynchronous - you have some central hub (or message queue) where you place all requests between the microservices and the
corresponding service takes the request, process it and return the result to the caller. This is what RabbitMQ (or e.g.
Apache Kafka) is used for. In this case all microservices know only about the existance of the hub.

Services must sometimes collaborate to handle those requests via an inter-process communication protocol. For this,
REST should be used for synchronous communications and a messaging technology such as RabbitMQ or Solace used for asynchronous.
Use REST when the key requirement is speed (and data loss isn't critical) and messaging when the key requirement is
reliability. If the receiving system is down, a message will sit on a queue until the system comes back up to process it.
If it's a REST endpoint and it's down, requests will simply fail.

A message queue provide an asynchronous communications protocol - You have the option to send a message from one service to
another without having to know if another service is able to handle it immediately or not. Messages can wait until the
responsible service is ready. A service publishing a message does not need know anything about the inner workings of the
services that will process that message. This way of handling messages decouple the producer from the consumer.
A message queue will keep the processes in your application separated and independent of each other; this way of handling
messages could create a system that is easy to maintain and easy to scale.