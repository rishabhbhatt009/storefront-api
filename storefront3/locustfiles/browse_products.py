from locust import HttpUser, task, between
from random import randint

######################################################################################
# Locust for performance testing 
# RUN : locust -f browse_products.py
######################################################################################

class WebsiteUser(HttpUser):
    
    wait_time = between(1,5)
    
    # Viewing Product 
    @task(2)
    def view_product(self):
        print('viewing products')
        collection_id = randint(2,6)
        self.client.get(
            url=f'/store/products/?collection_id={collection_id}',
            name='/store/products'
            )
    
    # Viewing Product Details 
    @task(4) 
    def view_product(self):
        print('viewing product details')
        product_id = randint(1,1000)
        self.client.get(
            url=f'/store/products/{product_id}',
            name='/store/products/:id'
        )
    
    # Add product to cart 
    @task(1) 
    def add_to_cart(self):
        print('adding to cart')
        product_id = randint(1,10)
        self.client.post(
            url=f'/store/carts/{self.cart_id}/items/',
            name='/store/carts/items',
            json={'product_id':product_id, 'quantity':1}
        )
    
    # Simulate slow response 
    @task 
    def slow_call(self):
        self.client.get('/playground/slow_api/')
    
    # lifecycle hook
    def on_start(self):
        response = self.client.post(url='/store/carts/')
        result = response.json()
        self.cart_id = result['id']
        
        