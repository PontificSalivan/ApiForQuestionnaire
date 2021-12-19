from django.contrib import admin

from .models import Question, Questionnaire

admin.site.register(Question)
admin.site.register(Questionnaire)
