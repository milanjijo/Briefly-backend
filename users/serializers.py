from rest_framework import serializers
from .models import User, Summary


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['email','text','summary','pub_date']
        
    def create(self, validated_data):
        print(validated_data)
        instance = Summary(**validated_data)
        instance.save()
        return instance



