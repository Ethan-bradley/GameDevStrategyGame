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
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
