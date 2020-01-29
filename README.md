[![Build Status](https://semaphoreci.com/api/v1/nicolas-teodosio/megawatt_chlg/branches/master/badge.svg)](https://semaphoreci.com/nicolas-teodosio/megawatt_chlg)

### Installation ###
* Clone the `git clone git@github.com project: nicolasteodosio / labsparser.git`
* Project was created with python 3.6, so create a virtualenv with python 3.6
* I recommend using [pyenv] (https://github.com/pyenv/pyenv-installer) and [pyenv-virtualenv] (https://github.com/pyenv/pyenv-virtualenv#installation)
* Activate your virtualenv
* [Install the docker] (https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository)
* [Install docker-compose] (https://docs.docker.com/compose/install/#install-compose)
* If using `pipenv` execute:` pipenv sync`
* If not, at the root of the project run `pip install -r requirements-dev.txt`

### Running the DEV application ###
* There are two ways to run this application for development
* 1:
    * Run `docker-compose up -d`
    * API will be running at: `http://localhost:8000`
* 2:
    * Run the `docker-compose up -d postgres redis rabbitmq monitor`
    * Change the file `env.example` for `.env`
    * If this is your first time, run `python manage.py migrate`, so you will have the application tables
    * Finally run `python manage.py runserver`
    * Application will be running at: `http://localhost:8000`
* For both it is still necessary to start celery
    * `celery -A megawatt beat -l info`
    * `celery -A megawatt worker -l info`

    
### Running the tests ###
* docker-compose must be running
* To run the tests run `python manage.py test --settings=megawatt.settings_test`

### Using PROD / DEV API ###
* The project was made using django and django rest framework
* This application is in production running at: `http://megawatt-chlg.herokuapp.com/`, WHICH IS NOT WORKING CORRECTLY, if you are running the application under development,
change the url to `http://localhost:8000`
* There are 5 endpoints that are answered by the application
* `admin`, can be logged in using the password and user:`admin`
* `plant`, where the list of registered solar plants appears
* `plant/id`, is a CRUD of solar plants, so it accepts GET, POST, DELETE and PUT
* `plant/pull_data`, only accepts post and is responsible for updating or creating a report of some solar plant, the necessary parameters are:
    * "plant": {"type": "string", "example": "test1"},
        "date_end": {"type": "string", "example": "2020-10-10"},
        "date_start": {"type": "string", "example": "2020-09-10"}
* `report`, only accepts get and is responsible for listing the reports of a solar plant on a date of a specific type
    * "plant_id": {"type": "string", "example": "9"},
        "type": {"type": "string", "example": ["Energy", or "Irradiation"]},
        "date": {"type": "string", "example": "2020-10-10"}

### Using COMMAND ###
* It is possible to execute the command to pull data from the monitoring service without being via API, just execute the command, with virtualenv enabled:
* `python manage.py pull_data --name test1 --fromdate 2019-01-01 --todate 2019-01-02`
* The parameters are:
     * `--name`, the name of the solar plant
    * `--fromdate`, the data start date
    * `--todate`, the data end date

### Comments ###
* This application has integration with [SENTRY] (https://sentry.io), so any exception is logged in the tool.
* The application also has a flow of `CI / CD` using [SEMAPHORE] (https://semaphoreci.com/), which can be found at [https://semaphoreci.com/nicolas-teodosio/megawatt_chlg] ( https://semaphoreci.com/nicolas-teodosio/megawatt_chlg).
Then any commit made in the `MASTER` branch triggers` SEMAPHORECI` that runs the tests and runs the `BUILD` step that deploys the new version in` HEROKU`.
* I used a periodic celery task to pull data every day, using celery beat, from what I read for development it works very well, but in production it would be nice to have a supervisor for that. I also considered that when doing this every day the intention is to go through all the plants and get the data from the previous day.
* I will list here some things I would have liked to have done, but I couldn't because of the time:
    * Would use https://github.com/PyCQA/bandit for security check
    * I would not deploy to heroku, but to AWS using https://github.com/Miserlou/Zappa
    * Add the project to SonarQube https://www.sonarqube.org/, to track code smelss, bugs and coverage
    * I would pay more attention to django admin, I believe it is an excellent tool if done well
    * I created the application in HEROKU, but unfortunately it is not working properly, I believe it was necessary to perform a migrate to the database
    * Add django cache using redis for the API