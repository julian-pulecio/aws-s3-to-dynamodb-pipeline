import json
import os


def populate_dynamodb_table(event, context):
    print(os.environ['AWS_REGION'])
    print(os.environ['S3_BUCKET'])
    return {"statusCode": 200, "body": json.dumps('')}
