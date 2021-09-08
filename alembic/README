Generic single-database configuration.

STEPS TO START THE APPLICAION

1. Install docker and docker-compose in the local system.
2. Run the command sudo docker-compose up to star the application.
3. To check the database connections in the browser just type localhost:5050/.
4. To check the apis click http://127.0.0.1:8000/docs where you will get the swagger documentation you can test over there.


IMPORTANT COMMANDS
1. sudo docker-compose up - to start the server.
2. sudo docker-compose down - to stop the connections.
3. sudo ss -lptn 'sport = :5432' - to check if any connections running on port 5432 of postgres.
4. sudo kill <pid>.
5. sudo docker-compose run web alembic revision --autogenerate  command for alembic migrations.
6. sudo docker-compose run web alembic upgrade head


STEPS TO CREATE SERVER AND DATABASE IN postgres
1. On your browser hit the url localhost:5050/
2. Login with username - pgadmin4@pgadmin.org and password - admin
3. create a server with name db and maintenance db as test_db, and user as postgres and password postgres
