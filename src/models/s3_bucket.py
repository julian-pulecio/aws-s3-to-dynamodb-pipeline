import boto3
from dataclasses import dataclass
from src.models.s3 import S3

@dataclass
class S3_Bucket(S3):
    name:str = None
    
    def __post_init__(self):
        super().__init__()