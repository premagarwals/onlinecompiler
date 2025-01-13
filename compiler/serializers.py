
from django.db.models import fields
from rest_framework import serializers
from .models import Solution, User, Problem, TestCase
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'username', 'email')

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('__all__')

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('__all__')

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('__all__')