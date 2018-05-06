Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema

You should think of migrations as a version control system for your database schema. `makemigrations` is responsible for packaging up your model changes into individual migration files - analogous to commits - and `migrate` is responsible for applying those to your database.

Django will make migrations for any change to your models or fields - even options that don’t affect the database - as the only way it can reconstruct a field correctly is to have all the changes in the history, as may be need in data migrations later on.

**Backend Support**

PostgreSQL is the most capable of all the databases here in terms of schema support; the only caveat is that adding columns with default values will cause a full rewrite of the table, for a time proportional to its size.
For this reason, it’s recommended you always create new columns with `null=True`, as this way they will be added immediately.

MySQL lacks support for transactions around schema alteration operations, meaning that if a migration fails to apply you will have to manually unpick the changes in order to try again (it’s impossible to roll back to an earlier point).
In addition, MySQL will fully rewrite tables for almost every schema operation and generally takes a time proportional to the number of rows in the table to add or remove columns. On slower hardware this can be worse than a minute per million rows - adding a few columns to a table with just a few million rows could lock your site up for over ten minutes.

**Migration files**

Migrations are stored as an on-disk format, referred to here as “migration files”. These files are actually just normal Python files with an agreed-upon object layout, written in a declarative style.

A basic migration file looks like this:

    class Migration(migrations.Migration):

        dependencies = [('migrations', '0001_initial')]

        operations = [
            migrations.DeleteModel('Tribble'),
            migrations.AddField('Author', 'rating', models.IntegerField(default=0)),
        ]

What Django looks for when it loads a migration file (as a Python module) is a subclass of django.db.migrations.Migration called Migration. It then inspects this object for four attributes, only two of which are used most of the time:

    dependencies, a list of migrations this one depends on.
    operations, a list of Operation classes that define what this migration does.

The operations are the key; they are a set of declarative instructions which tell Django what schema changes need to be made. Django scans them and builds an in-memory representation of all of the schema changes to all apps, and uses this to generate the SQL which makes the schema changes.
That in-memory structure is also used to work out what the differences are between your models and the current state of your migrations; Django runs through all the changes, in order, on an in-memory set of models to come up with the state of your models last time you ran makemigrations. It then uses these models to compare against the ones in your models.py files to work out what you have changed.

**Adding migrations to apps**

f your app already has models and database tables, and doesn’t have migrations yet (for example, you created it against a previous Django version), you’ll need to convert it to use migrations; this is a simple process:

    $ python manage.py makemigrations your_app_label

    $ python manage.py migrate --fake-initial

This will make a new initial migration for your app. and Django will detect that you have an initial migration and that the tables it wants to create already exist, and will mark the migration as already applied. (Without the migrate --fake-initial flag, the command would error out because the tables it wants to create already exist.
Note that this assumes your current database tables match your models.

Data Migrations
-----------------
As well as changing the database schema, you can also use migrations to change the data in the database itself, in conjunction with the schema if you want.

Migrations that alter data are usually called “data migrations”; they’re best written as separate migrations, sitting alongside your schema migrations.

Django can’t automatically generate data migrations for you, as it does with schema migrations, but it’s not very hard to write them

    $ python manage.py makemigrations --empty yourappname

Then open up the file which should look similar to this:

    class Migration(migrations.Migration):

    dependencies = [
        ('yourappname', '0001_initial'),
    ]

    operations = [
    ]

Now, all you need to do is create a new function and have `migrations.RunPython` use it.
Let’s write a simple migration that populates our new name field with the combined values of first_name and last_name:

from django.db import migrations

    def combine_names(apps, schema_editor):
        # We can't import the Person model directly as it may be a newer
        # version than this migration expects. We use the historical version.
        Person = apps.get_model('yourappname', 'Person')
        for person in Person.objects.all():
            person.name = '%s %s' % (person.first_name, person.last_name)
            person.save()

    class Migration(migrations.Migration):

        dependencies = [
            ('yourappname', '0001_initial'),
        ]

        operations = [
            migrations.RunPython(combine_names),
        ]

Once that’s done, we can just run python manage.py migrate as normal and the data migration will run in place alongside other migrations.

**Squashing migrations**

You are encouraged to make migrations freely and not worry about how many you have. However, eventually you will want to move back from having several hundred migrations to just a few, and that’s where squashing comes in.

Squashing is the act of reducing an existing set of many migrations down to one (or sometimes a few) migrations which still represent the same changes.

This enables you to squash and not mess up systems currently in production that aren’t fully up-to-date yet. The recommended process is to squash, keeping the old files, commit and release, wait until all systems are upgraded with the new release (or if you’re a third-party project, just ensure your users upgrade releases in order without skipping any), and then remove the old files, commit and do a second release.

The command that backs all this is `squashmigrations` - just pass it the app label and migration name you want to squash up to, and it’ll get to work:

Note that model interdependencies in Django can get very complex, and squashing may result in migrations that do not run; either mis-optimized (in which case you can try again with `--no-optimize`, though you should also report an issue), or with a `CircularDependencyError`, in which case you can manually resolve it.

Once you’ve squashed your migration, you should then commit it alongside the migrations it replaces and distribute this change to all running instances of your application, making sure that they run migrate to store the change in their database.

You must then transition the squashed migration to a normal migration by:

    Deleting all the migration files it replaces.
    Updating all migrations that depend on the deleted migrations to depend on the squashed migration instead.
    Removing the replaces attribute in the Migration class of the squashed migration (this is how Django tells that it is a squashed migration).

Providing initial data for models
---------------------------------
It’s sometimes useful to pre-populate your database with hard-coded data when you’re first setting up an app. You can provide initial data with migrations or fixtures.
A fixture is a collection of data that Django knows how to import into a database. The most straightforward way of creating a fixture if you’ve already got some data is to use the `manage.py dumpdata` command. Or, you can write fixtures by hand; fixtures can be written as JSON, XML or YAML.

As an example, though, here’s what a fixture for a simple Person model might look like in JSON:

    [
      {
        "model": "myapp.person",
        "pk": 1,
        "fields": {
          "first_name": "John",
          "last_name": "Lennon"
        }
      },
      {
        "model": "myapp.person",
        "pk": 2,
        "fields": {
          "first_name": "Paul",
          "last_name": "McCartney"
        }
      }
    ]
 
You’ll store this data in a fixtures directory inside your app.

Loading data is easy: just call `manage.py loaddata <fixturename>`, where `<fixturename>` is the name of the fixture file you’ve created. Each time you run loaddata, the data will be read from the fixture and re-loaded into the database. By default, Django looks in the `fixtures` directory inside each app for fixtures; this can be changing the `FIXTURE_DIRS` setting.

