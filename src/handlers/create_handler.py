import json
import os

def populate_dynamodb_table(event, context):
    print(os.environ)
    return {"statusCode": 200, "body": json.dumps('')}
