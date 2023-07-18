S3_EVENT = """{
    "Records": [{
        "eventVersion": "2.1",
        "eventSource": "aws:s3",
        "awsRegion": "us-east-1",
        "eventTime": "2023-07-17T19:35:52.452Z",
        "eventName": "ObjectCreated:Put",
        "userIdentity": {
                "principalId": "A2728DOV14PPHG"
                },
        "requestParameters": {
            "sourceIPAddress": "181.60.152.2"
        },
        "responseElements": {
            "x-amz-request-id": "BCV61558C5AWR7RQ",
            "x-amz-id-2": "y10Kk5zm39Xjah9pkGRxtRuyh8dhYl+QOIvWmLw9LXCiVh/bIpBLdUkkhQoPjMJFFBFwDgOu/j3trR+H3EKhId1hlIrLGK2u"
        },
        "s3": {
            "s3SchemaVersion": "1.0",
            "configurationId": "b10129a0-f457-4dbd-a173-913442381913",
            "bucket": {
                "name": "BUCKET_NAME",
                "ownerIdentity": {
                        "principalId": "A2728DOV14PPHG"
                },
                "arn": "arn:aws:s3:::BUCKET_NAME"
            },
            "object": {
                "key": "S3_OBJECT_KEY",
                "size": 8402,
                "eTag": "2dd39cb6de5ecc471fa37f1f2aac759f",
                "sequencer": "0064B598185FDA9DCA"
            }
        }
    }]
}"""

SQS_EVENT = {
    "Records": [{
        "messageId": "6eec1160-80e0-4db7-8e86-a0eecdf29232",
        "receiptHandle": "AQEBYnU/aiwYkzUM5eYS9COLfVxaFtQOQhFgGmFLnVSpHOM9/aigQfpQ0/hARdfLlNAUYvw2M9iMTcz1bpdwnKWXVKF94dyNgpCciJ7mRu0twh2k0LMdkShFO9ZSS+u2yixzDUThBpxOmG7AV5Su3n+vgMeD/A1fegfp2SQW65bkA5YJ7X/KD7ji/lrCNfpuILgKaBFrxL8XcLPlYgA5OYKEtn3KhGvwNeHwiZpNyoGPA7QKfE3WTVndwuzG556GRFcE7jPcI2Hx/sCbIkvJ5D0YNWYr4jRXuLPY/kvBpnNnl56cSAryAEquQsxEyvN0N7znAFdCagUxZEERjtpifH52VYndiwPBvdg9zv6RlJDyyglmUKI8GS/cEHNZXl2dpBRG8izugm4MKch2n4pP7/+hpf4Zrw3mDo2dXNcq9/X/2w0=",
        "body": S3_EVENT,
        "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1689622553282",
                "SenderId": "AIDAJHIPRHEMV73VRJEBU",
                "ApproximateFirstReceiveTimestamp": "1689622553287"
        },
        "messageAttributes": {},
        "md5OfBody": "ceaf935cceebacceca3a08b3583d1c86",
        "eventSource": "aws:sqs",
        "eventSourceARN": "arn:aws:sqs:us-east-1:257838013610:s3-to-dynamodb-SQSQueue-julianpulecio",
        "awsRegion": "us-east-1"
    }]
}