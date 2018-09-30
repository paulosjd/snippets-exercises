Task queues are used as a strategy to distribute the workload between threads/machines. Celery requires an external solution to send and receive messages. Those solutions are called message brokers. Currently, Celery supports RabbitMQ, Redis, and Amazon SQS as message broker solutions.

Used in web applications where the request-response cycle cannot be made fast, for specific tasks that are time-consuming e.g. a report page, export of big amount of data, video/image processing, where we would leave the user waiting for way too long.
An asynchronous task queue allows tasks to be run asynchronously irrespective of current program flow.


**Example: sending emails asynchronously in a Django application**

[Webpage](https://code.tutsplus.com/tutorials/using-celery-with-django-for-background-task-processing--cms-28732) for full tutorial

This is how it works: we send the user data to the application which creates a User model and then creates a connection to Gmail (or another service you selected). Django waits for the response, and only then does it return a response to our browser.
Creating a user is a bit slow. That's because Django sends the verification email inside the request time. Here is where Celery comes in.

    $ django-admin startproject quick_publisher
    $ cd quick_publisher
    $ ./manage.py startapp main

    # quick_publisher/settings.py
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
    CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

    # quick_publisher/celery.py
    import os
    from celery import Celery

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quick_publisher.settings')

    app = Celery('quick_publisher')
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks()

Celery is a task queue. It receives tasks from our Django application, and it will run them in the background.
Celery needs to be paired with other services that act as brokers, which intermediate the sending of messages between the web application and Celery.

We move the sending verification email functionality in another file called tasks.py:

    from django.core.mail import send_mail
    from django.contrib.auth import get_user_model
    from quick_publisher.celery import app

    @app.task
    def send_verification_email(user_id):
        UserModel = get_user_model()
        ...

Note: the name of the file is important, and how we decorated the `send_verification_email` function with `@app.task`, telling Celery this is a task that will be run in the task queue.

Going back to main/models.py, the signal code turns into:

    def user_post_save(sender, instance, signal, *args, **kwargs):
        if not instance.is_verified:
            # Send verification email
            send_verification_email.delay(instance.pk)

Notice how we call the `.delay` method on the task object. This means we're sending the task off to Celery and we don't wait for the result. I

**Periodic Tasks With Celery**

Once every single day we're going to go through all the users and fetch their posts, then send the author an email with a table containing the posts and view counts.
First, add a field to `Post` and update the view:

    view_count = models.IntegerField("View Count", default=0)

    def view_post(request, slug):
        ...
        post.view_count += 1
        post.save()
        ...

Then create the task which sends the email:

    from django.template import Template, Context
    from django.core.mail import send_mail
    from django.contrib.auth import get_user_model
    from quick_publisher.celery import app
    from publisher.models import Post


    REPORT_TEMPLATE = """
    Here's how you did till now:

    {% for post in posts %}
            "{{ post.title }}": viewed {{ post.view_count }} times |

    {% endfor %}
    """


    @app.task
    def send_view_count_report():
        for user in get_user_model().objects.all():
            posts = Post.objects.filter(author=user)
            if not posts:
                continue

            template = Template(REPORT_TEMPLATE)

            send_mail(
                'Your QuickPublisher Activity',
                template.render(context=Context({'posts': posts})),
                'from@quickpublisher.dev',
                [user.email],
                fail_silently=False,
            )

Then restart Celery and test out in the shell, and check in email if worked:

    $ ./manage.py shell
    In [1]: from publisher.tasks import send_view_count_report
    In [2]: send_view_count_report.delay()

Open up quick_publisher/celery.py and register the periodic tasks:

    # quick_publisher/celery.py

    import os
    from celery import Celery
    from celery.schedules import crontab

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quick_publisher.settings')

    app = Celery('quick_publisher')
    app.config_from_object('django.conf:settings')

    # Load task modules from all registered Django app configs.
    app.autodiscover_tasks()

    app.conf.beat_schedule = {
        'send-report-every-single-minute': {
            'task': 'publisher.tasks.send_view_count_report',
            'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
        },
    }

The task will every minute as indicated by the `crontab()` notation.

Open up another console, activate the appropriate environment, and start the Celery Beat service.

    $ celery -A quick_publisher beat
