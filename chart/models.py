from django.db import models


# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class Year(models.Model):
    name = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        return str(self.name)


class SuicideCase(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    cases = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.country.name
