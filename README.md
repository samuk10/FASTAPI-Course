# FASTAPI-Course

This is a course from freecodecamp!

Python API Development - Comprehensive Course for Beginners
https://www.youtube.com/watch?v=0sOvCWFmrtA

- FASTAPI
- CI/CD
- SQLAlchemy

# Features

- users should be able to like a post
- should only be able to like a post at once (composite primary_key will take care of it!)
- retrieving posts should also fetch the total number of likes

# stuffs

running the app: uvicorn app.main:app --reload

at: 9h:21m
last commit:

heroku --version
heroku login
heroku create fastapi-samuk10

git remote
git push heroku main # deploy para a plataforma

open the url

create file for heroku on root:
Profile
put the command to start app
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
receive port from heroku, but provide a default if not given

https://fastapi-samuk10.herokuapp.com/ deployed to Heroku
