# GameDevStrategyGame


## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Ethan-bradley/GameDevStrategyGame.git
$ cd Strategy
```

Then install the dependencies:

```sh
$ pip install -r requirements.txt
```
Once `pip` has finished downloading the dependencies, migrate the database:
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata seed/0008_Country.json
```
Then create a superuser (so you can access admin page). Enter the username and password used for login.

```sh
python manage.py createsuperuser
```
Then run the server locally.

```sh
python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

## Workflow
Open your working branch
Opening a new branch:
```sh
git checkout -b branchname
```
Opening an existing branch:
```sh
git checkout branchname
```

Run to open server locally
```sh
python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

Make changes.
If database changes are made run the migration commands
```sh
python manage.py makemigrations
python manage.py migrate
```

Check on `http://127.0.0.1:8000/` whether changes are what you intended.
Push to your branch on origin
```sh
git push origin branchname
```
Merge changes to master by creating a PR (Pull Request), then merge the pull request after any conflicts are resolved.
Will then automatically push master changes to heroku
