## Target

Create an Inventory Control Utility web app named ICU version 1.0.0

## Goals

1. Version 1.0.0 will be used in order to learn new technologies, skills and best practices.
2. Version 1.0.0 should be as minimal as possible. The following issues are ignored for now and will be fixed in later versions:
	- stability
	- scalability
	- security
	- standard REST conventions
		- including response best practicies
	- URL consistency
	- database indexes and foreign keys
3. Version 1.0.0 should be limited to HTML, CSS, JavaScript, Node JS, Java with Spring Boot, Python with Flask, MySQL database, GitHub Actions, Makefile, Docker, Docker Compose.
4. Utilise a Front End node js service, Java Service, Python service, MySQL database and a WireMock for technology learning purposes.
5. All API should respond with status code == 200

## Functionality

Inventory Control Utility should be able to create users, monitor and maintain stock, calculate income / expenses / profits / loss.

## Data model

### item

1. item_id - integer
2. name - string
3. optimal_stock - integer
4. price - decimal
5. volume - decimal
6. weight - decimal

### purchase_order

1. purchase_order_id - integer
2. created_dt - date and time
3. delivered_dt - date and time
4. status - string
5. provider - string

### purchase_order_item

1. purchase_order_item_id - integer
2. item_id - integer
3. purchase_order_id - integer
4. price - decimal
5. quantity - integer

### review

1. review_id - integer
2. start_dt - date and time
3. end_dt - date and time
4. status - string

### review_item

1. review_item_id - integer
2. review_id - integer
3. item_id - integer
4. quantity - integer


## Wiremock

Mocks item providers for purchase orders. Like:
POST `<wiremock-host>/provider/<name:string>` with json body:
```json
[
	{
		"item_name": <string>,
		"quantity": <integer>
	},
	...
]
```
	
1. All requests to name == "CMOT" or "Throat" result in response: `{"status":"failed"}`
2. All other requests result in response: `{"status":"success"}`

## Items service
Python service with Flask

### All items

GET `<items-service-host>/item` responds with:
```json
[
	{
		"item_id": <item_id>,
		"name": <name>
	},
	...
]
```

### Item details

GET `<items-service-host>/item/<item_id>` responds with:
```json
{
	"item_id": <item_id>,
	"name": <name>,
	"optimal_stock": <optimal_stock>,
	"price": <price>,
	"volume": <volume>,
	"weight": <weight>
}
```

### New item

POST `<items-service-host>/item` with body:
```json
{
	"item_id": <item_id>,
	"name": <name>,
	"optimal_stock": <optimal_stock>,
	"price": <price>,
	"volume": <volume>,
	"weight": <weight>
}
```
responds with `{"status":"created"}`

### Delete item

DELETE `<items-service-host>/item/<item_id>` responds with `{ "status": "deleted" }`

### All purchases

GET `<items-service-host>/purchase` responds with body:
```json
[
	{
		"purchase_order_id": <purchase_order_id>,
		"created_dt": <created_dt>,
		"delivered_dt": <delivered_dt>,
		"status": <status>,
		"provider": <provider>
	},
	...
]
```
### New purchase

POST `<items-service-host>/purchase` with body:
```json
{
	"purchase_order_id": <purchase_order_id>,
	"created_dt": <created_dt>,
	"delivered_dt": <delivered_dt>,
	"status": <status>,
	"provider": <provider>
}
```
responds with `{"status":"created"}`.

### Add purchase item

POST `<items-service-host>/purchase/<purchase_order_id>/item` with body:
```json
{
	"purchase_order_item_id": <purchase_order_item_id>,
	"item_id": <item_id>,
	"purchase_order_id": <purchase_order_id>,
	"price": <price>,
	"quantity": <quantity>
}
```
responds with `{"status":"added"}`.

### Delete purchase item

DELETE `<items-service-host>/purchase/<purchase_order_id>/item/<purchase_order_item_id>` responds with `{"status":"deleted"}`.

## Reviews service
Java service with Spring Boot

### Get all reviews

GET `<reviews-service-host>/review` responds with body:
```json
[
	{
		"review_id": <review_id>,
		"start_dt": <start_dt>,
		"end_dt": <end_dt>,
		"status": <status>
	},
	...
]
```

### Create review

POST `<reviews-service-host>/review` with body:
```json
{
	"review_id": <review_id>,
	"start_dt": <start_dt>,
	"end_dt": <end_dt>,
	"status": <status>
}
```
responds with `{"status":"created"}`.

### Delete review

DELETE `<reviews-service-host>/review/<review_id>` responds with `{"status":"deleted"}`.

### Get all review items

GET `<reviews-service-host>/review/<review_id>/item` responds with body:
```json
[
	{
		"review_item_id": <review_item_id>,
		"review_id": <review_id>,
		"item_id": <item_id>,
		"quantity": <quantity>
	},
	...
]
```

### Add review item

POST `<reviews-service-host>/review/<review_id>/item/<review_item_id>` with body:
```json
{
	"review_item_id": <review_item_id>,
	"review_id": <review_id>,
	"item_id": <item_id>,
	"quantity": <quantity>
}
```
responds with `{"status":"added"}`.

### Delete review item

DELETE `<reviews-service-host>/review/<review_id>/item/<review_item_id>` responds with `{"status":"deleted"}`.

## Front end

A most simple UI without any logic that wraps APIs described above.