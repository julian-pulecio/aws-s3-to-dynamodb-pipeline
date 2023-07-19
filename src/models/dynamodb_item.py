from dataclasses import dataclass
from src.models.dynamodb import Dynamodb
from src.models.dynamodb_attribute import Dynamodb_attribute


@dataclass
class Dynamodb_item(Dynamodb):
    key:str = None
    attributes:list[Dynamodb_attribute] = None
    headers:list[str] = None

    def get_dynamo_repr(self):
        dynamo_syntax_item = {
            'Key': { 'S': self.key},
        }
        for header_index, header in enumerate(self.headers):
            attribute = self.attributes[header_index]
            dynamo_syntax_item.update({header.strip():{attribute.attribute_type: attribute.value}})
        return dynamo_syntax_item