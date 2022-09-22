import datetime as dt
from django.forms import ValidationError


def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError('год произведения не может быть больше текущего')
    return (value)
