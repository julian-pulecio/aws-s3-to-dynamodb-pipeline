import re
import time
from dataclasses import dataclass
from returns.result import safe
from botocore.exceptions import ClientError
from src.models.dynamodb import Dynamodb
from src.models.dynamodb_attribute import Dynamodb_attribute
from src.models.dynamodb_item import Dynamodb_item
from src.models.s3_object import S3_object


@dataclass
class Dynamodb_table(Dynamodb):
    name:str = None

    def __post_init__(self):
        super().__init__()

    def _exist(self):
        existing_tables = self.client.list_tables()['TableNames']
        return self.name in existing_tables
    
    @safe(exceptions=(ClientError,))
    def create(self):
        if not self._exist():
            self.client.create_table(
                TableName=self.name,
                AttributeDefinitions = [{
                    'AttributeName': 'Key',
                    'AttributeType': 'S'
                }],
                KeySchema = [{
                    'AttributeName': 'Key',
                    'KeyType': 'HASH'
                }],
                ProvisionedThroughput = {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            self.client.get_waiter('table_exists').wait(
                TableName=self.name
            )
    
    @safe(exceptions=(ClientError,))
    def create_elements(self, s3_object:S3_object):
        for s3_object_item in s3_object.content:
            self.client.put_item(
                TableName=self.name,
                Item=self._create_item_configuration(
                    s3_object_headers=s3_object.headers,
                    s3_object_item=s3_object_item
                )
            )
    
    def _create_item_configuration(self, s3_object_headers:list, s3_object_item:str) -> dict:
        attributes = []
        for attribute in s3_object_item:
            dynamo_attribute = Dynamodb_attribute(
                value=attribute.strip()
            )
            attributes.append(dynamo_attribute)
        
        item = Dynamodb_item(
            key = re.sub(r'\.','', str(time.time())),
            attributes=attributes,
            headers=s3_object_headers
        )
        return item.get_dynamo_repr()

            
