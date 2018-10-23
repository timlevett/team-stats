FROM python:3-slim

RUN pip3 install jira
RUN pip3 install PyGithub
RUN pip3 install PyMySQL

RUN mkdir /program
COPY . /program
WORKDIR /program
