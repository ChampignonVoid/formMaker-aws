from django.contrib.auth.models import User

from rest_framework import serializers

from formMaker.helpers import generate_hash
from main.models import Form, Question, PossibleAnswer, Answer, AnonymousUser


class FormSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        validated_data['uuid'] = generate_hash()
        return super(FormSerializer, self).create(validated_data)

    class Meta:
        model = Form
        fields = ('id', 'uuid')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class PossibleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossibleAnswer
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AnonymousUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['uuid'] = generate_hash()
        return super(AnonymousUserSerializer, self).create(validated_data)

    class Meta:
        model = AnonymousUser
        fields = '__all__'
