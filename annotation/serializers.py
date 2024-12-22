from rest_framework import serializers
from .models import AnnotationProject, Image

class AnnotationProjectSerializer(serializers.ModelSerializer):
	creator = serializers.StringRelatedField()
	class Meta:
		model = AnnotationProject
		fields = '__all__'
		read_only_fields = ['creator',]


class ImageSerializer(serializers.ModelSerializer):
	project = serializers.StringRelatedField()

	class Meta:
		model = Image
		fields = '__all__'

class CreateImageSerializer(serializers.ModelSerializer):
	

	class Meta:
		model = Image
		fields = '__all__'



class UpdateImageSerializer(serializers.ModelSerializer):

	class Meta:
		model = Image
		exclude = ['project',]