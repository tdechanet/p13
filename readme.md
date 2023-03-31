The project is a django website that have for a goal to let users add workout programs and share them with each other.

To install the project, clone the repository, install the requirements file or the Pipfile.
Then, you will need to specify the following environment variables :
-SECRET_KEY
-ALLOWED_HOSTS
-DB_ENGINE
-DB_HOST
-DB_PORT
-DB_USER
-DB_NAME
-WORKOUTSHARE_DB_PASSWORD

It's not mendatory, but I also recommend you to run the command "py manage.py createsuperuser" to create an admin. By doing this, you will have acces to the admin page, where you can monitor the database entries and can add muscle group for the users to chose when creating an exercice.
Then go in the registry Workoutshare and launch the command "py manage.py runserver" then click on the link prompted in the command line.

This project use the frameworks django and bootstrap5.

To run the tests of the projects, we use pytest, so you will need to run the comment "pytest" to verify that all tests are fine (if you want to run the coverage, add the argument "--cov" to the command).
For a linter we use pylint, so to verify that the code follow the PEP8, use the command "pylint .\workoutshare\".

Also, we use continuous integration, so at every code push, we run all the verifications. The used CI is circle.ci and you can find the configuration file inside the follower .circleci.
