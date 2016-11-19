from django.db import models
import random
from django.contrib.auth.models import User
from datetime import datetime
import os
from django.conf import settings

def get_token():
	return ''.join([random.choice('0123456789ABCDEF') for x in range(8)])

class StudentToken(models.Model):
	name=models.CharField(max_length=100)
	token=models.CharField(default=get_token(),editable=False,unique=True,max_length=8)
	datetime=models.DateTimeField(auto_now=True,editable=False)
	by=models.ForeignKey(User)
	def __str__(self):
		return self.name+', '+str(self.token)+", "+str(self.datetime)

class Course(models.Model):
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Student(models.Model):
	care_of_choices=[('Parents','Parents'),('Gardians','Gardians')]
	gender_choices=[('Male','Male'),('Female','Female'),('others','others')]
	category_choices=[('General','General'),('SC','SC'),('ST','ST'),('Other Backward Classes','Other Backward Classes')]
	occupation_choices=[('Government','Government'),('Government undertaking','Government undertaking'),('self employed','self employed'),('others','others')]
	highest_educational_qualification_choices=[('Others','Others'),('Graduation or higher','Graduation or higher'),('Polytechnic Diploma','Polytechnic Diploma'),('Below 10th','Below 10th'),('10th Pass','10th Pass'),('12th Pass','12th Pass'),('10th + ITI','10th + ITI')]
	#applied_as_choices=[('Direct','Direct'),('Institute','Institute')]

	user=models.OneToOneField(User,related_name='student')
	token=models.OneToOneField(StudentToken,primary_key=True,related_name="student")
	courses=models.ManyToManyField(Course)

	care_of=models.CharField(max_length=100,choices=care_of_choices,default=care_of_choices[0])
	father_name=models.CharField(max_length=100)
	mother_name=models.CharField(max_length=100)
	gender=models.CharField(max_length=100,choices=gender_choices,default=gender_choices[0])
	date_of_birth=models.DateField()
	category=models.CharField(max_length=100,choices=category_choices,default=category_choices[0])
	occupation=models.CharField(max_length=100,choices=occupation_choices)
	mobile=models.CharField(max_length=10)

	address=models.CharField(max_length=500)
	city=models.CharField(max_length=100)
	state=models.CharField(max_length=100)
	distict=models.CharField(max_length=100)
	pin_code=models.IntegerField()
	highest_educational_qualification=models.CharField(choices=highest_educational_qualification_choices,max_length=100)
	year_of_passing=models.IntegerField()
	adhar_card_number=models.CharField(max_length=100)
	photo=models.ImageField(upload_to='photos')
	signature=models.ImageField(upload_to='signatures')
	left_thumb_impression=models.ImageField(upload_to='thumb_impressions')

	def __str__(self):
		return self.user.get_full_name()

	@property
	def get_photo_url(self):
		return '/'.join(self.photo.url.split("/")[-3:])

	@get_photo_url.setter
	def get_photo_url(self, value):
		self.__get_photo_url = value

	def get_img_tag(self):
		return '<img src="%s" width="150">' % self.photo.url
	get_img_tag.short_description = 'Image'
	get_img_tag.allow_tags = True

	def get_name(self):
		return self.user.get_full_name()
	get_name.short_description = 'Name'
	get_name.allow_tags = True

	def get_email(self):
		return self.user.email
	get_email.short_description = 'Email'
	get_email.allow_tags = True

	def get_username(self):
		return self.user.username
	get_username.short_description = 'Username'
	get_username.allow_tags = True
