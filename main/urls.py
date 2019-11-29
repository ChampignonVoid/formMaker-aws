from django.urls import path, re_path  # noqa: F401
from django.views.generic import TemplateView  # noqa: F401

from main.endpoints import RetrieveUpdateDestroyForm, RetrieveUpdateDestroyPossibleAnswer, \
    ListCreatePossibleAnswer, RetrieveUpdateDestroyQuestion, ListCreateQuestion, ListCreateForm, CreateAnswer, \
    DestroyUser, CreateAnonymousUser
from main.views import form, form_token, form_create, my_forms, form_summary

urlpatterns = [
    path('form_token', form_token, name='form_token'),
    path('form_create', form_create, name='form_create'),
    path('my_forms', my_forms, name='my_forms'),
    path('form_summary/<str:uuid>/', form_summary, name='form_summary'),
    path('api/', TemplateView.as_view(template_name='main/api.html'), name='api'),
    path('', TemplateView.as_view(template_name='main/index.html'), name='index'),
    re_path('forms/(?P<pk>\d+)/$', RetrieveUpdateDestroyForm.as_view(), name='forms_endpoint_pk'),  # noqa: W605
    re_path('forms/$', ListCreateForm.as_view(), name='forms_endpoint'),
    re_path('questions/(?P<pk>\d+)/$', RetrieveUpdateDestroyQuestion.as_view(),  # noqa: W605
        name='questions_endpoint_pk'),  # noqa: W605
    re_path('questions/$', ListCreateQuestion.as_view(), name='questions_endpoint'),
    re_path('possible_answers/(?P<pk>\d+)/$', RetrieveUpdateDestroyPossibleAnswer.as_view(),  # noqa: W605
            name='possible_answers_endpoint_pk'),
    re_path('possible_answers/$', ListCreatePossibleAnswer.as_view(), name='possible_answers_endpoint'),
    re_path('answers/$', CreateAnswer.as_view(), name='answers_endpoint'),
    re_path('users/(?P<pk>\d+)/$', DestroyUser.as_view(), name='users_endpoint_pk'),  # noqa: W605
    re_path('anonymous_users/$', CreateAnonymousUser.as_view(), name='anonymous_users_endpoint'),
    path('<str:uuid>', form, name='form'),
]
