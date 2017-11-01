# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def register(self, name, last, email, password, confirmation):

        errors = []

        if len(name) < 3:
            errors.append("Name most be 2 characters or longer!")
        if len(last) < 3:
            errors.append("Last name must be 2 characters or longer!")
        if len(Users.userManager.filter(email=email)) > 0:
            errors.append("This email is already taken.")
        if len(password) < 8:
            errors.append("Password most be 8 characters or longer!")
        if not password == confirmation:
            errors.append("Passwords must match.")
        if len(errors) > 0:
            return(False, errors)
        else:
            passwordHashed =bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = Users.userManager.create(name=name, lastName=last, email=email, passwordHashed=passwordHashed)
            return (True, user)
    def login(self, email, password):
        errors = []

        if len(email) < 2:
            errors.append("Email must be 2 characters or longer!")
        if len(password) < 8:
            errors.append("Password must be 8 characters or longer!")

        email = Users.userManager.filter(email=email)

        if len(email) == 0:
            errors.append("Email not found!")

        if len(errors) > 0:
            return (False, errors)

        else:
            if bcrypt.checkpw(password.encode(), email[0].passwordHashed.encode()):
                return (True, email[0])
            else:
                return (False, ["Incorrect Password!"])


class Users(models.Model):
    name = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    passwordHashed = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    userManager = UserManager()

class QuotesManager(models.Manager):
    def quote(self, author, message, creator):
        errors = []
        if len(author) < 3:
            errors.append("Author most be 3 characters or longer!")
        if len(message) < 10:
            errors.append("Message most be 10 characters or longer!")
        if len(errors) > 0:
            return(False, errors)
        else:
            quote = Quotes.quotesManager.create(author=author,message=message, creator_id = creator )
            return(True, quote)
class Quotes(models.Model):
    author = models.CharField(max_length = 255)
    message = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    created_at = models.DateTimeField(auto_now = True)
    creator = models.ForeignKey(Users, related_name = "quoter")

    quotesManager = QuotesManager()

class Favorites(models.Model):
    quote = models.ForeignKey(Users, related_name = "quote")
    post = models.ForeignKey(Quotes, related_name = "post")
