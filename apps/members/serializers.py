from rest_framework import serializers
from .models import Members, MembersClasses


class MemberRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True, min_length=8, max_length=8)
    name = serializers.CharField(required=True, max_length=50)
    gender = serializers.CharField(required=True, max_length=6)
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)
    campus = serializers.CharField(required=True, min_length=2, max_length=2)
    favorite_club = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True, min_length=6, max_length=32, write_only=True)

    def create(self, validated_data):
        return Members.objects.create(**validated_data)

    class Meta:
        model = Members
        fields = ('id', 'name', 'gender', 'mobile', 'campus', 'favorite_club', 'password')


class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        models = Members.objects.all()
        fields = ('id', 'name', 'gender', 'mobile', 'email', 'campus', 'favorite_club', 'photo')


class MemberResetPasswordSerializer(serializers.ModelSerializer):
    pass


class MemberClassesSerializer(serializers.ModelSerializer):
    pass
