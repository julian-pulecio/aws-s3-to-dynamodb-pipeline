import boto3
import os
import re
from moto import mock_s3, mock_dynamodb
from pytest import fixture
from unittest import mock
from src.tests.contents_tests import CORRECT_S3_OBJECT_BODY, MALFORMED_S3_OBJECT_BODY
from src.tests.events_test import SQS_EVENT
from src.tests.events_test import S3_EVENT
from src.handlers.create_handler import populate_dynamodb_table

BUCKET_NAME = 'my_unique_test_bucket_17072023'

@fixture
def dynamodb():
    with mock_dynamodb():
        dynamodb_client = boto3.client('dynamodb')
        yield dynamodb_client

@fixture
def s3():
    with mock_s3():
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=BUCKET_NAME)
        yield s3

@fixture
def correct_s3_object_evirom(s3):
    S3_OBJECT_KEY = 'my_test_csv_file.csv'
    s3.put_object(
        Bucket=BUCKET_NAME,
        Body=CORRECT_S3_OBJECT_BODY, Key=S3_OBJECT_KEY
    )
    update_sqs_event(
        s3_object_key=S3_OBJECT_KEY,
        bucket_name=BUCKET_NAME
    )
    yield s3

@fixture
def incorrect_type_s3_object_evirom(s3):
    S3_OBJECT_KEY = 'my_test_csv_file.xlm'
    s3.put_object(
        Bucket=BUCKET_NAME,
        Body=CORRECT_S3_OBJECT_BODY, Key=S3_OBJECT_KEY
    )
    update_sqs_event(
        s3_object_key=S3_OBJECT_KEY,
        bucket_name=BUCKET_NAME
    )
    yield s3

@fixture
def incorrect_body_s3_object_evirom(s3):
    S3_OBJECT_KEY = 'my_test_csv_file.csv'
    s3.put_object(
        Bucket=BUCKET_NAME,
        Body=MALFORMED_S3_OBJECT_BODY, Key=S3_OBJECT_KEY
    )
    update_sqs_event(
        s3_object_key=S3_OBJECT_KEY,
        bucket_name=BUCKET_NAME
    )
    yield s3

@fixture
def non_existing_bucket_evirom(s3):
    S3_OBJECT_KEY = 'my_test_csv_file.csv'
    update_sqs_event(
        s3_object_key=S3_OBJECT_KEY,
        bucket_name='non_existing_bucket'
    )
    yield s3

@fixture
def non_existing_key_evirom(s3):
    S3_OBJECT_KEY = 'non_existing_key'
    update_sqs_event(
        s3_object_key=S3_OBJECT_KEY,
        bucket_name=BUCKET_NAME
    )
    yield s3

def update_sqs_event(s3_object_key:str, bucket_name:str):
    s3_event = re.sub('BUCKET_NAME', bucket_name, S3_EVENT)
    s3_event = re.sub('S3_OBJECT_KEY', s3_object_key, s3_event)
    SQS_EVENT['Records'][0]['body'] = s3_event
    return SQS_EVENT

def test_success_response_on_csv_file(correct_s3_object_evirom, dynamodb):
    response = populate_dynamodb_table(event=SQS_EVENT, context='')
    assert response['status_code'] == 200

def test_error_response_on_non_csv_files(incorrect_type_s3_object_evirom, dynamodb):
    response = populate_dynamodb_table(event=SQS_EVENT, context='')
    assert response['status_code'] == 500

def test_error_response_on_malformed_csv_file(incorrect_body_s3_object_evirom, dynamodb):
    response = populate_dynamodb_table(event=SQS_EVENT, context='')
    assert response['status_code'] == 500

def test_error_response_on_non_existing_bucket(non_existing_key_evirom, dynamodb):
    response = populate_dynamodb_table(event=SQS_EVENT, context='')
    assert response['status_code'] == 500
