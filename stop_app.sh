#!/bin/sh

docker stop app db
docker rm app db
docker image rm nt_task_bank_app-app nt_task_bank_app-db
