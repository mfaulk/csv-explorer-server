# Start virtualenv and configure local environment variables. 
# Perhaps this functionality should be invoked via virtualenvwrapper's postactivate hook?

# Inspired by https://realpython.com/blog/python/flask-by-example-part-1-project-setup/

source ./env/bin/activate

export APP_SETTINGS="config.DevelopmentConfig" 