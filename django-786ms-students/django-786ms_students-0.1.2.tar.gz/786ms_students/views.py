from django.shortcuts import render
from .forms import *
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from .models import *

def std_login(request):
	if request.user.is_authenticated() and Group.objects.get(name="student") in request.user.groups.all():
		return HttpResponseRedirect("details/")
	else:
		data={}
		msg=''
		form=LoginForm()
		if request.method=='POST':
			print 'POST'
			form=LoginForm(request.POST)
			if form.is_valid():
				username=request.POST['username']
				password=request.POST['password']
				user=authenticate(username=username, password=password)
				if user is not None:
					if Group.objects.get(name="student") in user.groups.all():
						login(request, user)
						return HttpResponseRedirect("details/")
					else:
						msg='No such student'
				else:
					msg='Incorrect username or password'
		else:
			#GET singin form
			pass
		if form:
			data['form']=form
		if msg:
			data['msg']=msg
		return render(request,'786ms_students/student_login_form.html',data)
		
	
def std_details(request):
	if request.user.is_authenticated() and Group.objects.get(name="student") in request.user.groups.all():
		data={}
		group=Group.objects.get(name="student")
		data['group']=group
		student=Student.objects.get(user=request.user)
		data['student']=student
		if request.method=='POST':
			update_form=StudentUpdateForm(request.POST,request.FILES,instance=student)
			if update_form.is_valid():
				request.user.email=update_form.cleaned_data['email']
				if update_form.cleaned_data['password1']:
					request.user.set_password(update_form.cleaned_data['password1'])
				request.user.save()
				update_form.save()
				student=Student.objects.get(user=request.user)
				data['student']=student
				update_form=StudentUpdateForm(instance=student,initial={'email':student.user.email,'photo':student.photo})
				data['update_form']=update_form
				data['msg']='Details updated successfully'
			else:	
				data['update_form']=update_form
				data['msg']='Details not valid'
		else:
			update_form=StudentUpdateForm(instance=student,initial={'email':student.user.email,'photo':student.photo})
			data['update_form']=update_form
		return render(request,'786ms_students/student_details.html',data)
	return HttpResponseRedirect("/student")


def signout(request):
	logout(request)
	return HttpResponseRedirect('/student')

def std_register(request):
	if request.method=='POST':
		form=StudentRegisterationForm(request.POST,request.FILES)
		if form.is_valid():
			student=form.save(commit=False)
			#user creating 
			user=User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
			user.last_name=form.cleaned_data['last_name']
			user.first_name=form.cleaned_data['first_name']
			user.save()
			#add to student group
			group=Group.objects.get(name="student")
			group.user_set.add(user)
			#save student
			student.user=user
			student.token=StudentToken.objects.get(token=form.cleaned_data['ttoken'],name=student.user.get_full_name())
			student.save()
			student.save_m2m()
		else:
			print 'invalid form'
		
		#Student creation
	else:#GET
		form=StudentRegisterationForm()
	return render(request,'786ms_students/registration_form.html',{'form':form})

def std_update(request,pk):
	group=Group.objects.get(name="manager")
	msg=''
	if request.user.is_authenticated() and group in request.user.groups.all():
		data={'group':group}
		student=Student.objects.get(pk=pk)
		data['student']=student
		if request.method=="POST":
			form=ManagerStudentUpdateForm(request.POST,request.FILES,instance=student)
			if form.is_valid():
				student=form.save()
				#check password to update
				if 'password1' in form.cleaned_data and form.cleaned_data['password1']:
					student.user.set_password(form.cleaned_data['password1'])
					student.user.save()
				#check for email change
				if student.user.email!=form.cleaned_data['email']:
					student.user.email=form.cleaned_data['email']
					student.user.save()
				#check for first_name
				if student.user.first_name!=form.cleaned_data['first_name']:
					student.user.first_name=form.cleaned_data['first_name']
					student.user.save()
				#check for last_name
				if student.user.last_name!=form.cleaned_data['last_name']:
					student.user.last_name=form.cleaned_data['last_name']
					student.user.save()
				msg="Details updated"
				initial={'ttoken':student.token.token,'username':student.user.username,'first_name':student.user.first_name,'last_name':student.user.last_name,'email':student.user.email}
				form=ManagerStudentUpdateForm(instance=data['student'],initial=initial)
			else:
				msg="Invalid Data!! Please provide valid input"
		else:
			initial={'ttoken':student.token.token,'username':student.user.username,'first_name':student.user.first_name,'last_name':student.user.last_name,'email':student.user.email}
			form=ManagerStudentUpdateForm(instance=data['student'],initial=initial)
		data['form']=form
		if msg:
			data['msg']=msg
		return render(request,'786ms_students/std_update.html',data)
	else:
		return HttpResponseRedirect("/student/manager")

def get_random_token():
	return ''.join([random.choice('0123456789ABCDEF') for x in range(8)])
	
def manager_panel(request):
	group=Group.objects.get(name="manager")
	if request.user.is_authenticated() and group in request.user.groups.all():
		data={'group':group}
		return render(request,'786ms_students/manager_panel.html',data)
	else:
		return HttpResponseRedirect("/student/manager")
		
def std_list(request):
	group=Group.objects.get(name="manager")
	if request.user.is_authenticated() and group in request.user.groups.all():
		data={'group':group}
		data['students']=Student.objects.all()
		return render(request,'786ms_students/std_list.html',data)
	else:
		return HttpResponseRedirect("/student/manager")

def update_password(request):
	group=Group.objects.get(name="manager")
	if request.user.is_authenticated() and group in request.user.groups.all():
		data={'group':group}
		if request.method=='POST':
			form=PasswordUpdateForm(request.POST)
			if form.is_valid():
				request.user.set_password(form.cleaned_data['password1'])
				request.user.save()
				logout(request)
				return HttpResponseRedirect("/student/manager")
		else:
			form=PasswordUpdateForm()
		data['form']=form
		return render(request,'786ms_students/update_password.html',data)
	else:
		return HttpResponseRedirect("/student/manager")
		
def gen_token(request):
	group=Group.objects.get(name="manager")
	if request.user.is_authenticated() and group in request.user.groups.all():
		data={'group':group}
		if request.method=='POST':
			token_form=TokenForm(request.POST)
			if token_form.is_valid():
				name=token_form.cleaned_data['name']
				token=token_form.save(commit=False)
				token.by=request.user
				save=False
				while(not save):
					try:
						token.save()
						save=True
					except:
						token.token=get_random_token()
				data['token']=token
				data['token_form']=TokenForm()
		else:
			data['token_form']=TokenForm()
		return render(request,'786ms_students/gen_token.html',data)
	else:
		return HttpResponseRedirect("/student/manager")
		
def view_std(request,pk):
	data={}
	if request.user.is_authenticated() and Group.objects.get(name="manager") in request.user.groups.all():
		data['student']=Student.objects.get(pk=pk)
		return render(request,'786ms_students/view_std.html',data)
	else:
		return HttpResponseRedirect("/student/manager")

def manager_login(request):
	if request.user.is_authenticated() and Group.objects.get(name="manager") in request.user.groups.all():
		#possibly already login
		return HttpResponseRedirect("manager-panel/")
	else:
		form=LoginForm()
		data={}
		msg=''
		if request.method=='POST':
			username=request.POST['username']
			password=request.POST['password']
			user=authenticate(username=username, password=password)
			if user is not None:
				if Group.objects.get(name="manager") in user.groups.all():
					login(request, user)
					return HttpResponseRedirect("manager-panel/")
				else:
					msg='No such manager'
			else:
				msg='Incorrect Username or Password'
		data['form']=form
		if msg:
			data['msg']=msg
		return render(request,'786ms_students/manager_login_form.html',data)
