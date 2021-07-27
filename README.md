# my_sample_code

## Pre-requisites
 - python3.8
 - python3.8-venv
 - postgresql

## Installation

Create a new directory to work in, and cd into it:
```
mkdir <folder_name>
cd <folder_name>
```
Clone the project:
```
https://github.com/AleksandrPischulin/my_sample_code.git
```
Create and activate a virtual environment:
```
python3.8 -m venv venv
source venv/bin/activate
```
cd into my_sample_code folder:
```
cd my_sample_code
```
Update pip inside the virtual environment and install project requirements:
```
pip install --upgrade pip
pip install -r requirements.txt
```
## Config
Create a new psql database and user:
```
sudo -u postgres psql
postgres=# create database mydb;
postgres=# create user myuser with encrypted password 'mypass';
postgres=# grant all privileges on database mydb to myuser;
```
in my_sample_code folder create new file secret_settings.py and add the following information to it:
```
SECRET_KEY = 'some_secret_string'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your created db name'
        'USER': 'your created user name',
        'PASSWORD': 'your created user password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

```
Run migrations:
```
python manage.py migrate
```
Run dev-server:
```
python manage.py runserver
```
## How to use this API
Here it is described what the URL is and what data is expected in the request / response.

later this description will be replaced with a swagger

### Get product list

url = http://127.0.0.1:8000/api/v1/product/

request method = GET
```
expected request data = not need

expected response data (example) = 
[{"id":3,
  "name":"test3",
  "vendor_code":"AAA3",
  "about_product":"test_info3",
  "price":"300.00",
  "cost_price":"30.00",
  "quantity":100},
{"id":1,
 "name":"test1",
 "vendor_code":"AAA1",
 "about_product":"test_info1",
 "price":"150.00",
 "cost_price":"50.00",
 "quantity":300},
{"id":2,
 "name":"test2",
 "vendor_code":"AAA2",
 "about_product":
 "test_info2",
 "price":"200.00",
 "cost_price":"20.00",
 "quantity":92}]
```
### Create new product

url = http://127.0.0.1:8000/api/v1/product/

request method = POST
```
expected request data (example) = {"name": "test4",
                                   "vendor_code": "AAA4",
                                   "about_product": "test_info4",
                                   "price": "400.00",
                                   "cost_price": "40.00",
                                   "quantity": 100}
                                   
expected response data (example) = {"id": 4,
                                    "name": "test4",
                                    "vendor_code": "AAA4",
                                    "about_product": "test_info4",
                                    "price": "400.00",
                                    "cost_price": "40.00",
                                    "quantity": 100}
```
### Change product data

url = http://127.0.0.1:8000/api/v1/product/4/ #product_id=4

request method = PUT
```
expected request data (example) = {"name": "test4",
                                   "vendor_code": "AAA4",
                                   "about_product": "test_info4_changed",
                                   "price": "400.00",
                                   "cost_price": "40.00",
                                   "quantity": 100}
                                   
expected response data (example) = {"id": 4,
                                    "name": "test4",
                                    "vendor_code": "AAA4",
                                    "about_product": "test_info4_changed",
                                    "price": "400.00",
                                    "cost_price": "40.00",
                                    "quantity": 100}
```
### Search items in product list on 'name', 'price' or 'cost_price'

url (example) = http://127.0.0.1:8000/api/v1/product/?search=150

request method = GET
```
expected request data = none

expected response data (example) = 
[{"id":1,
 "name":"test1",
 "vendor_code":"AAA1",
 "about_product":"test_info1",
 "price":"150.00",
 "cost_price":"50.00",
 "quantity":300}]
```
### Filter product list on 'name', 'price' or 'cost_price'

url (example) = http://127.0.0.1:8000/api/v1/product/?price=150

request method = GET
```
expected request data = none

expected response data (example) = 
[{"id":1,
 "name":"test1",
 "vendor_code":
 "AAA1",
 "about_product":"test_info1",
 "price":
 "150.00",
 "cost_price":"50.00",
 "quantity":300}]
```
### Order product list on 'name', 'price' or 'cost_price'

url (example) = http://127.0.0.1:8000/api/v1/product/?ordering=price

request method = GET
```
expected request data = none

expected response data (example) = 
[{"id":1,
 "name":"test1",
 "vendor_code":"AAA1",
 "about_product":"test_info1",
 "price":"150.00",
 "cost_price":"50.00",
 "quantity":300},
{"id":2,
 "name":"test2",
 "vendor_code":"AAA2",
 "about_product":"test_info2",
 "price":"200.00",
 "cost_price":"20.00",
 "quantity":92},
{"id":3,
 "name":"test3",
 "vendor_code":"AAA3",
 "about_product":"test_info3",
 "price":"300.00",
 "cost_price":"30.00",
 "quantity":100}]
```
### Change 'quantity', 'price' or 'cost_price' of selected product (all of this or only one):

url = http://127.0.0.1:8000/api/v1/update_product_economic_data/

request method = PUT
```
expected request data (example) = {"id": 1,
                                   "quantity":10000,
                                   "price": 10000,
                                   "cost_price": 1000}
                                   
expected response data (example) = {"id": 1,
                                    "quantity":10000,
                                    "price": 10000,
                                    "cost_price": 1000}
```
### Get products in cart list 

url = http://127.0.0.1:8000/api/v1/cart/

request method = GET
```
expected request data = none

expected response data (example) = {"2": {"quantity": 30,
                                          "price": "200.00"}
                                   }
                                   
*if cart is empty response data = {}
```
### Add products to cart

url = http://127.0.0.1:8000/api/v1/cart/

request method = POST
```
expected request data (example) = {"product_id": 2,
                                   "quantity_to_buy": 30}
                                   
expected response data (example) = {"detail": "Product added to your cart",
                                    "products": {
                                        "2": {
                                            "quantity": 30,
                                            "price": "200.00"
                                            }
                                        }
                                    }
```
### Remove products from cart

url = http://127.0.0.1:8000/api/v1/cart/

request method = DELETE
```
expected request data (example) = {"product_id": 2}

expected response data (example) = {"detail": "Item removed from cart"}
```
### Get order data

url = http://127.0.0.1:8000/api/v1/order/

request method = GET
```
expected request data (example) = {"order_id": 25}

expected response data (example) = {"order": {
                                    "id": 25,
                                    "customer_name": "test_customer",
                                    "email": "test@email.com",
                                    "address": "test_address",
                                    "postal_code": "123456",
                                    "city": "test_city",
                                    "created": "2021-07-26T00:00:24.391791Z",
                                    "updated": "2021-07-26T00:00:24.402960Z",
                                    "returned": false
                                        }
                                    }
                                    
*if order not created will return 404 ('Not found')
```
### Create order

url = http://127.0.0.1:8000/api/v1/order/

request method = POST
```
expected request data (example) = {"customer_name": "test_customer",
                                   "email": "test@email.com",
                                   "address": "test_address",
                                   "postal_code": 123456,
                                   "city": "test_city"}

expected response data (example) = {"detail": "Order created",
                                    "order_data": {
                                        "id": 25,
                                        "customer_name": "test_customer",
                                        "email": "test@email.com",
                                        "address": "test_address",
                                        "postal_code": "123456",
                                        "city": "test_city",
                                        "created": "2021-07-25T21:43:00.594539Z",
                                        "updated": "2021-07-25T21:43:00.602500Z",
                                        "returned": false
                                    },
                                    "selled_products": {
                                        "1": {
                                            "quantity": 30,
                                            "total_price": 4500.0
                                             },
                                        "2": {
                                            "quantity": 30,
                                            "total_price": 6000.0
                                             }
                                    },
                                    "not_selled_products": {}
                                    }
```                    
### Refund order

url = http://127.0.0.1:8000/api/v1/order/

request method = PATCH
```
expected request data (example) = {"order_id": 25}

expected response data (example) = {"detail": "Order has been returned"}
```
### Get report(quantity of refund products, quantity of selled products, proceeds, profit) for every product for a selected period of time

url = http://127.0.0.1:8000/api/v1/report/

request method = GET
```
expected request data (example) = {"date_from": "21.07.2021",
                                   "date_to": "26.07.2021"}
                                   
expected response data (example) = {"products": [
                                       {"product__id": 2,
                                        "refund_products": 33,
                                        "quantity_selled_products": 9,
                                        "proceeds": 1800.0,
                                        "profit": 1620.0
                                        },
                                       {"product__id": 1,
                                        "refund_products": 332,
                                        "quantity_selled_products": 13,
                                        "proceeds": 1950.0,
                                        "profit": 1300.0
                                        }
                                      ]
                                    }
```
