# MoodStock
A web application showing the sentiment of stocks based on twitter posts.

## Quickstart
To setup the project:

1. [Install docker](https://docs.docker.com/install/) 
1. [Install docker-compose](https://docs.docker.com/compose/install/)
1. Open the Docker application
1. Clone the project :
    ```bash
    # usign ssh
    git clone git@github.com:petartonchev/weast.git
    cd weast
    ```
    or
     ```bash
    # usign https
    git clone https://github.com/petartonchev/weast.git
    cd weast
    ```
1. Build the project (this step would take a while). 
    ```bash
    docker-compose -f local.yml build
    ```
    
1. Start the web application
     ```bash
    docker-compose -f local.yml up
    ```
    **Note:** The next time you want to start the web application you should execute this step only.
    
## Executing Commands from Docker:

To execute management commands inside a docker container you can use `docker-compose -f local.yml run --rm`
For example to execute comands inside the `django` service:
 ```bash
docker-compose -f local.yml run --rm django python manage.py migrate
docker-compose -f local.yml run --rm django python manage.py createsuperuser
 ```
 
 ## Testing:
 
 This project uses the [Pytest](https://docs.pytest.org/en/latest/example/simple.html), a framework for easily building simple and scalable tests. 
 To run the tests execute:
 ```bash
 docker-compose -f local.yml run django pytest
 ```
 
 ##### For coverage reports:
 1.  Run the tests with `coverage` enabled 
     ```bash
      docker-compose -f local.yml run django coverage run -m pytest
     ```
 2. Once the tests are complete you can see the reprot running:
      ```bash
      docker-compose -f local.yml run django coverage report
     ```
## Documentation
1. [Cookiecutter project template](https://cookiecutter-django.readthedocs.io/en/latest/index.html)
