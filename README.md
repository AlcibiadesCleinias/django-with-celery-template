# Dockerizing Django with Celery and Postgres, Gunicorn, Nginx
> Kinda forked from https://github.com/testdrivenio/django-on-docker/tree/main

## Difference From Forked Source

> PR diff: https://github.com/AlcibiadesCleinias/django-with-celery-template/pull/1

- Integrated Celery Tasks
  - Proposed Celery task code layout (in [tasks.py](app/upload/tasks.py) with calling only logic method inside only), aka separation b/w logic and views.py]
  - Celery logging setup
    - how logger should be get and used: `logger = get_task_logger('celery.task.hello_django.upload')`
  - test example for tasks: [app/tests/test_tasks.py](app/tests/test_tasks.py)
    - locate tests on the same layer within Django apps and manage.py (or even upper in case of building the Django-app package)
- Integrated Celery Beat
  - Proposed periodic task code layout (in [app/hello_django/celery.py](app/hello_django/celery.py), could be moved to separate module though)
- Monitoring Integration Example (in docker compose the [Flower](https://flower.readthedocs.io/en/latest/) container proposed)
- copy of [.env.dev-sample](.env.dev-sample) to .env and run with 1 command via `docker compose up`
  - open http://localhost:8000/foo-counter to schedule task
  - check that periodic tasks called

## Want to learn how to build this?

Check out the [tutorial](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx).

## Want to use this project?

### Development

Uses the default Django development server.

1. Rename *.env.dev-sample* to *.env.dev*.
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.
