#!/usr/bin/env bash

WORKING_DIRECTORY="~/www/lab09_deploy"

USERNAME="cs1531lab09deploy"
SSH_HOST="ssh-cs1531lab09deploy.alwaysdata.net"

rm -rf ./__pycache__ ./.pytest_cache > /dev/null
scp number_fun.py numbers_http_test.py numbers_test.py server.py requirements.txt "$USERNAME@$SSH_HOST:$WORKING_DIRECTORY"
ssh "$USERNAME@$SSH_HOST" "cd $WORKING_DIRECTORY && pip3 install -r requirements.txt"
