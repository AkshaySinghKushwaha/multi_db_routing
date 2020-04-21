# -*- coding: utf-8 -*-

# Import required modules
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from my_site.forms import SignUpForm,ProductForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse,HttpResponseRedirect
from my_site.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse



@login_required
def user_dashboard(request):
	"""
		- It will show list of all the databases assigned to the user.
		- It will show list of products and their databases.
		- It will create product and choice database from the list of assigned databases.

		Arguments :
			request object : contains metadata about the request

		return :
			- On product creation it will redirect to user dashboard  with success message.
	"""
	user = request.user
	if user.is_superuser :
		return redirect('admin_dashboard')
	database_list = []
	user_databases = UserDatabases.objects.filter(user = user).values_list('database_list')
	if user_databases:
		database_list = user_databases[0][0].split(',')			
	if request.method == "POST":
		product_form = ProductForm(database_list = database_list,data = request.POST)
		if product_form.is_valid():
			clean_data_dict = product_form.cleaned_data
			product_name = clean_data_dict['product_name']
			product_slug = clean_data_dict['product_slug']
			product_description = clean_data_dict['product_description']
			product_price = clean_data_dict['product_price']
			database_choice = clean_data_dict['database_choice']			
			product = Product(name = product_name, slug = product_slug, description = product_description, price = product_price, username_association = user.username)			
			product.save(using = database_choice)
			messages.success(request, 'Your product is successfully created in '+str(database_choice))
			return HttpResponseRedirect(reverse('home'))
	else:	
		product_form = ProductForm(database_list = database_list)	
	return render(request, 'home.html', {'database_list' : database_list,'product_form':product_form})


def activate(request, uidb64, token):
	"""
		- It will make user is_active as True.
		- After successfull account activation it will login the user in the session and redirect to home page.
		
		Arguments :
			request object : contains metadata about the request
			uid64 : The user's id encoded in base 64
			token : To check that the password is valid

		return :
			- It will redirect to home page.
	"""
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('home')		
	else:
		return HttpResponse('Activation link is invalid!')


def admin_dashboard(request):
	"""
		- It will show list of users and product details
		- Admin can add user and assign multiple databases 
		- On user creation, user will receive and email for account activation

		Arguments :
			request object : contains metadata about the request
		
		return :
			- It will redirect to confirm email page,ask user to activate account from email link.
	"""
	user_detail_dict = {}
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			cleaned_data_dict = form.cleaned_data					
			username = cleaned_data_dict['username']
			password = cleaned_data_dict['password1']
			first_name = cleaned_data_dict['first_name']
			last_name = cleaned_data_dict['last_name']
			email = cleaned_data_dict['email']
			database_choices_list = cleaned_data_dict['database_choices']
			user = User.objects.create_user(username = username, password = password, first_name = first_name, last_name = last_name, email = email)
			user.save()
			database_choices = ','.join([str(each_database) for each_database in database_choices_list])
			user_databases = UserDatabases(user = user,database_list = database_choices)
			user_databases.save()						
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account.'
			message = render_to_string('acc_active_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),
				'token':account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
						mail_subject, message, to=[to_email]
			)
			email.send()
			return HttpResponse('Please confirm your email address to complete the registration')
	else:
		form = SignUpForm()
		user_list = User.objects.all()
		database_list = ['database1','database2','database3','database4','database5']		
		for each_user in user_list :			
			all_product_list = []
			for each_db in database_list :
				details_dict = {}
				product = Product.objects.using(each_db).filter(username_association = each_user.username).values()
				if product :
					details_dict = {'product': product,'db_name' : each_db}
					print details_dict
					all_product_list.append(details_dict)
			# print all_product_list
			user_detail_dict[each_user] = all_product_list
			
	return render(request, 'user_signup.html', {'form': form,'user_detail_dict':user_detail_dict})


@login_required
def product_details(request):
	"""
		- It will show list of products details with their database name.

		Arguments :
			request object : contains metadata about the request
		
		return :
			- It will redirect product details with their database on product_details.html template.
	"""
	user = request.user
	database_list = ['database1','database2','database3','database4','database5']
	all_product_list = []
	for each_db in database_list :
		details_dict = {}		
		product = Product.objects.using(each_db).filter(username_association = user.username).values()
		if product :
			details_dict = {'product': product,'db_name' : each_db}			
			all_product_list.append(details_dict)			
	return render(request, 'product_details.html', {'all_product_list' : all_product_list})	
