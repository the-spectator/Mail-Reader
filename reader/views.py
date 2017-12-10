from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import time,json

from reader.authhelper import get_signin_url, get_token_from_code, get_access_token
from reader.outlookservice import get_me,get_my_messages,send_my_messages

# Create your views here.

def home(request):
	redirect_uri = request.build_absolute_uri(reverse('reader:gettoken'))
	sign_in_url = get_signin_url(redirect_uri)
	context = { 'signin_url': sign_in_url }
	return render(request, 'reader/home.html', context)
	#return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):
	auth_code = request.GET['code']
	redirect_uri = request.build_absolute_uri(reverse('reader:gettoken'))
	token = get_token_from_code(auth_code, redirect_uri)
	access_token = token['access_token']
	user = get_me(access_token)
	refresh_token = token['refresh_token']
	expires_in = token['expires_in']
	expiration = int(time.time()) + expires_in -300
	# Save the token in the session
	request.session['access_token'] = access_token
	request.session['user_email'] = user['mail']
	request.session['refresh_token'] = refresh_token
	request.session['token_expires'] = expiration
	return HttpResponseRedirect(reverse('reader:mail')) 

def mail(request):
	access_token = get_access_token(request, request.build_absolute_uri(reverse('reader:gettoken')))
	user_email = request.session['user_email']
	# If there is no token in the session, redirect to home
	if not access_token:
		return HttpResponseRedirect(reverse('reader:home'))
	else:
		messages = get_my_messages(access_token, user_email,'inbox')
		context = { 'messages': messages['value'] }
		return render(request, 'reader/mail.html', context)
		#return HttpResponse(messages)
		
def sendmail(request):
	access_token = get_access_token(request, request.build_absolute_uri(reverse('reader:gettoken')))
	user_email = request.session['user_email']
	# If there is no token in the session, redirect to home
	if not access_token:
		return HttpResponseRedirect(reverse('reader:home'))
	else:
		message = []
		with open('messages.json') as msgfile:
			data = json.load(msgfile)
		for x in data['msgs']:
			message.append(send_my_messages(access_token,user_email,x))
		context = { 'messages': message }
		return render(request, 'reader/sendmail.html', context)
		
def outbox(request):
	access_token = get_access_token(request, request.build_absolute_uri(reverse('reader:gettoken')))
	user_email = request.session['user_email']
	# If there is no token in the session, redirect to home
	if not access_token:
		return HttpResponseRedirect(reverse('reader:home'))
	else:
		messages = get_my_messages(access_token, user_email,'sentitems')
		context = { 'messages': messages['value'] }
		return render(request, 'reader/outbox.html', context)	
		
		
