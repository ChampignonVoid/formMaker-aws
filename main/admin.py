from django.contrib import admin

from main.models import Form, Question, PossibleAnswer, Answer

admin.site.register(Form)
admin.site.register(Question)
admin.site.register(PossibleAnswer)
admin.site.register(Answer)
