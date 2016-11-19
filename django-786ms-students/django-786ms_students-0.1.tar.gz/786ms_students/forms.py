from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

class StudentUpdateForm(ModelForm):
	email=forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}),required=False)
	password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}),required=False)
	
	class Meta:
		model=Student
		exclude = ['ttoken','first_name','last_name','username','gender','date_of_birth','care_of','father_name','mother_name','category','adhar_card_number']
		fields=['courses','email','password1','password2','mobile','occupation','address','city','state','distict','pin_code','highest_educational_qualification','year_of_passing','photo','signature','left_thumb_impression']
		widgets={
			'courses':forms.CheckboxSelectMultiple,
			'mobile':forms.TextInput(attrs={'class':'form-control'}),
			'occupation':forms.Select(attrs={'class':'form-control'}),
			'address':forms.TextInput(attrs={'class':'form-control'}),
			'city':forms.TextInput(attrs={'class':'form-control'}),
			'state':forms.TextInput(attrs={'class':'form-control'}),
			'distict':forms.TextInput(attrs={'class':'form-control'}),
			'pin_code':forms.TextInput(attrs={'class':'form-control'}),
			'highest_educational_qualification':forms.Select(attrs={'class':'form-control'}),
			'year_of_passing':forms.TextInput(attrs={'class':'form-control'}),
		}
	def clean(self):
		errors={}
		#photo
		if 'photo' in self.cleaned_data and not self.cleaned_data['photo']:
			errors['photo']='You must provide a new photo'
		
		#sign
		if 'signature' in self.cleaned_data and not self.cleaned_data['signature']:
			errors['signature']='You must provide a signature image'
		
		#thumb
		if 'left_thumb_impression' in self.cleaned_data and not self.cleaned_data['left_thumb_impression']:
			errors['left_thumb_impression']='You must provide a left thumb impression image'
			
		#password
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1']==self.cleaned_data['password2']:
				pass
			else:
				errors['password2']='Password didn\'t match'
			
		if errors:
			raise forms.ValidationError(errors)
		else:
			return self.cleaned_data

class StudentRegisterationForm(ModelForm):
	first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	email=forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
	ttoken=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label="Token")
	class Meta:
		model=Student
		fields=['ttoken','courses','first_name','last_name','email','username','password1','password2','mobile','gender','date_of_birth','care_of','father_name','mother_name','category','occupation','address','city','state','distict','pin_code','highest_educational_qualification','year_of_passing','adhar_card_number','photo','signature','left_thumb_impression']
		widgets={
			'courses':forms.CheckboxSelectMultiple,
			'care_of':forms.RadioSelect,
			'gender':forms.RadioSelect,
			'mobile':forms.TextInput(attrs={'class':'form-control'}),
			'gender':forms.RadioSelect,
			'date_of_birth':forms.DateInput(attrs={'class':'form-control','placeholder':'YYYY-MM-DD'}),
			'father_name':forms.TextInput(attrs={'class':'form-control'}),
			'mother_name':forms.TextInput(attrs={'class':'form-control'}),
			'category':forms.Select(attrs={'class':'form-control'}),
			'occupation':forms.Select(attrs={'class':'form-control'}),
			'address':forms.TextInput(attrs={'class':'form-control'}),
			'city':forms.TextInput(attrs={'class':'form-control'}),
			'state':forms.TextInput(attrs={'class':'form-control'}),
			'distict':forms.TextInput(attrs={'class':'form-control'}),
			'pin_code':forms.TextInput(attrs={'class':'form-control'}),
			'highest_educational_qualification':forms.Select(attrs={'class':'form-control'}),
			'year_of_passing':forms.TextInput(attrs={'class':'form-control'}),
			'adhar_card_number':forms.TextInput(attrs={'class':'form-control'}),
		}
	def clean(self):
		errors={}		
		#token
		if 'ttoken' in self.cleaned_data and 'first_name' in self.cleaned_data and 'last_name' in self.cleaned_data:
			try:
				token=self.cleaned_data['ttoken']
				name=self.cleaned_data['first_name']+" "+self.cleaned_data['last_name']
				token=StudentToken.objects.get(token=token,name=name)
				#token used
				try:
					student=token.student
					errors['ttoken']='Token already used'
				except Student.DoesNotExist:
					pass
			except StudentToken.DoesNotExist:
				errors['ttoken']='Invalid Token'
				
		#username
		if 'username' in self.cleaned_data:
			try:
				user=User.objects.get(username=self.cleaned_data['username'])
				errors['username']='Username not available! Try another'
			except User.DoesNotExist:
				pass
		
		#password
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1']:
			if self.cleaned_data['password1']==self.cleaned_data['password2']:
				pass
			else:
				errors['password2']='Password didn\'t match'
			
		if errors:
			raise forms.ValidationError(errors)
		else:
			return self.cleaned_data

class ManagerStudentUpdateForm(StudentRegisterationForm):
	def __init__(self, *args, **kwargs):
		super(StudentRegisterationForm,self).__init__(*args, **kwargs)
		self.fields.pop('ttoken')
		self.fields.pop('username')
		not_required=['password1','password2','photo','signature','left_thumb_impression']
		for key in not_required:
			self.fields[key].required = False
			
	def clean(self):
		errors={}
		#password
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1']:
			if self.cleaned_data['password1']==self.cleaned_data['password2']:
				pass
			else:
				errors['password2']='Password didn\'t match'
			
		if errors:
			raise forms.ValidationError(errors)
		else:
			return self.cleaned_data
			
	class Meta:
		model=Student
		exclude=['ttoken','username']
		fields=['courses','first_name','last_name','email','password1','password2','mobile','gender','date_of_birth','care_of','father_name','mother_name','category','occupation','address','city','state','distict','pin_code','highest_educational_qualification','year_of_passing','adhar_card_number','photo','signature','left_thumb_impression']
		widgets={
			'courses':forms.CheckboxSelectMultiple,
			'care_of':forms.RadioSelect,
			'gender':forms.RadioSelect,
			'mobile':forms.TextInput(attrs={'class':'form-control'}),
			'gender':forms.RadioSelect,
			'date_of_birth':forms.DateInput(attrs={'class':'form-control','placeholder':'YYYY-MM-DD'}),
			'father_name':forms.TextInput(attrs={'class':'form-control'}),
			'mother_name':forms.TextInput(attrs={'class':'form-control'}),
			'category':forms.Select(attrs={'class':'form-control'}),
			'occupation':forms.Select(attrs={'class':'form-control'}),
			'address':forms.TextInput(attrs={'class':'form-control'}),
			'city':forms.TextInput(attrs={'class':'form-control'}),
			'state':forms.TextInput(attrs={'class':'form-control'}),
			'distict':forms.TextInput(attrs={'class':'form-control'}),
			'pin_code':forms.TextInput(attrs={'class':'form-control'}),
			'highest_educational_qualification':forms.Select(attrs={'class':'form-control'}),
			'year_of_passing':forms.TextInput(attrs={'class':'form-control'}),
			'adhar_card_number':forms.TextInput(attrs={'class':'form-control'}),
		}

class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
	
class TokenForm(ModelForm):
	class Meta:
		model=StudentToken
		fields=['name']
		exclude=['token','by','datetime']
		widgets={
			'name':forms.TextInput(attrs={'class':'form-control'}),
		}
class StudentSearchForm(forms.Form):
	token=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Token'}))

class PasswordUpdateForm(forms.Form):
	password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
	password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1']==self.cleaned_data['password2']:
			return self.cleaned_data
		else:
			raise forms.ValidationError({'password2':'Password must match'})
