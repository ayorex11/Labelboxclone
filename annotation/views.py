from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import AnnotationProjectSerializer, ImageSerializer, UpdateImageSerializer, CreateImageSerializer
from .models import AnnotationProject, Image
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import FormParser, MultiPartParser


@swagger_auto_schema(methods=["POST"], request_body=AnnotationProjectSerializer())
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])

def create_annotation_project(request):
	user = request.user 
	serializer = AnnotationProjectSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save(creator=user)

	data = {
		'message':'success',
		'data':serializer.data 
	}
	return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_my_projects(request):
	user = request.user
	projects = AnnotationProject.objects.filter(creator=user)
	if not projects:
		return Response({'message':'No project created yet'}, status=status.HTTP_404_NOT_FOUND)

	serializer = AnnotationProjectSerializer(projects, many=True)

	data = {
		'message':'success',
		'data': serializer.data
	}
	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])


def get_all_projects(request):
	projects = AnnotationProject.objects.all()
	if not projects:
		return Response({'message':'No project created yet'}, status=status.HTTP_404_NOT_FOUND)

	serializer = AnnotationProjectSerializer(projects, many=True)
	data = {
		'message':'success',
		'data': serializer.data
	}
	return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])

def search_by_id(request, pk):
	project = get_object_or_404(AnnotationProject, id=pk)
	images = Image.objects.filter(project=project)
	if not images:
		return Response({'message':'No image in project yet.'}, status=status.HTTP_404_NOT_FOUND)
	serializer = ImageSerializer(images, many=True)

	data = {
		'message':'success',
		'data': serializer.data
	}
	return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])

def search_by_name(request, name):
	projects = AnnotationProject.objects.filter(name=name)
	if not projects:
		return Response({'message':'No project with such name. Check for spelling, upper or lower case letters.'}, status=status.HTTP_404_NOT_FOUND)
	serializer = AnnotationProjectSerializer(projects, many=True)

	data = {
		'message':'success',
		'data':serializer.data
	}
	return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=["PATCH"], request_body=AnnotationProjectSerializer())
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])

def update_annotation_project(request, pk):
	user = request.user 
	project = get_object_or_404(AnnotationProject, id=pk)
	if project.creator != user:
		return Response({'message':'You do not have access to edit this project.'}, status=status.HTTP_400_BAD_REQUEST)
	serializer = AnnotationProjectSerializer(project, data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save()
	data = {
		'message':'success',
		'data':serializer.data
	}
	return Response(data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])


def delete_project(request, pk):
	user = request.user
	project = get_object_or_404(AnnotationProject, id=pk)
	if project.creator != user:
		return Response({'message':'You do not have access to delete this project.'}, status=status.HTTP_400_BAD_REQUEST)
	project.delete()
	return Response({'message':'deleted'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(methods=["POST"], request_body=CreateImageSerializer())
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])

def add_image_to_project(request): 
	serializer = CreateImageSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save()

	data = {
		'message':'success',
		'data':serializer.data 
	}
	return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(methods=["PATCH"], request_body=UpdateImageSerializer())
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])



def update_image(request, pk):
	user = request.user 
	image = get_object_or_404(Image, id=pk)
	if image.project.creator != user:
		return Response({'message':'You do not have access to edit this image.'}, status=status.HTTP_400_BAD_REQUEST)
	serializer = UpdateImageSerializer(project, data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save()
	data = {
		'message':'success',
		'data':serializer.data
	}
	return Response(data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])


def delete_image(request, pk):
	user = request.user
	image = get_object_or_404(Image, id=pk)
	if image.project.creator != user:
		return Response({'message':'You do not have access to delete this image.'}, status=status.HTTP_400_BAD_REQUEST)
	image.delete()
	return Response({'message':'deleted'}, status=status.HTTP_204_NO_CONTENT)
