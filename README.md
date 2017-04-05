[![Build Status](https://travis-ci.org/axant/contacthub-sdk-python.svg?branch=master)](https://travis-ci.org/axant/contacthub-sdk-python) [![Coverage Status](https://coveralls.io/repos/github/axant/contacthub-sdk-python/badge.svg)](https://coveralls.io/github/axant/contacthub-sdk-python)

# Contacthub Python SDK

## Table of contents
-   [Introduction](#introdcution)
-   [Getting started](#getting_started)
    -   [Installing and importing the SDK](#installing)
	-   [Performing simple operations on customers](#simpleoperations)
-   [Authentication](#authentication)
-   [Operations on Customers](#customers)
    -   [Add a new customer](#addc)
    -   [Get all customers](#getallc)
    -   [Get a single customer](#getc)
    -   [Update a customer](#updatec)
        - [Full update]()
        - [Patch]()
    -   [Query on customers](#query)
    -   [Tag](#tag)
    -   [Education](#education)
    -   [Job](#job)
    -   [Like](#like)
-   [Operations on Events](#events)
    - [Add a new event](#adde)
    - [Get all events](#getalle)
    - [Get a single event](#gete)
-  [Exception Handling](#exceptionhandling)
-   [API Reference](#apireference)

<a name="introduction"/>

## Introduction

This is the official Python SDK for [ContactHub REST API](https://contactlab.github.io/contacthub-json-schemas/apidoc.html).
This SDK easily allows to access your data on ContactHub, making the authentication immediate and simplifying reading/writing operations.

For all information about ContactHub, check [here](http://contactlab.com/en/offer/engagement-marketing-platform/contacthub/)

<a name="getting_started"/>

## Getting started

<a name="installing"/>

### Installing and importing the SDK

The ContactHub SDK can be installed from PyPi:

```
pip install contacthub
```
After installing, for importing the contacthub SDK just:

```
import contacthub
```

<a name="simpleoperations"/>

### Performing simple operations on customers

#### Getting Customer's data

Retrieving entity's data can be easily archived with simple operations.

First of all, you need to authenticate with credentials provided by `ContactHub`:
```
from contacthub import Workspace

workspace = Workspace(workspace_id = 'workspace_id', token = 'token')
```
After that you can get a `Node` object to perform all operations on customers and events:
```
my_node = workspace.get_node(node_id='node_id')
```
With a node, is immediate to get all customers data in a ``list`` of ``Customer`` objects:
```
customers = my_node.customers

for customer in customers:
  print(customer.base.firstName)
```

Getting a single ``Customer``:

```
my_customer = my_node.get_customer(id='id')

print('Welcome back %s', % my_customer.base.firstName)
```
or querying on customers by theirs own properties:

```
fetched_customers = my_node.query(Customer).filter((Customer.base.firstName == 'Bruce') & (Customer.base.secondName == 'Wayne')).all()
```

#### Add a new Customer

Creating and posting a Customer is simple as getting. The method `add_customer` of the node take a dictionary containing the structure of your customer as parameter and returns a new Customer object:
```
customer_struct =   {
                    'base': {'contacts': {'email': 'myemail@email.com'}}, 
                    'extra': 'extra', 
                    'extended': {'my_string':'my new extended property string'}
                    }
my_customer = c.add_customer(**customer_struct)
```
For creating the customer structure, you can also create a new Customer object and convert it to a dictionary for posting:
```
from contacthub.models import Customer

my_customer = Customer(node = my_node)
my_customer.base.contacts.email = 'myemail@email.com'
my_customer.extra = 'extra'
my_customer.extended.my_string = 'my new extended property string'
my_customer = c.add_customer(**my_customer.to_dict())
```
or posting it directly with the `post` method:
```
my_customer.post()
```

#### Relationship between Customers and Events

In this SDK entities are easily connected.
For retrieving all events associated to a ``Customer``, just:

```
my_customer = my_node.get_customer(id='id')
events = my_customer.events
```

Note that relations are immutable objects. You can just consult events associated to a ``Customer``,
but you cannot add new ones or delete.

<a name="authentication"/>

## Authentication

You can create a `Workspace` object that allows the control of the workspace's nodes. It require the workspace id and the access token provided by ContactHub. 

```
my_workspace = Workspace(workspace_id='workspace_id', token='token')
```

If not specified, the SDK will use the default URL for the ConctactHub API - `https://api.contactlab.it/hub/v1` - but you can specify a different base URL for the API:

```
my_workspace = Workspace(workspace_id='workspace_id', token='token', base_url='base_url')
```

Once obtained a workspace, you're able to access the various nodes linked to it with the `get_node` method:
```
my_node = workspace.get_node(node_id='node_id')
```

This method will return a `Node` object, that allows you to perform all operations on customers and events.
A ``Node`` is a key object for getting, posting, putting, patching and deleting data on entities.

### Authenticating via configuration file

You can specify the workspace ID, the access token and the base url (not mandatory. If ommited, the default base URL for ContactHub will be used) 
via INI file:

```
my_workspace = Workspace.from_INI_file('file.INI')
```

The file must follow this template :
```
workspace_id = workspace_id
token = token
base_url = base_url
```

<a name="customers" />

## Operations on customers
After the [authentication](#authentication), you are ready to perform all operations on ContactHub's entities.

### Create and add a new customer
Like every other entities in ContactHub, you can perform an operation via two methods:
1. Via the Node's standard methods
2. Performing the operation directly by your entity's object
 
#### 1. Adding a new customer via the Node standard methods
In this first case, a new customer can be added in ContactHub by the `Node` object. By default, the `add_customer` method takes as parameter a dictionary containing the structure of your new customer and return a new `Customer` object:
```
customer_structure = {
                        'externalId': '01',
                        'extra': 'extra',
                        'base':
                                {
                                'timezone': 'Europe/Rome',
                                'fistName': 'Bruce',
                                'lastName': 'Wayne',
                                'contacts': {
                                            'email': 'email@email.com',
                                            }
                                }
                        }
                        
my_customer = my_node.add_customer(**customer_structure)
```

To specify the structure of your new customer, you can also use the `Customer` class, creating a new `Customer` object and converting it to a dictionary:
```
from contacthub.models import Customer

post_customer = Customer(node = my_node)
post_customer.base.firstName = 'Bruce'
post_customer.base.lastName = 'Wayne'
post_customer.base.contacts.email = 'email@example.com'
post_customer.extra = 'extra'
post_customer.extended.my_string = 'my new extended property string'

new_customer = my_node.add_customer(**post_customer.to_dict())
```

When you declare a new `Customer`, by default its internal structure start with this template:
```
{'base':{
        'contacts': {}
        },
'extended': {},
'tags': {
        'manual':[],
        'auto':[]
        }
}
```
You can directly access every simple attribute (strings, numbers) in a new customer created with the above structure.
It's possibile to re-define your own internal structure for a customer with the `default_attributes` parameter of the `Customer` constructor:
```
c = Customer(node=my_node, default_attributes={'base':{}})
```
In this case, you can directly set the `base` attribute, but you have to define beforehand all other objects in the internal structure.

##### Properties class
An important tool for this SDK it's the `Properties` class. It represent a default generic object and you should use it for simplify the declarations of entity's properties.
In `Properties` object constructor you can declare every field you need for creating new properties. These fields can be strings, integer, datetime object, other `Properties` and lists of above types.

For example:
```
from contacthub.entities import Properties

my_customer.base.contacts = Properties(email = 'bruce.wayne@darkknight.it', fax = 'fax', otherContacts = [Properties(value='123',name='phone', type='MOBILE')])

my_customer.base.address = Properties(city='city', province='province', geo=Properties(lat=40, lon=100))
```

##### Extended properties

By default the extended properties are already defined in the `Customer` structure, so you can populate it with new integers, strings or `Properties` object for storing what you need. Extended properties follow a standardized schema defined in the [ContactHub settings](https://hub.contactlab.it/#/settings/properties).

```
my_customer.extended.my_extended_int = 1
my_customer.extended.my_extended_string = 'string'
my_customer.extended.my_extended_object = Properties(key='value', k='v')
```

#### 2. Posting a customer directly by its object
In the second case, after the creation of the `Customer` you can post it directly with the `post` method:
```
my_customer.post()
```

#### Force update

If the customer already exists in the node, you can force its update with the new structure specified. If the system notice a match between the new customer posted and an existent one in the node, with the flag `force_update` set to True, the customer will be updated with new data. The match criteria between customers is a configurable option in the [ContactHub settings](https://hub.contactlab.it/#/settings/properties).
```
my_customer = my_node.add_customer(**customer_structure, forceUpdate=True)
```
or alternatively:
```
my_customer.post(forceUpdate=True)
```

For adding a new customer, you have to define its structure with all attributes you need.
You must specify all required attribute, according to your ContactHub configuration. You can find the required attributes in your [ContactHub dashboard](https://hub.contactlab.it/#/settings/properties).

**N.B.: You must follow the ContatHub schema selected for your base properties. Check the [ContactHub dashboard](https://hub.contactlab.it/#/settings/properties) for further information.**

### Get all customers
To retrieve a list of customers in a node, just:
```
customers = node.get_customers()
```
This method return a list of `Customer` objects. 
For accessing the email of a customer the customer attributes:
```
print(my_customer.base.contacts.email)
```
or
```
for tag in my_customer.tags.manual:
    print(tag)
```

In this way you can access every attribute of a single `Customer`. 

Note that if you'll try to access for example the `base` attribute of a `Customer`, it will return an `Properties` object, that will contain all the base properties of the `Customer` object.

#### Paging the customers

ContactHub allows you to page the list of your customers. You can specify the maximum number of customers per page 
and the page to get.

For example, if you have 50 customers and you want to divide them in 10 per page, getting only the second page, use
the `size` and the `page` parameters in this way:

```
customers = node.get_all_customers(size=10, page=2)
```

This call will return a list of 10 customers, taken from the 2nd page of the total 5.

#### Getting customers by their externalId

If there are many customers with the same `externalId`, you can get a list of them by:

```
customers = node.get_all_customers(externalId="01")
```

If it's stored only one customer associated with the specified externalId, this call will return a single `Customer` object
insted of a list.

#### Getting specific fields of customers

It's possible to filter the fields present in a `Customer`, specifying them in a list of fields: 

```
customers = node.get_all_customers(fields=[Customer.base.email,Customer.base.dob,Customer.extra ])
```
Every element of the fetched list will only have the given fields.

**None of the previous parameter passed to the `get_all_customers` method is required and you can combine them for getting the list of customers that suits your needs.**

### Get a single customer

You can get a single customer by specifying its `id` or `externalId`, obtaining a new `Customer` object.

By id:
```
my_customer = node.get_customer(id='01')
```

or by the externalId:
```
my_customer = node.get_customer(externalId='02')
```

In this last case, if there are multiple customers assiociated, this method will return a list of `Customers` object, performing the same call of the `get_all_customers(externalId="02")`

<a name="query"/>

### Query 

#### Simple queries
ContactHub allows you to retrieve subsets of customers entry in a node, by querying on `Customer` entity.

For retrieving a list of Customers that satisfy your fetching criteria, just create a new `Query` object: 
``` 
new_query = node.query(Customer)
```

Now you're ready to apply multiple filters on this  `Query`, specifying new criteria as parameter of the `.filter`method of `Query` class:

``` 
new_query = new_query.filter((Customer.base.firstName == 'Bruce') & (Customer.base.lastName == 'Wayne'))
```
Each filter applied subsequently will put your new criteria in the `AND` condition, adding it to the criteria already present in the query:
``` 
new_query = new_query.filter((Customer.base.dob <= datetime(1994, 6, 10))
```
Once obtained a full filtered query, call the `.all()` method for applying the filters and get a `list` of queried customers:
``` 
filtered_customers = new_query.all()
```

#### Avaible operations for creating a criteria
##### Equality operator
``` 
new_query = node.query(Customer).filter(Customer.base.firstName == 'Bruce')
```
##### Not equals
``` 
new_query = node.query(Customer).filter(Customer.base.firstName != 'Bruce')
```
##### Greater than 
``` 
new_query = node.query(Customer).filter(Customer.base.dob > datetime(1994,6,10))
```
##### Greater than equals
``` 
new_query = node.query(Customer).filter(Customer.base.dob >= datetime(1994,6,10))
```
##### Lower than
``` 
new_query = node.query(Customer).filter(Customer.registeredAt < datetime(2010,6,10))
```
##### Lower than equals
``` 
new_query = node.query(Customer).filter(Customer.registeredAt <= datetime(2010,6,10))
```
##### In, Not in
You can verify the presence of a value in a customer `list` attribute, like `Customer.tags.manual`, with the `in_` and `not_in_` methods of the `query` module:
```
from contacthub.models.query import in_

new_query = node.query(Customer).filter(in_('manual_tag', Customer.tags.manual))
```
``` 
from contacthub.models.query import not_in_

new_query = node.query(Customer).filter(not_in_('manual_tag', Customer.tags.manual))
```
##### Between
You can check if a customer date attribute is between two dates. These two dates can be `datetime` objects or normal string following the ISO8601 standard for dates.
``` 
from contacthub.models.query import between_

new_query = node.query(Customer).filter(between_(Customer.base.dob, datetime(1950,1,1), datetime(1994,1,1)))
```
#### Combine criteria
To combine the above criteria and create complex ones, you can use the `&` and  `|` operators:
##### AND
``` 
customers = node.query(Customer).filter((Customer.base.firstName == 'Bruce') & (Customer.base.lastName == 'Wayne')).all()
```

##### OR
``` 
customers = node.query(Customer).filter(((Customer.base.firstName == 'Bruce')) | ((Customer.base.firstName == 'Batman'))).all()
```
#### Combined query
It's possibile to combine simple queries to create a combined query. 
For this purpose, you can use the `&` operator to put two simple queries in the `AND` condition and the `|` operator for putting them in the `OR` condition.

```
q1 = node.query(Customer)
q2 = node.query(Customer)

and_query = q1 & q2

or_query = q1 | q2
```
 
 For apply all filters created in the new combined query, just like the simple queries call the `.all()`
``` 
filtered_customers = and_query.all()
```
### Update a customer
Customers can be updated with new data. The update can be carried on an entire customer or only on a few attributes.
#### Full update - Put
The full update on customer - PUT method - totally replace old customer attributes with new ones.
As all operations on this SDK, you can perform the full update in two ways: by the node method or directly by the `Customer` object.

Note that if you perform the full update operation by the `update_customer` method of the node, you have to pass all attributes previously set on the customer, otherwise an APIError will occur (see [Exception handling](#exceptionhandling)). These attributes can be easily retrieved via the `to_dict` method. 

Set the `full_update` flag to `True` for a full update, eg:
``` 
my_customer = node.get_customer(id='id')
my_customer.base.contacts.email = 'anotheremail@example.com'

updated_customer = node.update_customer(**my_customer.to_dict(), full_update=True)
```
To directly execute a full update on a customer by the `Customer` object:
```
my_customer = node.get_customer(id='customer_id')
my_customer.base.contacts.email = 'anotheremail@example.com'

my_customer.put()
```
There are no difference between these two ways of working.
#### Partial update - Patch
The partial update - PATCH method -  applies partial modifications to a customer. 

Once the customer is modified, you can get the changes occurred on its attributes by the `get_mutation_tracker` method, that returns a new dictionary:
```
my_customer = node.get_customer(id='customer_id')
my_customer.base.contacts.email = 'anotheremail@example.com'

updated_customer = node.update_customer(**my_customer.get_mutation_tracker())
```

You can also pass to the `update_customer` method a dictionary representing the mutations you want to apply on customer attributes and the id of the customer for applying it:
```
mutations = {'base':{'contacts':{'email':'anotheremail@example.com'}}}

updated_customer = node.update_customer(id='customer_id',**mutations)
```
To partially update a customer by the `Customer` object, just:
```
my_customer.base.contacts.email = 'anotheremail@example.com'

my_customer.patch()
```
 
### Delete a customer
Via node method, passing the id of a customer:
```
node.delete_customer(id='customer_id')
```
or passing the dictionary form of the customer:
```
node.delete_customer(**my_customer.to_dict())
```
Via `Customer` object:
```
my_customer.delete()
``` 

### Tag
### Education
### Job
### Like
## Operations on events
### Add a new event
#### Anonymous customer - Using Sessions
### Get all events
### Get a single event
### Relationship between customers and events
## Exception Handling