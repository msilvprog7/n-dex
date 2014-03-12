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

		return super(CardView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CardView, self).get_context_data(**kwargs)



		return context