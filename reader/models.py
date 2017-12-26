from django.db import models

# Table EmailData
class EmailData(models.Model):
	id = models.CharField(max_length = 255, primary_key = True)
	emailid = models.EmailField(max_length = 255,blank = False)
	rdatetime = models.CharField(max_length = 255)
	subject = models.CharField(max_length = 255)
	content = models.TextField()
