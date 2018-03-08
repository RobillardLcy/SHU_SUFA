from rest_framework import serializers
from .models import Members, MembersClasses


<<<<<<< HEAD
class MemberRegistrationSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, min_length=8, max_length=8)
    name = serializers.CharField(required=True, max_length=50)
    gender = serializers.CharField(required=True, max_length=6)
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)
    email = serializers.EmailField(allow_null=True, max_length=50)
    campus = serializers.CharField(required=True, min_length=2, max_length=2)
    favorite_club = serializers.CharField(required=True, max_length=20)
    photo = serializers.ImageField(allow_null=True, max_length=100)
    password = serializers.CharField(required=True, min_length=6, max_length=32, write_only=True)

    def create(self, validated_data):
        return Members.objects.create(**validated_data)
=======
class MemberSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, min_length=8, max_length=8)
    name = serializers.CharField(read_only=True, max_length=50)
    gender = serializers.CharField(read_only=True, max_length=6)
    mobile = serializers.CharField(min_length=11, max_length=11)
    email = serializers.EmailField(allow_null=True, max_length=50)
    campus = serializers.CharField(min_length=2, max_length=2)
    favorite_club = serializers.CharField(max_length=20)
    photo = serializers.ImageField(allow_null=True, max_length=100)
>>>>>>> d3c299ebbac2d325a97214a5d1782b8c50f6acce

    def create(self, validated_data):
        return Members.objects.create(**validated_data)

<<<<<<< HEAD
class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        models = Members.objects.all()
        fields = ('id', 'name', 'gender', 'mobile', 'email', 'campus', 'favorite_club', 'photo')
=======

class MemberLoginSerializer(serializers.Serializer):
    pass


class MemberActiveSerializer(serializers.Serializer):
    pass


class MemberProfileSerializer(serializers.Serializer):
    pass


class MemberResetPasswordSerializer(serializers.Serializer):
    pass
>>>>>>> d3c299ebbac2d325a97214a5d1782b8c50f6acce


class MembersAdminSerializer(serializers.Serializer):
    pass


class MemberClassesSerializer(serializers.Serializer):
    pass
