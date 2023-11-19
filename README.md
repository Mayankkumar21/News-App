# News-App

### Running the project locally

  

```bash

git  clone  https://github.com/Mayankkumar21/News-App.git

```



 

### Install Python and pip

  

Visit https://www.python.org/downloads/

  

### Create virtual environment

  

```bash

python3  -m  venv  .venv

```

### Activate virtual Environment

  

```bash

source  .venv/bin/activate

```

  

### Installing external libraries

  

```bash

pip3 install flask news-api redis

```

  

### Installing Redis

Get more info on installing redis and redis server here https://redis.io/docs/install/install-redis/

  

### Check if redis is installed correctly(for mac OS)

```bash

brew services restart redis

```

```bash

redis-cli

ping

```

If you get response as pong after ping then its successfully installed!

  

### Set up your News-Api account

Visit https://newsapi.org/ to sign up and get your api-key

Read official doc - https://newsapi.org/docs
1) Enter your api-key in app.py in NewsApiClient

2) Ensure Redis server is running

  

```bash

python3  app.py

```

And you are good to go!