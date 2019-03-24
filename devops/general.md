
Containers: Making Infrastructure as Code Easier
------------------------------------------------
While the microservices model has advantages of the monolithic model, by dividing everything out into separate services,
you have to manage the infrastructure for each service instead of just managing the infrastructure around a single
deployable unit. Infrastructure as Code was born as a solution to this challenge.

They are complemenatry in that IaC tools like chef and Puppet actually bring the host machine to the desired state for allow
the machine running containers.  After that, the container engine (e.g. Docker), will take the role of further
deploying our solutions on a fast and reliable.

**What is Infrastructure as Code?**

IaC refers to the practice of scripting the provisioning of hardware and operating system requirements concurrently
with the development of the application itself. Typically, these scripts are managed in a similar manner to the software
code base, including version control and automated testing. When properly implemented, the need for an administrator to
log into a new machine and configure it manually is replaced by scripts which describe the ideal state of the new machine,
and execute the necessary steps in order to configure the machine to realize that state.

**Key Benefits of IaC**

Each new environment can take a significant amount of time to configure. IaC eliminates the most common pain points with system configuration
and offers additional benefits:

- Relatively easy reuse of common scripts.
- Automation of the entire provisioning process, including being able to provision hardware as part of a continuous delivery process.
- Version control, allowing newer configurations to be tested and rolled back as necessary.
- Peer review and hardening of scripts. Rather than manual configuration from documentation or memory, scripts can be reviewed, updated and continually improved.

**Improving IaC with Containers**

Not only does Docker eliminate inconsistencies in app behaviour from different environments,
it also brings IaC into the development process as a core component. To illustrate this, below is a a Dockerfile for web application with a simple UI, specifying the configuration
of the container which will contain the application:

    FROM ubuntu:12.04

    # Install dependencies
    RUN apt-get update -y && apt-get install -y git curl apache2 php5 libapache2-mod-php5 php5-mcrypt php5-mysql

    # Install app
    RUN rm -rf /var/www/*
    ADD src /var/www

    # Configure apache
    RUN a2enmod rewrite
    RUN chown -R www-data:www-data /var/www
    ENV APACHE_RUN_USER www-data
    ENV APACHE_RUN_GROUP www-data
    ENV APACHE_LOG_DIR /var/log/apache2

    EXPOSE 80
    CMD ["/usr/sbin/apache2", "-D", "FOREGROUND"]

This file will be used to create a Docker image, which is essentially a template that will be used to create a container.
When the Docker container is created, the image will be used to build the container, and a self-contained application will
be created. It will be available for use on whatever machine it is instantiated on, from developer workstation to
high-availability cloud cluster.

`FROM ubuntu:12.04` pulls in an Ubuntu Docker image from Docker Hub to use as the base for your new container.
The image is an official image, which means that it is one of a library of images managed by a dedicated team sponsored by
Docker. The beauty of using this image is that when something goes wrong with your underlying technology, there is a good chance
that someone has already developed the fix and implemented it, and all you would need to do is update your Dockerfile to
reference the new version, rebuild your image, and test and deploy your containers again. The remaining lines in the
Dockerfile install various packages on the base image using apt-get. Add the source of your application to the
/var/www directory, configure Apache, and then set the exposed port for the container to port 80. Finally, the
CMD command is run when the container is brought up, and this will initiate the Apache server and open it for http
requests. That’s Infrastructure as Code in its simplest form. That’s all there is to it. At this point, assuming you
have Docker installed and running on your workstation, you could execute the following command from the directory in
which the Dockerfile resides.

    $ docker build -t my_demo_application:v0.1

Docker will build your image for you, naming it my_demo_application and tagging it with v0.1, which is essentially a version
number. With the image created, you could now take that image and create a container from it with the following command.

    $ docker run -d my_demo_application:v0.1

And just like that, you’ll have your application running on your local machine, or on whatever hardware you choose to run it.




Intro Devops
------------
Maybe three general topics:
Infrastructure Automation – create your systems, OS configs, and app deployments as code. configuration management
(puppet, chef, ansible) Continuous Delivery – build, test, deploy your apps in a fast and automated manner. tools in release (jenkins, travis)
Site Reliability Engineering – operate your systems; monitoring and orchestration

