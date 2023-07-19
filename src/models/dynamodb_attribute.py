import ast
from dataclasses import dataclass
from src.models.dynamodb import Dynamodb


@dataclass
class Dynamodb_attribute(Dynamodb):
    attribute_type:str = None
    value:any = None

    def __post_init__(self):
        try:
            attribute_type = type(ast.literal_eval(self.value.strip()))
        except ValueError:
            attribute_type = str        

        if attribute_type == str:
            self.attribute_type = 'S'
        if attribute_type == int or self.attribute_type == float:
            self.attribute_type = 'N'
        if attribute_type == bool:
            self.attribute_type = 'BOOL'