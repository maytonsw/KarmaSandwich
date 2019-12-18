FROM python:3.6-alpine

ADD KarmaSandwich.py /
ADD Operations.py /
ADD praw.ini /

RUN pip install praw

CMD praw_client_id=$SECRET_CLIENT_ID praw_client_secret=$SECRET_CLIENT_SECRET praw_username=$SECRET_USERNAME praw_password=$SECRET_PASSWORD python ./KarmaSandwich.py