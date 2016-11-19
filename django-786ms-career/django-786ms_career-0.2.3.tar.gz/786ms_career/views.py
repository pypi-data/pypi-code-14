from django.shortcuts import render
from .models import User
from django.views.generic import CreateView
from .forms import QualificationInlineFormSet,ExperienceInlineFormSet,UserForm,TokenForm
from .models import User,Token,Experience,Qualification
from django.forms.models import inlineformset_factory
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .urls import *

class UserView(CreateView):
	template_name = '786ms_career/trainer_career.html'
	model=User
	form_class = UserForm
	success_url = 'submit/'
	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		
		token_form = TokenForm()
		exp_form = ExperienceInlineFormSet()
		quali_form=QualificationInlineFormSet()
		return self.render_to_response(self.get_context_data(form=form,token_form=token_form,exp_form=exp_form,quali_form=quali_form))
	
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		token_form = TokenForm(self.request.POST)
		exp_form = ExperienceInlineFormSet(self.request.POST)
		quali_form=QualificationInlineFormSet(self.request.POST)
		if(form.is_valid() and token_form.is_valid() and exp_form.is_valid() and quali_form.is_valid()):
			return self.form_valid(form,token_form,exp_form,quali_form)
		else:
			return self.form_invalid(form,token_form,exp_form,quali_form)
	def form_valid(self,form,token_form,exp_form,quali_form):
		
		token=token_form.save(commit=False)
		token=Token.objects.get(token=token.token)
		user=form.save()
		user.token=token
		user.save()
		
		quali_form.instance=user
		quali_form.save()
		
		exp_form.instance=user
		exp_form.save()
		
		return trainer_view(self.request,token)#HttpResponseRedirect(self.get_success_url())
		
	def form_invalid(self,form,token_form,exp_form,quali_form):
		return self.render_to_response(self.get_context_data(form=form,token_form=token_form,exp_form=exp_form,quali_form=quali_form))
	
def index(request):
	return render(request,'786ms_career/index.html',{'active_nav_link':'career',})

def trainer_view(request,token):
	try:
		token=Token.objects.get(token=token)
		user=User.objects.get(token=token)
		return render(request,'786ms_career/trainer_submit_career.html',{
		'active_nav_link':'career',
		'user':user,
		'token':token,
		'quali':user.qualification_set.all(),
		'exp':user.experience_set.all()
		})
	except:
		return error(request)
def error(request):
	return render(request,'404.html')
