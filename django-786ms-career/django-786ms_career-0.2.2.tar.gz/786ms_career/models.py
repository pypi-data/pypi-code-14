from django.db import models
from validators import *
import hashlib

class Token(models.Model):
	name=models.CharField(max_length=50)
	dob=models.DateField('Date Of Birth')
	token=models.CharField(max_length=100,unique=True)
	def __str__(self):
		return self.token
	def save(self, *args, **kwargs):
		if not self.token:
			token=hashlib.sha1()
			token.update(self.name)
			token.update(str(self.dob))
			self.token = token.hexdigest()[:8]
		super(Token, self).save(*args, **kwargs)
		
class User(models.Model):
	name=models.CharField(max_length=50)
	email=models.EmailField(default='')
	mobile_no = models.CharField(max_length=15,validators=[phone_regex], blank=True)
	dob=models.DateField('Date Of Birth')
	token=models.ForeignKey(Token,blank=True,null=True)
	def __str__(self):
		return self.name
	def get_token(self):
		return ",".join(str(x) for x in self.token_set.all())
	def get_qualification(self):
		return ",".join(str(x) for x in self.qualification_set.all())
	def get_experience(self):
		return ",".join(str(x) for x in self.experience_set.all())
	get_token.short_description='Tokens'
	get_qualification.short_description='Qualifications'
	get_experience.short_description='Experiences'
	
class Qualification(models.Model):
	name=models.CharField(max_length=100)
	duration=models.IntegerField()
	board=models.CharField(max_length=100)
	marks=models.FloatField()
	user=models.ForeignKey(User)
	def __str__(self):
		return self.name+","+str(self.duration)+","+self.board+","+str(self.marks)
	
class Experience(models.Model):
	exp_title=models.CharField(max_length=100)
	duration=models.IntegerField()
	summary=models.CharField(max_length=200)
	user=models.ForeignKey(User)
	def __str__(self):
		return self.exp_title+","+str(self.duration)+","+self.summary
