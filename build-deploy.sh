#!/bin/bash

pip3 install jira
pip3 install PyGithub

mkdir -p reports
chmod u+x jira-report.py

./run-report.py