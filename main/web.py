from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class Home(TemplateView):
	""" Home screen for a logged in user, should view their collections
	"""
	template_name = "main/home.html"

	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)



		return context
