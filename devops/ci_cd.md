One of the key parts of the DevOps tool suite is automation.
Companies want to be able to focus on continuous integration and continuous delivery (CI/CD)
of their software. By automating code integration and the build process companies can move towards
faster releases of their software and more reliable processes.

Jenkins is a build automation tool that sits in the CI/CD space. It ties in with your existing source
control tools and provides a simple way to automate the testing and building process for your software.
Jenkins was first released in 2011 following on from the Hudson project and has a very active community
behind it. The idea behind CI/CD is that a developer checks some new code into a code repository.
A push notification is sent to the build engine, in this case Jenkins. Jenkins clones a copy of
the code, builds it and runs all the defined tests. Jenkins will then set off any post-build steps.
These can be notifying another server that there is a new version of the software to deploy,
or it can deal with deployment itself.

This course looks at how to install and manage a Jenkins server. We have a project to build and deploy
and over the course we will look at how to connect Jenkins to git and pick up notifications,
how to define when and how to build the software and how to deploy it to a Tomcat webserver.
We also look at the administration side including how to define projects, how to setup
Jenkins slave machines and how to define where a project should be built.