import json
from returns.result import safe
from dataclasses import dataclass
from botocore.exceptions import ClientError
from src.models.s3 import S3
from src.models.s3_bucket import S3_bucket


@dataclass
class S3_object(S3):
    bucket: S3_bucket = None
    key: str = None
    content: list[str] = None
    headers:list[str] = None

    def __post_init__(self):
        super().__init__()

    @safe(exceptions=(ValueError,))
    def validate(self) -> bool:
        if not self.key:
            raise ValueError('key cannot be empty.')
        if self.key[-4:] != '.csv':
            raise ValueError('key must be a .csv file.')
        if not self.bucket:
            raise ValueError('bucket cannot be empty.')
        return True

    @safe(exceptions=(IndexError,ClientError))
    def set_content_from_bucket(self) -> bool:
        response = self.client.get_object(
            Bucket=self.bucket.name,
            Key=self.key
        )
        content = response['Body'].read()
        decoded_content = list(filter(None, content.decode('utf-8').split('\n')))
        self.headers = decoded_content.pop(0).split(',')
        self.content = [item.split(',') for item in decoded_content]
        return True
