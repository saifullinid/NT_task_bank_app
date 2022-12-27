#!/bin/bash

docker-compose up --build -d
docker exec -it app /bin/bash
cd bank