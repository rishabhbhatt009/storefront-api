# Storefront 3 

### How to run
1. Run database : `sudo service mysql start`
2. Connect to mysql : `sudo mysql -u root -p`
3. Run django server : `python manage.py runserver`

Additional Commands : 
- Collect static file assets : `python manage.py collectstatic` 

Additional : 
1. Upload API : 
2. SMTP Server/Container (email) : `docker run --rm -it -p 3000:80 -p 2525:25 rnwood/smtp4dev`
3. Redis Server/Container : `docker run -d -p 6379:6379 redis`
4. Start celery : `settings.py doc`
5. Start locust : `locust -g locustfiles/browse_products.py`


Docker : 
- list all containers : `docker ps -a`
- start container : `docker start CONTAINER_ID_OR_NAME`
- stop container : `docker stop CONTAINER_ID_OR_NAME`
- executing command inside container : `docker exec -it CONTAINER_ID_OR_NAME command`

Redis : 
- opening redis cli : `docker exec -it CONTAINER_ID_OR_NAME redis-cli`
- select database : `select #`
- Note : database have numbers (not names) in redis 
- get keys : `keys *`
- delete key : `del key`
- delete all keys : `flushall`



