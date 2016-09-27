# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View
from .client import Client
from .forms import QAQuestionForm, QAAnswerForm
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm, UpdateUserForm


class UserSignupView(View):
    """
    Renders a form to signup users.
    The form includes the necessary validations.
    """
    template_name = 'balystic/user_signup.html'
    client = Client()

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            data['password'] = data.pop('password_1')
            data.pop('password_2')
            response = self.client.signup_user(**data)
            if 'username' in response.keys():
                user = authenticate(email=response['email'],
                                    password=data['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Your account has been created.')
                    url = 'http://' + user.url + '&next=' +\
                        request.build_absolute_uri('/users/~redirect/')
                    return redirect(url)
                else:
                    messages.success(request, 'Account created, please login')
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                if 'error' in response.keys():
                    form.add_error(None, response['error'])
                else:
                    form.add_error(
                        None,
                        'Unable to create account with the provided information')
        return render(request, self.template_name, {'form': form})


class CommunityUserList(View):
    """
    Displays a list of the users retrieved from 7dhub
    """
    template_name = 'balystic/user_list.html'
    client = Client()

    def get(self, request):
        context = {'users': self.client.get_users()}
        return render(request, self.template_name, context)


class CommunityUserDetail(View):
    """
    Displays the details for the given user
    """
    template_name = 'balystic/user_detail.html'
    client = Client()

    def get(self, request, username):
        context = {'user': self.client.get_user_detail(username)['user']}
        return render(request, self.template_name, context)


class CommunityUserUpdate(View):
    """
    View to update user profile
    """
    template_name = 'balystic/user_update.html'
    client = Client()

    def dispatch(self, request, username, *args, **kwargs):
        if request.user.username != username:
            return HttpResponseForbidden()
        return super(CommunityUserUpdate, self).dispatch(
            request, username, *args, **kwargs)

    def get(self, request, username):
        data = self.client.get_user_detail(username)
        form = UpdateUserForm(initial=data['user'])
        return render(request, self.template_name, {'form': form})

    def post(self, request, username):
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            self.client.update_user(username, form.cleaned_data)
            return redirect(reverse(
                'balystic_user_detail',
                kwargs={'username': username}))
        return render(request, self.template_name, {'form': form})


class CommunityBlogListView(View):
    template_name = "balystic/blog_list.html"

    def get(self, request):
        """
        Display the list of all the blogs posts
        in the community (by page)
        """
        page = request.GET.get('page', 1)
        client = Client()
        blog_entries = client.get_blogs(page=page)
        #############################
        if 'blogs' not in blog_entries:
            raise Http404
        next_page = blog_entries.get('next_page', None)
        blog_entries = blog_entries['blogs']
        try:
            previous_page = int(page) - 1
        except ValueError:
            previous_page = 0
        #############################
        for entry in blog_entries:
            entry['tags'] = [tag for tag in entry['tags'].split(',') if tag]
        context = {'blog_entries': blog_entries,
                   'next_page': next_page,
                   'previous_page': previous_page,
                   'balystic_path': settings.BALYSTIC_API_PATH.
                   replace('/api/', '')}
        return render(request, self.template_name, context)


class CommunityBlogDetailView(View):
    template_name = "balystic/blog_detail.html"

    def get(self, request, slug):
        """
        Display detail of the required blog post,
        if it does exists.
        """
        client = Client()
        blog_entry = client.get_blog_detail(slug)
        #########################
        if 'blog' not in blog_entry:
            raise Http404
        blog_entry = blog_entry['blog']
        #########################
        blog_entry['tags'] = [tag for tag in
                              blog_entry['tags'].split(',') if tag]

        context = {'entry': blog_entry}
        return render(request, self.template_name, context)


class DeleteBlogView(View):

    def get(self, request, slug):
        return redirect(
            reverse('balystic_blog_detail',
                    kwargs={'slug': slug}))

    def post(self, request, slug):
        """
        Delete the required post
        """
        client = Client()
        response = client.delete_blog(slug)
        if 'error' in response.keys():
            return HttpResponseForbidden()
        messages.success(
            request, 'Blog deleted')
        return redirect('balystic_blog')


class CommunityQAListView(View):
    template_name = "balystic/qa_list.html"

    def get(self, request):
        """
        Display list of all the questions
        inside community
        """
        page = request.GET.get('page', 1)
        noans_page = request.GET.get('noans_page', 1)
        client = Client()
        questions = client.get_questions(
            page=page, noans_page=noans_page)
        #############################
        if 'questions' not in questions:
            raise Http404
        reward = questions['reward']
        noans = questions['noans']
        total_noans = questions['total_noans']
        active_tab = request.GET.get('tab', 'questions')
        tabs = ['questions', 'noans', 'reward']
        active_tab = 'questions' if active_tab not in tabs else active_tab
        question_pages = questions['question_pages']
        noans_pages = questions['noans_pages']
        questions = questions['questions']
        #############################
        context = {
            'questions': questions,
            'reward': reward,
            'noans': noans,
            'question_pages': question_pages,
            'noans_pages': noans_pages,
            'total_noans': total_noans,
            'active_tab': active_tab}
        return render(request, self.template_name, context)


class CommunityQADetailView(View):
    template_name = "balystic/qa_detail.html"

    def get(self, request, pk):
        """
        Display detail of the required question,
        if it exists
        """
        client = Client()
        form = QAAnswerForm()
        question = client.get_question_detail(pk)
        #########################
        if 'question' not in question:
            raise Http404
        question = question['question']
        #########################
        context = {'question': question, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        """
        creates an answer for a question
        """
        form = QAAnswerForm(request.POST)
        if form.is_valid():
            client = Client()
            data = form.cleaned_data
            data['user_email'] = request.user.email
            client = Client()
            client.create_answer(pk, data)
            return redirect('balystic_qa_detail', pk=pk)
        context = {'form': form}
        return render(request, self.template_name, context)


class CommunityQAEditQuestionView(View):

    template_name = "balystic/qa_create_question.html"

    def get(self, request, pk):
        """
        Display the form for creating a question
        """
        client = Client()
        question = client.get_question_detail(pk)
        #########################
        if 'question' not in question:
            raise Http404
        question = question['question']
        form = QAQuestionForm(
            initial={
                'title': question['title'],
                'description': question['description'],
                'tags': ','.join(question['tags'])
            })
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = QAQuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user_email'] = request.user.email
            client = Client()
            client.edit_question(pk, data)
            return redirect('balystic_qa_detail', pk=pk)
        context = {'form': form}
        return render(request, self.template_name, context)


class CommunityQADeleteQuestionView(View):

    def post(self, request, pk):
        client = Client()
        client.delete_question(pk, request.user.email)
        return redirect('balystic_qa')


class CommunityQAEditAnswerView(LoginRequiredMixin, View):

    def post(self, request, pk):
        form = QAAnswerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user_email'] = request.user.email
            client = Client()
            client.edit_answer(pk, data)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('balystic_qa')


class CommunityQADeleteAnswerView(LoginRequiredMixin, View):

    def post(self, request, pk):
        client = Client()
        client.delete_answer(pk, request.user.email)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('balystic_qa')


class CommunityQACreateQuestionView(LoginRequiredMixin, View):
    template_name = "balystic/qa_create_question.html"

    def get(self, request):
        """
        Display the form for creating a question
        """
        form = QAQuestionForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Creates the question in the qa community
        """
        form = QAQuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user_email'] = request.user.email
            client = Client()
            client.create_question(data)
            return redirect('balystic_qa')
        context = {'form': form}
        return render(request, self.template_name, context)


class CommunityQAQuestionVoteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        client = Client()
        data = request.POST.copy()
        data['user_email'] = request.user.email
        client.vote_question(pk, data=data)
        return redirect('balystic_qa_detail', pk=pk)


class CommunityQAAnswerVoteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        client = Client()
        data = request.POST.copy()
        data['user_email'] = request.user.email
        client.vote_answer(pk, data=data)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('balystic_qa')


class CommunityQACloseQuestionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        client = Client()
        data = request.POST.copy()
        data['user_email'] = request.user.email
        client.close_question(pk, data=data)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('balystic_qa')


class CommunityQASelectAnswerView(LoginRequiredMixin, View):
    def post(self, request, pk):
        client = Client()
        data = request.POST.copy()
        data['user_email'] = request.user.email
        client.select_answer(pk, data=data)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('balystic_qa')


class CommunityQACreateCommentView(LoginRequiredMixin, View):
    def post(self, request, instance, object_id):
        client = Client()
        data = request.POST.copy()
        data['user_email'] = request.user.email
        client.create_comment(instance, object_id, data=data)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('balystic_qa')


class CommunityQAEditCommentView(LoginRequiredMixin, View):
    def post(self, request, instance, object_id):
        client = Client()
        data = request.POST.copy()
        data['user_email'] = request.user.email
        client.edit_comment(instance, object_id, data=data)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('balystic_qa')


class CommunityQADeleteCommentView(LoginRequiredMixin, View):

    def post(self, request, instance, object_id):
        client = Client()
        client.delete_comment(instance, object_id, request.user.email)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('balystic_qa')


class LoginView(View):
    """
    View that handles the authentication form.
    """
    template_name = 'balystic/login.html'

    def get(self, request):
        form = LoginForm()
        next_url = request.GET.get('next')
        return render(request, self.template_name, {'form': form, 'next_url': next_url})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.POST.get('next', ''): 
                        next = request.POST.get('next')
                        return redirect(next) 
                    else: 
                        url = 'http://' +\
                            user.url + '&next=' +\
                            request.build_absolute_uri('/users/~redirect/')
                        return redirect(url)
                else:
                    form.add_error(None, 'Account is not active')
            else:
                form.add_error(
                    None,
                    'Not able to authenticate with the given credentials')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    template_name = 'balystic/logout.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        logout(request)
        return redirect('balystic_login')
