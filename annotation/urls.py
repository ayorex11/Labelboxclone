from django.urls import path
from . import views

urlpatterns = [
	path('create_annotation_project/', views.create_annotation_project),
	path('get_my_projects/', views.get_my_projects),
	path('get_all_projects/', views.get_all_projects),
	path('search_by_id/<int:pk>/', views.search_by_id),
	path('search_by_name/<str:name>/', views.search_by_name),
	path('update_annotation_project/<int:pk>/', views.update_annotation_project),
	path('delete_project/<int:pk>/', views.delete_project),
	path('add_image_to_project/', views.add_image_to_project),
	path('update_image/<int:pk>/', views.update_image),
	path('delete_image/<int:pk>/', views.delete_image),
]