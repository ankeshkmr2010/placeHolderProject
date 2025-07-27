# **PROJECTS**


### Project 1: HR helper application (For Bonsen AI)
A simple HR helper application that
#### 1. Parses a job description and extracts the required skills.
#### 2. Evaluates resume(s) against the criteria and scores them returning a csv file for the .



### Run information
```
1. clone the repository https://github.com/ankeshkmr2010/ProjectStubs.git branch:ankesh/bonsenAiDemo
2. create a .env file in the root directory. use .env.sample as a reference.
3. run the following comands 
    docker compose up
4. run using poetry command
    poetry install
    poetry run uvicorn app.main:fastapi_app --host 0.0.0.0 --port 8000
5. open the browser and go to http://localhost:8000/docs for the swagger UI.  
```





