import json, os, boto3, uuid, decimal

dynamodb = boto3.resource("dynamodb")
orders = dynamodb.Table(os.environ["ORDERS_TABLE"])
products = dynamodb.Table(os.environ["PRODUCTS_TABLE"])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)

def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "POST")
    if method != "POST":
        return {"statusCode": 405, "body": json.dumps({"message": "Method Not Allowed"})}

    try:
        body = json.loads(event.get("body") or "{}")
        product_id = str(body["productId"])
        qty = int(body.get("qty", 1))
        customer = str(body["customer"])

        # Validate product and stock
        prod = products.get_item(Key={"id": product_id}).get("Item")
        if not prod:
            return {"statusCode": 400, "body": json.dumps({"message": "Invalid productId"})}

        stock = int(prod.get("stock", 0))
        if qty <= 0 or qty > stock:
            return {"statusCode": 400, "body": json.dumps({"message": "Insufficient stock"})}

        order_id = str(uuid.uuid4())
        item = {
            "id": order_id,
            "productId": product_id,
            "qty": qty,
            "customer": customer,
            "status": "CREATED"
        }
        orders.put_item(Item=item)

        # (Optional) Decrease stock — simplistic, without conditional check
        products.update_item(
            Key={"id": product_id},
            UpdateExpression="SET stock = stock - :q",
            ExpressionAttributeValues={":q": qty}
        )

        return {"statusCode": 201, "body": json.dumps(item, cls=DecimalEncoder)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
