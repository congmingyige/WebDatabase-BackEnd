from django.db import models
from re import match, compile

class User(models.Model):
    '''Table of user data

    The model of user data, designed for the Login/Register test.

    Attributes:
        phone: 11 digit phone number
        email: e-Mail address
        password: the password of the account
    '''

    phone = models.CharField(max_length=11, unique=True, null=True)
    email = models.EmailField(max_length=64, unique=True, null=True)
    password = models.CharField(max_length=64)

    class Meta:
        db_table = 'user_data'
        # bind them together to build the primary key
        unique_together = (("phone", "email"),)

    def __str__(self):
        if self.phone is not None:
            return '<User %r>' % self.phone
        else:
            return '<User %r>' % self.email

    def __repr__(self):
        if self.phone is not None:
            return '<User %r>' % self.phone
        else:
            return '<User %r>' % self.email
