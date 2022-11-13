from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator

class BinaryPhoto(Model):
    limited_integer_field = IntegerField(
        default=1,
        validators=[
            MaxValueValidator(30000),
            MinValueValidator(30)
        ]
     )