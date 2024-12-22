from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AnnotationProject(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=500, blank=False)

	def __str__(self):
		return self.name

class Image(models.Model):
    project = models.ForeignKey(AnnotationProject, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    annotated_data = models.JSONField(null=True, blank=True)

    def __str__(self):
    	return self.image_file
