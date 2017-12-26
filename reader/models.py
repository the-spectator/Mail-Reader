from django.db import models

# Table Emaildata
class Emaildata(models.Model):
	eid = models.CharField(max_length = 255, primary_key = True)
	emailid = models.EmailField(max_length = 255,blank = False)
	rdatetime = models.CharField(max_length = 255)
	subject = models.CharField(max_length = 255)
	content = models.TextField()

