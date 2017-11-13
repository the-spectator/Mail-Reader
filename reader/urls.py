from django.conf.urls import url
from reader import views 

urlpatterns = [ 
  # The home view ('/reader/') 
  url(r'^$', views.home, name='home'), 
  # Explicit home ('/reader/home/') 
  url(r'^home/$', views.home, name='home'), 
  # Redirect to get token ('/reader/gettoken/')
  url(r'^gettoken/$', views.gettoken, name='gettoken'),
  # Mail view ('/reader/mail/')
  url(r'^mail/$', views.mail, name='mail'),
  # SendMail view ('/reader/sendmail/')
  url(r'^sendmail/$', views.sendmail, name='sendmail'),
  # Outbox view ('/reader/outbox/')
  url(r'^outbox/$', views.outbox, name='outbox'),
]
