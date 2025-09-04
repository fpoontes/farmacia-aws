import json, os, boto3, uuid, decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["PRODUCTS_TABLE"])

# Helper to convert Decimal from DynamoDB to float
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)

def seed_if_empty():
    # Seed 3 products if table empty
    resp = table.scan(Limit=1)
    if resp.get("Count", 0) == 0:
        items = [
            {"id": "1", "name": "Paracetamol 750mg", "price": 12.9, "stock": 100},
            {"id": "2", "name": "Dipirona 500mg", "price": 9.5,  "stock": 80},
            {"id": "3", "name": "Vitamina C 1g",   "price": 19.9, "stock": 50},
        ]
        with table.batch_writer() as batch:
            for it in items:
                batch.put_item(Item=it)

def handler(event, context):
    seed_if_empty()

    route = event.get("requestContext", {}).get("http", {}).get("path", "/products")
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path_params = event.get("pathParameters") or {}

    if method == "GET" and route.startswith("/products"):
        if "id" in path_params:
            item_id = path_params["id"]
            resp = table.get_item(Key={"id": item_id})
            item = resp.get("Item")
            if not item:
                return {"statusCode": 404, "body": json.dumps({"message": "Not found"})}
            return {"statusCode": 200, "body": json.dumps(item, cls=DecimalEncoder)}

        # List all
        resp = table.scan()
        items = resp.get("Items", [])
        return {"statusCode": 200, "body": json.dumps(items, cls=DecimalEncoder)}

    return {"statusCode": 400, "body": json.dumps({"message": "Bad Request"})}
