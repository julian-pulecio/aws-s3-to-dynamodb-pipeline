import boto3
from dataclasses import dataclass

@dataclass
class Dynamodb:
    client: boto3.client = None

    def __init__(self):
        self.client = boto3.client('dynamodb')