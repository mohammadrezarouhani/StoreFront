from locust import task,HttpUser,between
from random import randint

class BrowsPeoduct(HttpUser):
    wait_time=between(1,5)

    @task(2)
    def brows_product(self):
        collection_id=randint(1,5)
        res=self.client.get(
            f'/store/products/?collection_id={collection_id}',
            name='/store/products'
        )
        
    @task(4)
    def brows_single_product(self):
        product_id=randint(1,1000)
        self.client.get(
            f'/store/products/{product_id}/',
            name='/store/products/:id'
        )
    
    @task(1)
    def add_to_card(self):
        product_id=randint(1,1000)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name='add://store/carts/',
            json={
                'product_id':product_id,
                'quantity':1
            }
        )

    @task(1)
    def open_hello_page(self):
        self.client.get('/playground/hello/')

    def on_start(self):
        response=self.client.post('/store/carts/',name='create://store/cart')
        result=response.json()
        self.cart_id=result['id']