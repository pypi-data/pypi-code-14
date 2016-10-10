# -*- coding: utf-8 -*-
from django.conf.urls import url
# from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # url(r'', TemplateView.as_view(template_name="balystic/base.html")),
    url(r'^login/$', views.LoginView.as_view(),
        name='balystic_user_login'),
    url(r'^signup/$', views.UserSignupView.as_view(),
        name='balystic_user_signup'),
    url(r'^users/$', views.CommunityUserList.as_view(),
        name='balystic_user_list'),
    url(r'^users/edit/(?P<username>[-\w.+]+)/$',
        views.CommunityUserUpdate.as_view(), name='balystic_user_update'),
    url(r'^users/(?P<username>[-\w.+]+)/$',
        views.CommunityUserDetail.as_view(),
        name='balystic_user_detail'),
    url(r'^blog/$',
        views.CommunityBlogListView.as_view(), name='balystic_blog'),
    url(r'^blog/(?P<slug>[-\w.]+)/$',
        views.CommunityBlogDetailView.as_view(), name='balystic_blog_detail'),
    url(r'^blog/(?P<slug>[-\w.]+)/delete/$',
        views.DeleteBlogView.as_view(), name='balystic_blog_delete'),
    url(r'^qa/$',
        views.CommunityQAListView.as_view(), name='balystic_qa'),
    url(r'^qa/(?P<pk>\d+)/$',
        views.CommunityQADetailView.as_view(), name='balystic_qa_detail'),

    url(r'^qa/create-question/$',
        views.CommunityQACreateQuestionView.as_view(),
        name='balystic_qa_create_question'),
    url(r'^qa/vote-question/(?P<pk>\d+)/$',
        views.CommunityQAQuestionVoteView.as_view(),
        name='balystic_qa_vote_question'),

    url(r'^qa/edit-question/(?P<pk>\d+)/$',
        views.CommunityQAEditQuestionView.as_view(),
        name='balystic_qa_edit_question'),

    url(r'^qa/delete-question/(?P<pk>\d+)/$',
        views.CommunityQADeleteQuestionView.as_view(),
        name='balystic_qa_delete_question'),

    url(r'^qa/close-question/(?P<pk>\d+)/$',
        views.CommunityQACloseQuestionView.as_view(),
        name='balystic_qa_close_question'),

    url(r'^qa/delete-answer/(?P<pk>\d+)/$',
        views.CommunityQADeleteAnswerView.as_view(),
        name='balystic_qa_delete_answer'),

    url(r'^qa/edit-answer/(?P<pk>\d+)/$',
        views.CommunityQAEditAnswerView.as_view(),
        name='balystic_qa_edit_answer'),

    url(r'^qa/vote-answer/(?P<pk>\d+)/$',
        views.CommunityQAAnswerVoteView.as_view(),
        name='balystic_qa_vote_answer'),

    url(r'^qa/select-answer/(?P<pk>\d+)/$',
        views.CommunityQASelectAnswerView.as_view(),
        name='balystic_qa_select_answer'),

    url(r'^qa/comment/(?P<instance>[-\w.]+)/(?P<object_id>[-\w.]+)/$',
        views.CommunityQACreateCommentView.as_view(),
        name='balystic_qa_comment'),

    url(r'^qa/delete-comment/(?P<instance>[-\w.]+)/(?P<object_id>[-\w.]+)/$',
        views.CommunityQADeleteCommentView.as_view(),
        name='balystic_qa_delete_comment'),

    url(r'^qa/edit-comment/(?P<instance>[-\w.]+)/(?P<object_id>[-\w.]+)/$',
        views.CommunityQAEditCommentView.as_view(),
        name='balystic_qa_edit_comment'),
]
