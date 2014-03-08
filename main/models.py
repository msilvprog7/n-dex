from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Collection(models.Model):
	""" Collection for various cardsets
	"""
	name = models.CharField(max_length=255)
	description = models.TextField()
	datetime = models.DateTimeField(auto_now_add=True)

	user = models.ForeignKey(User)



class CardSet(models.Model):
	""" A specific cardset contained within one of the User's Collections
	"""
	name = models.CharField(max_length=255)
	description = models.TextField()
	datetime = models.DateTimeField(auto_now_add=True)

	user = models.ForeignKey(User)
	collection = models.ForeignKey(Collection)



class Card(models.Model):
	""" A card from a CardSet 
	"""
	front = models.TextField()
	back = models.TextField()
	frontImage = models.BooleanField(default=False)
	position = models.IntegerField(default=0)

	user = models.ForeignKey(User)
	collection = models.ForeignKey(Collection)
	cardSet = models.ForeignKey(CardSet)



