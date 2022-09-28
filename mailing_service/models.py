from django.core.validators import RegexValidator
from django.db import models

import pytz


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Mailing(models.Model):
    launch_datetime = models.DateTimeField()
    finish_datetime = models.DateTimeField()
    text = models.TextField()
    operator_code = models.SmallIntegerField()
    customer_tag = models.CharField(max_length=255)

    def __str__(self):
        return f'Mailing due to {self.launch_datetime}.'


class Customer(models.Model):
    personal_number = models.CharField(max_length=11, unique=True,
                                       validators=[RegexValidator(
                                           regex=r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
                                       )])
    operator_code = models.SmallIntegerField()
    tag = models.CharField(max_length=255)
    timezone = models.CharField(max_length=32, choices=TIMEZONES)

    def __str__(self):
        return f'Customer {self.tag} with phone number: {self.personal_number}.'


class Message(models.Model):
    creating_datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    corresponding_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    corresponding_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

