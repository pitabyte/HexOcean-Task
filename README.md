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

## Tiers
### 'Basic', 'Premium' and 'Enterprise' tiers are already created. You can add custom tiers in admin interface. </br>
#### To do so specify following parameters: </br>
<b>'name'</b> - tier name </br>
<b>'heights'</b> - add thumbnail heights as space-separated values (eg. 100 500 1000) </br>
<b>'gets-original'</b> - gets a link to the original photo after upload </br>
<b>'expiring-link'</b> - ability to get an expiring link to a binary photo after upload </br>

## Users
#### admin-user:
username: admin <b>/</b> password: admin

#### Following users are already created, each with 'Basic', 'Premium' and 'Enterprise' tier accordingly: <br>
username: adam <b>/</b> password: adam </br>
username: ewa <b>/</b> password: ewa </br>
username: dawid <b>/</b> password: dawid </br>

#### To add custom users in admin interface specify 'username', 'password' and 'tier'.  </br>

## Endpoints

### POST:

#### http://127.0.0.1:8000/upload/ - Returns links to images based on a user's tier. 

#### Send photos via Postman using following key-value pairs in form-data body:

'photos' -> select files to upload </br>
'username' -> username (e.g. adam) </br>
'expires' -> value from 30 to 30000 (used to create a binary photo) </br>


### GET:

#### http://127.0.0.1:8000/all/ - Lists all images of a specified user. In request body:

'username' -> username

#### http://127.0.0.1:8000/binary/{id} - Returns a binary image (if exists)









