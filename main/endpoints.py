from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, DestroyAPIView

from main.models import Form, Question, PossibleAnswer
from main.serializers import FormSerializer, QuestionSerializer, PossibleAnswerSerializer, AnswerSerializer, \
    UserSerializer, AnonymousUserSerializer


class RetrieveUpdateDestroyForm(RetrieveUpdateDestroyAPIView):
    serializer_class = FormSerializer

    def get_queryset(self):
        return Form.objects.filter(creator=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RetrieveUpdateDestroyForm, self).dispatch(request, *args, **kwargs)


class ListCreateForm(ListCreateAPIView):
    serializer_class = FormSerializer

    def get_queryset(self):
        return Form.objects.filter(creator=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ListCreateForm, self).dispatch(request, *args, **kwargs)


class RetrieveUpdateDestroyQuestion(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(form__creator=self.request.user)

    def update(self, request, *args, **kwargs):
        # calling serializer to validate the form id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # checking if the user owns the related form
        form = Form.objects.filter(id=request.data['form']).first()
        if form.creator != request.user:
            raise PermissionDenied
        return super(RetrieveUpdateDestroyQuestion, self).update(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RetrieveUpdateDestroyQuestion, self).dispatch(request, *args, **kwargs)


class ListCreateQuestion(ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(form__creator=self.request.user)

    def post(self, request, *args, **kwargs):
        # calling serializer to validate the form id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # checking if the user owns the related form
        form = Form.objects.filter(id=request.data['form']).first()
        if form.creator != request.user:
            raise PermissionDenied
        return super(ListCreateQuestion, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ListCreateQuestion, self).dispatch(request, *args, **kwargs)


class RetrieveUpdateDestroyPossibleAnswer(RetrieveUpdateDestroyAPIView):
    serializer_class = PossibleAnswerSerializer
    queryset = PossibleAnswer.objects.all()

    def get_queryset(self):
        return PossibleAnswer.objects.filter(question__form__creator=self.request.user)

    def update(self, request, *args, **kwargs):
        # calling serializer to validate the question id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # checking if the user owns the related form
        question = Question.objects.filter(id=request.data['question']).first()
        if question.form.creator != request.user:
            raise PermissionDenied
        return super(RetrieveUpdateDestroyPossibleAnswer, self).update(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RetrieveUpdateDestroyPossibleAnswer, self).dispatch(request, *args, **kwargs)


class ListCreatePossibleAnswer(ListCreateAPIView):
    serializer_class = PossibleAnswerSerializer

    def get_queryset(self):
        return PossibleAnswer.objects.filter(question__form__creator=self.request.user)

    def post(self, request, *args, **kwargs):
        # calling serializer to validate the question id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # checking if the user owns the related form
        question = Question.objects.filter(id=request.data['question']).first()
        if question.form.creator != request.user:
            raise PermissionDenied
        return super(ListCreatePossibleAnswer, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ListCreatePossibleAnswer, self).dispatch(request, *args, **kwargs)


class CreateAnswer(CreateAPIView):
    serializer_class = AnswerSerializer


class DestroyUser(DestroyAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if request.user != User.objects.filter(pk=pk).first():
            raise PermissionDenied
        return super(DestroyUser, self).delete(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DestroyUser, self).dispatch(request, *args, **kwargs)


class CreateAnonymousUser(CreateAPIView):
    serializer_class = AnonymousUserSerializer
