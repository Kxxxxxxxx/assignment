from django.db import models

# Create your models here.
class Category(models.Model):
	category_name = models.CharField(max_length=200, null = True)
	def __str__(self):
		return self.category_name
