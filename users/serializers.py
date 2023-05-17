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
        fields ='__all__'

class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields =['id','name','description','pub_date']
        
        # ['sid','name','pub_date']
        
    # sid = serializers.IntegerField(source='Summary.id', read_only = True )
    # name = serializers.CharField(source='Summary.name', read_only = True )
    # pub_date = serializers.DateField(source='Summary.pub_date', read_only = True )



