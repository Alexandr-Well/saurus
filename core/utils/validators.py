import re
from rest_framework import serializers


class RegexValidator:
    """
        valid data
        regex valid data by mask
    """
    message = 'car number should be like xxxxY where x-digit, y-latin char Uppercase'

    def __init__(self, field_name: str, mask: str, message=None):
        self.message = message or self.message
        self.field_name = field_name
        self.mask = mask

    def __call__(self, attrs):
        data = attrs[self.field_name]
        mask = re.compile(self.mask)
        if not mask.search(str(data)):
            raise serializers.ValidationError(self.message, code=417)


class IntegerNumberValidator:
    """
        valid data
        from weight_min: int
        to weight_max: int
    """
    message = '{this} field must be more 1 and less 1000 (1000 is ok)'

    def __init__(self, field_name: str, weight_min: int, weight_max: int, message=None):
        self.message = message or self.message
        self.field_name = field_name
        self.weight_min = weight_min
        self.weight_max = weight_max

    def __call__(self, attrs):
        data = attrs[self.field_name]
        if not (self.weight_min <= data <= self.weight_max):
            message = self.message.format(this=self.field_name)
            raise serializers.ValidationError(message, code=417)
