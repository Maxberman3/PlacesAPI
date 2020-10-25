## A simple server application to liason with the open maps API, with a React app UI & caching

The app expects environment variables to be set or there to be a .dotenv file in the root directory with the following keys:

* OPEN_MAP_KEY is set to the value for the api key to use with openmaps.io
* CACHE_TTL_SECONDS is the lifespan of a key in the cache in seconds. Optional parameter with a default value of 5 minutes.

Run `python manage.py createcachetable` to set up the cache before launching the server with `python manage.py runserver`
