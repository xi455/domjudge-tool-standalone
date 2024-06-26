#!/bin/sh
set -e

echo "Make log dir"
[ -d ./log/archived ] || mkdir -p ./log/archived

echo "Run crontab"
service cron start

streamlit run home.py --server.port=8000 --server.address=0.0.0.0