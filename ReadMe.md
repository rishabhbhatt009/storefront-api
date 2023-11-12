# Storefront Web Application using Django 
Created a web application with a RESTful API using Django and Django REST-FRAMEWORK. Iterated though 3 versions (storefront 1,2,3). With each version I improved my design and added functionality. I used the final version to test performance and load. 

## Version Log 
Please find the version log below : 

### Storefront-1 : `./storefornt2`
- Created a skeleton for the web application using Django. 
- Designed the data model and used Django ORM to enable basic CRUD operations required for a storefront.
- packaging and virtual env created using : pipenv
- Debugging : django-debug-toolbar

### Storefront-2 : `./storefornt2`
- Added a web API using DRF = Django REST Framework. The API is based on REST principles
- Implemented serializers for different data models and created views using ViewSets
- Added routers to manage multiple endpoints
- Added users, created user groups and assigned permissions to manage access 
- Used Djoser and JSON Web Tokens (JWT) to add security and authentication 

### Storefront-3 : `./storefornt3`
- Added simple frontend : `storefront3_client`
- Added Functionality : 
  - uploading images and files using django-cors-headers and pillow
  - email service using a SMTP server 
- Improved performance  : 
  - used redis as message broker and for caching, 
  - used celery for task management, and 
  - used flower for monitoring 
- Testing : 
  - Automated Testing using pytest, model-bakery 
  - Implemented continuous testing using pytest-watch
  - Performance Testing :  
    - Used Locust for Load Testing and Silk for profiling
  - Stress Testing : 
    - Performance test where we find the limits of the current system 
- Deployed the app on Heroku

---