from django.db import models
from django.forms import ModelForm
from django.conf import settings

class notre_equipe_bdd(models.Model):
	ordre = models.CharField(default=' ',max_length=400)
	nomPrenom = models.CharField(default=' ',max_length=400)
	

	class Meta:
		verbose_name = "notre equipe bdd"
		ordering = ['ordre']
	
	def __str__(self):
		return self.nomPrenom
