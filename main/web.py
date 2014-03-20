from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.contrib import messages

import main.models as models


# Create your views here.
class Home(TemplateView):
	""" Home screen for a logged in user, should view their collections
	"""
	template_name = "main/home.html"

	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)

		context["collections"] = models.Collection.objects.filter(user=self.request.user).order_by("-datetime")

		return context

class AddCollection(View):
	""" Add Collection Post request for users to add collections
	"""

	def post(self, request, *args, **kwargs):

		if not ('name' in request.POST and 'description' in request.POST):
			messages.error(request, "Name and description must be provided.")
			return redirect("/home/")

		if not (request.POST["name"] != "" and request.POST["description"] != ""):
			messages.error(request, "Fields left blank.")
			return redirect("/home/")

		if len(request.POST["name"]) > 255:
			messages.error(request, "Name is too long (limit is 255 characters)")
			return redirect("/home/")


		if len(models.Collection.objects.filter(user=request.user, name=request.POST["name"].replace("%20", " "))) > 0:
			messages.error(request, "Collection with the name specified already exists!")
			return redirect("/home/")


		new_collection = models.Collection(user=request.user, name=request.POST["name"].replace("%20", " "), description=request.POST["description"])
		new_collection.save()

		return redirect("/home/")

class DeleteCollection(View):
	""" Delete Collection Post request for users to remove collections
	"""

	def post(self, request, *args, **kwargs):

		if not ('name' in request.POST):
			return redirect("/home/")

		if not (request.POST["name"] != ""):
			return redirect("/home/")

		if len(request.POST["name"]) > 255:
			return redirect("/home/")

		if len(models.Collection.objects.filter(user=request.user, name=request.POST["name"].replace("%20", " "))) == 0:
			return redirect("/home/")

		for collection in models.Collection.objects.filter(user=request.user, name=request.POST["name"].replace("%20", " ")):
			models.Card.objects.filter(user=request.user, collection=collection).delete()
			models.CardSet.objects.filter(user=request.user, collection=collection).delete()
			collection.delete()

		return redirect("/home/")

class CollectionView(TemplateView):
	""" Screen for user to view a specific collection
	"""
	template_name = "main/collection.html"

	def dispatch(self, request, *args, **kwargs):
		if len(models.Collection.objects.filter(user=request.user, id=int(kwargs["collection_id"]))) <= 0:
			return redirect("/home/")

		return super(CollectionView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CollectionView, self).get_context_data(**kwargs)

		context["collection"] = models.Collection.objects.filter(user=self.request.user, id=int(kwargs["collection_id"])).first()
		context["cardsets"] = models.CardSet.objects.filter(user=self.request.user, collection=context["collection"])

		return context

class AddCardSet(View):
	""" Add CardSet Post request for users to add cardsets
	"""

	def post(self, request, *args, **kwargs):

		if not ('collection_name' in request.POST):
			return redirect("/home/")

		if len(models.Collection.objects.filter(user=request.user, name=request.POST["collection_name"].replace("%20", " "))) <= 0:
			return redirect("/home/")

		associatedCollection = models.Collection.objects.filter(user=request.user, name=request.POST["collection_name"].replace("%20", " ")).first()


		if not ('name' in request.POST and 'description' in request.POST):
			messages.error(request, "Name and description must be provided.")
			return redirect("/home/" + str(associatedCollection.id) + "/")

		if not (request.POST["name"] != "" and request.POST["description"] != ""):
			messages.error(request, "Fields left blank.")
			return redirect("/home/" + str(associatedCollection.id) + "/")

		if len(request.POST["name"]) > 255:
			messages.error(request, "Name is too long (limit is 255 characters)")
			return redirect("/home/" + str(associatedCollection.id) + "/")

		if len(models.CardSet.objects.filter(user=request.user, name=request.POST["name"].replace("%20", " "), collection=associatedCollection)) > 0:
			messages.error(request, "Cardset with the name specified already exists!")
			return redirect("/home/" + str(associatedCollection.id) + "/")


		new_cardset = models.CardSet(user=request.user, name=request.POST["name"].replace("%20", " "), description=request.POST["description"], collection=associatedCollection)
		new_cardset.save()

		return redirect("/home/" + str(associatedCollection.id) + "/")

class DeleteCardSet(View):
	""" Delete CardSet Post request for users to remove cardsets
	"""

	def post(self, request, *args, **kwargs):

		if not ('collection_name' in request.POST):
			return redirect("/home/")

		if len(models.Collection.objects.filter(user=request.user, name=request.POST["collection_name"].replace("%20", " "))) <= 0:
			return redirect("/home/")

		associatedCollection = models.Collection.objects.filter(user=request.user, name=request.POST["collection_name"].replace("%20", " ")).first()


		if not ('name' in request.POST):
			return redirect("/home/" + str(associatedCollection.id) + "/")

		if not (request.POST["name"] != ""):
			return redirect("/home/" + str(associatedCollection.id) + "/")

		if len(request.POST["name"]) > 255:
			return redirect("/home/" + str(associatedCollection.id) + "/")

		if len(models.CardSet.objects.filter(user=request.user, name=request.POST["name"].replace("%20", " "), collection=associatedCollection)) == 0:
			return redirect("/home/" + str(associatedCollection.id) + "/")

		for cardset in models.CardSet.objects.filter(user=request.user, name=request.POST["name"].replace("%20", " "), collection=associatedCollection):
			models.Card.objects.filter(user=request.user, collection=associatedCollection, cardSet=cardset).delete()
			cardset.delete()

		return redirect("/home/" + str(associatedCollection.id) + "/")

class CardView(TemplateView):
	""" Screen for user to view a specific cardset
	"""
	template_name = "main/cardset.html"

	def dispatch(self, request, *args, **kwargs):
		if len(models.CardSet.objects.filter(user=request.user, collection_id=int(kwargs["collection_id"]), id=int(kwargs["cardset_id"]))) <= 0:
			return redirect("/home/")

		cardset = models.CardSet.objects.filter(user=request.user, collection_id=int(kwargs["collection_id"]), id=int(kwargs["cardset_id"])).first()
		num_cards = len(models.Card.objects.filter(user=request.user, collection_id=int(kwargs["collection_id"]), cardSet_id=int(kwargs["cardset_id"])))

		if ('current_card' in kwargs) and (int(kwargs["current_card"]) <= 0 or int(kwargs["current_card"]) > num_cards):
			return redirect("/home/" + str(cardset.collection_id) + "/" + str(cardset.id) + "/")

		return super(CardView, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		cardset = models.CardSet.objects.filter(user=request.user, collection_id=int(kwargs["collection_id"]), id=int(kwargs["cardset_id"])).first()
		num_cards = len(models.Card.objects.filter(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id))

		# new card created on top
		if ('new_card' in request.POST and request.POST["new_card"] == "card-on-top"):
			# increment old cards positions
			for card in models.Card.objects.filter(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id):
				card.position += 1
				card.save()

			new_card = models.Card(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id, position=1, front="", back="")
			new_card.save()

			#redirect
			return redirect("/home/" + str(cardset.collection_id) + "/" + str(cardset.id) + "/" + "1#edit")

		elif ('new_card' in request.POST and request.POST["new_card"] == "card-in-position") and ('new_card_position' in request.POST):
			# shift other cards from this position (MUST DO in reverse, else you're editing what you changed)
			for currentPosition in reversed(range(int(request.POST["new_card_position"]), num_cards + 1)):
				currentCard = models.Card.objects.filter(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id, position=currentPosition).first()
				currentCard.position += 1
				currentCard.save()

			# create new card in position
			new_card = models.Card(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id, position=int(request.POST["new_card_position"]), front="", back="")
			new_card.save()

			# redirect to edit
			return redirect("/home/" + str(cardset.collection_id) + "/" + str(cardset.id) + "/" + request.POST["new_card_position"] + "#edit")

		elif ('edit_card' in request.POST and request.POST['edit_card'] == "edit-card") and ('front' in request.POST and 'frontImage' in request.POST and 'back' in request.POST):
			#update card content
			if ('current_card' in kwargs and int(kwargs["current_card"]) > 0 and int(kwargs["current_card"]) <= num_cards):
				edit_card = models.Card.objects.filter(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id, position=int(kwargs["current_card"])).first()
				
				edit_card.front = request.POST["front"]
				edit_card.frontImage = (request.POST["frontImage"] == "true")
				edit_card.back = request.POST["back"]

				edit_card.save()

				#let redirect to current card as specified below

		elif ('delete_card' in request.POST and request.POST['delete_card'] == "delete-card"):
			# delete this card
			delete_card = models.Card.objects.filter(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id, position=int(kwargs["current_card"])).first()
			delete_card.delete()
			
			# re-order other positions after this
			for currentPosition in range(int(kwargs["current_card"]) + 1, num_cards + 1):
				currentCard = models.Card.objects.filter(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id, position=currentPosition).first()
				currentCard.position = currentPosition - 1
				currentCard.save()

			# redirect based on cards left and current position

			num_cards = len(models.Card.objects.filter(user=request.user, collection_id=cardset.collection_id, cardSet_id=cardset.id))

			if (num_cards <= 0):
				return redirect("/home/" + str(cardset.collection_id) + "/" + str(cardset.id) + "/")
			elif (int(kwargs["current_card"]) > num_cards):
				return redirect("/home/" + str(cardset.collection_id) + "/" + str(cardset.id) + "/" + str(int(kwargs["current_card"]) - 1))

			# else redirect to current card



		current_card_str = ""
		if ('current_card' in kwargs):
			current_card_str = kwargs["current_card"]

		return redirect("/home/" + str(cardset.collection_id) + "/" + str(cardset.id) + "/" + current_card_str)

	def get_context_data(self, **kwargs):
		context = super(CardView, self).get_context_data(**kwargs)

		context["collection"] = models.Collection.objects.filter(user=self.request.user, id=int(kwargs["collection_id"])).first()
		context["cardset"] = models.CardSet.objects.filter(user=self.request.user, collection_id=int(kwargs["collection_id"]), id=int(kwargs["cardset_id"])).first()

		context["num_cards"] = len(models.Card.objects.filter(user=self.request.user, collection_id=int(kwargs["collection_id"]), cardSet_id=int(kwargs["cardset_id"])))
		if ('current_card' in kwargs) and (int(kwargs["current_card"]) > 0 and int(kwargs["current_card"]) <= context["num_cards"]):
			context["card"] = models.Card.objects.filter(user=self.request.user, collection_id=int(kwargs["collection_id"]), cardSet_id=int(kwargs["cardset_id"]), position=int(kwargs["current_card"])).first()

		return context