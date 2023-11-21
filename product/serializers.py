from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Upload
from .models import Person





class UploadSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Upload
        fields = '__all__'

    def get_owner(self, obj):
        return self.context['request'].user.id if self.context.get('request') else None

    def create(self, validated_data):
        return Upload.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email_ow = validated_data.get('email_ow', instance.email_ow)
        instance.password_em = validated_data.get('password_em', instance.password_em)
        instance.message = validated_data.get('message', instance.message)
        instance.file = validated_data.get('file', instance.file)
        instance.create_at = validated_data.get('create_at', instance.create_at)
        instance.save()
        return instance






class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'




class PersonSelectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['selected']

    def update(self, instance, validated_data):
        
        instance.selected = validated_data.get('selected', instance.selected)
        instance.save()
        return instance
