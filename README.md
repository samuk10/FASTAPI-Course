# FASTAPI-Course

This is a course from freecodecamp!

Python API Development - Comprehensive Course for Beginners
https://www.youtube.com/watch?v=0sOvCWFmrtA

- FASTAPI
- CI/CD
- SQLAlchemy

# Features

running on Heroku: https://fastapi-samuk10.herokuapp.com/docs#/

- login to get, create, update
- can delete/update only own post
- search by post
- should be only be able to like a post at once
- retrieving posts should also fetch the total number of likes

# TO DO:

- add nginx container to compose
- implement more features in the app!

# stuffs

running the app: uvicorn app.main:app --reload

- create your .env with:

DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USERNAME=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
