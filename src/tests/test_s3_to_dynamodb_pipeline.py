import boto3
import os
import re
from moto import mock_s3
from pytest import fixture
from unittest import mock
from src.tests.contents_tests import TRAVELS, CITITES
from src.tests.events_test import SQS_EVENT
from src.tests.events_test import S3_EVENT
from src.handlers.create_handler import populate_dynamodb_table

BUCKET_NAME = 'my_unique_test_bucket_17072023'
S3_OBJECT_KEY = 'my_test_csv_file.csv'

@fixture
def s3():
    with mock_s3(), mock.patch.dict(os.environ, {"S3_BUCKET": BUCKET_NAME}):
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=BUCKET_NAME)
        s3.put_object(
            Bucket=BUCKET_NAME,
            Body=TRAVELS, Key=S3_OBJECT_KEY
        )
        yield s3

@fixture
def sqs_event():
    s3_event = re.sub('BUCKET_NAME', BUCKET_NAME, S3_EVENT)
    s3_event = re.sub('S3_OBJECT_KEY', S3_OBJECT_KEY, s3_event)
    SQS_EVENT['Records'][0]['body'] = s3_event
    return SQS_EVENT

def test_success_response_on_csv_files(s3, sqs_event):
    populate_dynamodb_table(event=sqs_event, context='')
