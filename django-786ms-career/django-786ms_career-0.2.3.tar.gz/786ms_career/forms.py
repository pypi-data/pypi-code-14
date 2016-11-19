from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class TokenForm(ModelForm):
	class Meta:
		model=Token
		fields=['token']
	def clean(self):
		try:
			t=self.data['token']
			token=Token.objects.get(token=t)
			try:
				user=User.objects.get(token=token)
				print user
				print 'already used'
				raise ValidationError({'token':['Token already used']})
			except User.DoesNotExist:
				print 'all ok'
				return self.cleaned_data
		except Token.DoesNotExist:
			print 'not exist'
			raise ValidationError({'token':['Token does not exist']})
			
		
class DateInput(forms.DateInput):
    input_type = 'date'
    
class UserForm(ModelForm):
	class Meta:
		model=User
		fields=['name','email','dob','mobile_no']
		widgets = {
            'dob': DateInput()
        }

QualificationInlineFormSet=inlineformset_factory(User,Qualification,form=UserForm,extra=1,fields=['name','duration','board','marks'],can_delete=False)
ExperienceInlineFormSet=inlineformset_factory(User,Experience,form=UserForm,extra=1,fields=['exp_title','duration','summary'],can_delete=False)
