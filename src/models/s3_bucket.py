import re
from botocore.exceptions import ClientError
from returns.result import safe
from dataclasses import dataclass
from src.models.s3 import S3


@dataclass
class S3_bucket(S3):
    name:str = None
    
    def __post_init__(self):
        super().__init__()
    
    @safe(exceptions=(ClientError,))
    def exists(self) -> bool:
        self.client.head_bucket(
            Bucket=self.name
        )
        return True

