from django import forms
from django.contrib import admin
from leonardo.utils.widgets import get_htmltext_widget

from .models import Question


class QuestionAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'question_text': get_htmltext_widget(),
            'answer': get_htmltext_widget(),
        }


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm

    list_display = ('question_text', )


admin.site.register(Question, QuestionAdmin)
