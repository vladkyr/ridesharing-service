# ridesharing-service
Information System project for IMSE course at Uni Wien

## How to run:

1. install Docker, run the Docker Daemon.
2. clone this repo.
3. run command:
```
docker compose up --build
```
4. navigate to:
```
localhost:8001
```
5. To stop the running containers press "CTRL-C" and run:
```
docker compose down
```

## How to work with database:
1. to visit home page, go to:
```
localhost:8000/home
```
2. initialise mysql database:
```
localhost:8000/init-db
```
3. fill mysql database:
```
localhost:8000/fill-db
```
4. get report:
```
localhost:8000/report
```
5. get mongo report:
```
localhost:8000/mongo/report
```
