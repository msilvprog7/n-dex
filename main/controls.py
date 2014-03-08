from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.generic.base import TemplateView, View

# Create your views here.
class Index(TemplateView):
	""" Index of website, main page for login, etc.
	"""
	template_name = "controls/index.html"

	def dispatch(self, request, *args, **kwargs):

		if request.user.is_authenticated():
			return redirect("/home/")

		return super(Index, self).dispatch(request, *args, **kwargs)





class Login(View):
	""" Login to handle POST request
	"""

	def post(self, request, *args, **kwargs):

		if not ('username' in request.POST and 'password' in request.POST):
			messages.error(request, "Username and password must be provided.")
			return redirect("/")

		user = authenticate(username=request.POST["username"], password=request.POST["password"])

		if user is not None:

			if user.is_active:
				login(request, user)
				return redirect("/home/")
			else:
				messages.error(request, "Account disabled.")
				return redirect("/")
		else:

			messages.error(request, "Incorrect username or password")
			return redirect("/")





class Logout(View):
	""" Logout to handle logging out
	"""

	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect("/")




class Register(View):
	""" Register to handle POST request
	"""

	def post(self, request, *args, **kwargs):

		if not ('username' in request.POST and 'password' in request.POST and 'confirm_password' in request.POST and 'email' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST):
			messages.error(request, "Missing field in registration form.")
			return redirect("/")

		if request.POST["password"] != request.POST["confirm_password"]:
			messages.error(request, "Passwords do not match in registration.")
			return redirect("/")

		if len(User.objects.filter(username=request.POST["username"])) > 0:
			messages.error(request, "Username already being used by another user.")
			return redirect("/")

		if len(User.objects.filter(email=request.POST["email"])) > 0:
			messages.error(request, "Email already being used by another user.")
			return redirect("/")

		user = User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["password"])
		user.first_name = request.POST["first_name"]
		user.last_name = request.POST["last_name"]
		user.save()

		user = authenticate(username=request.POST["username"], password=request.POST["password"])
		login(request, user)
		return redirect("/home/")

		

