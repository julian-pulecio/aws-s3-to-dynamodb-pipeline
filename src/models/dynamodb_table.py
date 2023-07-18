import boto3
from dataclasses import dataclass
from returns.result import safe
from botocore.exceptions import ClientError
from src.models.dynamodb import Dynamodb


@dataclass
class Dynamodb_table(Dynamodb):
    name:str = None

    def __post_init__(self):
        super().__init__()
    
    @safe(exceptions=(ClientError,))
    def create_table(self):
        self.client.create_table(
            TableName=self.name,
            AttributeDefinitions = [{
                'AttributeName': 'id',
                'AttributeType': 'N'  # Numeric attribute
            }],
            KeySchema = [{
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }],
            ProvisionedThroughput = {
                'ReadCapacityUnits': 5,   # Adjust according to your needs
                'WriteCapacityUnits': 5   # Adjust according to your needs
            }
        )
        self.get_waiter('table_exists').wait(
            TableName=self.name
        )