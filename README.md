# HexCode recruitment task

## How to run

After cloning the project open command prompt, navigate to project's root directory (HexCodeTask) and execute:

```bash
# Navigate to 'mysite' directory ("/../HexCodeTask/mysite"):
$ cd mysite

# Install dependencies:
$ pip install -r requirements.txt

# To run an app: (or 'python' if you use an earlier version)
$ python3 manage.py runserver 

```

## Endpoints

### POST:

#### http://127.0.0.1:8000/upload/ - send images via Postman using following key-value pair in form-data body:

'images' -> select files to upload
'username' -> username (e.g. adam)
'expires' -> value from 30 to 30000 (used to create a binary photo)


### GET:

#### http://127.0.0.1:8000/all/ - lists all images of a specified user. In request body:

'username' -> username

#### http://127.0.0.1:8000/binary/{id} - Returns a binary image (if exists)









