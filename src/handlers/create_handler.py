import json
from returns.result import Success
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from src.utils.find_value_by_key import find_value_by_key
from src.models.s3_bucket import S3_bucket
from src.models.s3_object import S3_object
from src.models.dynamodb_table import Dynamodb_table


def populate_dynamodb_table(event, context):
    result = flow(
        event,
        get_s3_event,
        get_s3_object,
        bind(create_dynamo_db_table)
    )
    print(result)
    if is_successful(result):
        response = {'status_code':200, 'body':result.unwrap()}
    else:
        response = {'status_code':500, 'body':str(result.failure())}
    return response

def get_s3_event(event:dict) -> dict:
    for record in event.get('Records'):
        s3_event = record.get('body')
        return json.loads(s3_event)

def get_s3_object(event:dict) -> dict:
    bucket_name = find_value_by_key(event, 'name')
    key_name = find_value_by_key(event, 'key')
    s3_bucket = S3_bucket(
        name=bucket_name
    )
    s3_object = S3_object(
        key=key_name,
        bucket=s3_bucket
    ) 
    result = flow(
        s3_bucket.exists(),
        bind(lambda _:s3_object.validate()),
        bind(lambda _:s3_object.set_content_from_bucket()),
        bind(lambda _:Success(s3_object)),
    )
    return result

def create_dynamo_db_table(s3_object:S3_object):
    dynamodb_table = Dynamodb_table(
        name=s3_object.key
    )
    result = flow(
        dynamodb_table.create(),
        bind(lambda _:dynamodb_table.create_elements(s3_object))
    )        
    return result
