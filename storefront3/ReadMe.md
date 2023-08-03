# Storefront 3 

### How to run
1. Run database : `sudo service mysql start`
2. Connect to mysql : `sudo mysql -u root -p`
3. Run django server : `python manage.py runserver`

Additional : 
1. Upload API : 
2. SMTP Server/Container (email) : `docker run --rm -it -p 3000:80 -p 2525:25 rnwood/smtp4dev`
3. Redis Server/Container : `docker run -d -p 6379:6379 redis`
4. 


Docker : 
- list all containers : `docker ps -a`
- start container : `docker start CONTAINER_ID_OR_NAME`
- stop container : `docker stop CONTAINER_ID_OR_NAME`



