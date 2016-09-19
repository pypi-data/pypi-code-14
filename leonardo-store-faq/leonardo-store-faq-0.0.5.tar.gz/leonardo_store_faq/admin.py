from django import forms
from django.contrib import admin
from leonardo.widgets import get_htmltext_widget

from .models import Question


class QuestionAdminForm(forms.ModelForm):

    class Meta:
        model = Question
        widgets = {
            'question_text': get_htmltext_widget(),
            'answer': get_htmltext_widget()
        }
        exclude = tuple()


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm

    list_display = ('name', )


admin.site.register(Question, QuestionAdmin)
