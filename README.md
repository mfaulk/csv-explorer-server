Based on the template project at git@github.com:zachwill/flask_heroku.git

Instructions
------------

Download `pip`, `virtualenv`, `foreman`, and the [`heroku`
Ruby gem](http://devcenter.heroku.com/articles/using-the-cli).

    $ sudo easy_install pip
    $ sudo pip install virtualenv
    $ sudo gem install foreman heroku

Setup an isolated environment with `virtualenv`.

    $ virtualenv --no-site-packages env
    $ source env/bin/activate

    $ pip install -r requirements.txt


Run the tests.

    $ python -m unittest discover ./tests -p '*_tests.py'

Now, you can run the application locally.

    $ foreman start

Or simply

    $ python app.py


