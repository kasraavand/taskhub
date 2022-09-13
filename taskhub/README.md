### Test Case Scenarios
* Test to verify registration with invalid password.
* Test to verify registration with already exists username.
* Test to verify registration with valid datas.
* Tested API authentication endpoint validations.
* Tested authenticated user authorization.
* Create a project with API.
* Update a project with API.
* Delete a project with API.
* Create a todo with API.
* Update a todo with API.
* Delete a todo with API.
* Get todo list for a developer.
* Get project list for a manager.

### API Endpoints

#### Users

* **/api/users/** (User registration endpoint)
* **/api/users/login/** (User login endpoint)
* **/api/users/logout/** (User logout endpoint)

#### projects

* **/api/projects/** (Project create and list endpoint)
* **/api/projects/{project-name}/** (Project retrieve, update and destroy endpoint)


#### tasks

* **/api/tasks/** (Task create and list endpoint)
* **/api/tasks/{todo-id}/** (Task retrieve, update and destroy endpoint)

### Install 

    pip install -r requirements.txt

### Usage

    python manage.py test


### Curl example 

`curl -i -H "Authorization: Token 96381abfccbabcc6ff3d6e960b310220283e5181" http://127.0.0.1:8000/api/todos/`

`curl -H "Content-Type: application/json" -X POST -d '{"username":"user02", "role": "manager", "password":"samplepass", "confirm_password": "samplepass"}'  http://127.0.0.1:8000/api/projects/`


### Using docker

- build 

`sudo docker build -t taskhub`

- DB migrations

`docker run taskhub sh -c "python manage.py makemigrations && python manage.py migrate"`

- running the image

`sudo docker run -it taskhub`