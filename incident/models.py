from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up


 
class utilisateur_client(models.Model):
	mail = models.CharField(default=' ',max_length=400)
	admin = models.BooleanField(default=False)
	nom = models.CharField(default=' ',max_length=400)
	prenom = models.CharField(default=' ',max_length=400)
	telephone = models.CharField(default=' ',max_length=400)
	#Archive
	archive = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Utilisateur client"
		ordering = ['mail']
	
	def __str__(self):
		return self.mail






class utilisateur_technicien(models.Model):
	mail = models.CharField(default=' ',max_length=400)
	nom = models.CharField(default=' ',max_length=400)
	prenom = models.CharField(default=' ',max_length=400)
	telephone = models.CharField(default=' ',max_length=400)
	#Archive
	archive = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Utilisateur technicien"
		ordering = ['mail']
	
	def __str__(self):
		return self.mail




class velo(models.Model):
	#Le client peut modifier le surnom du velo
	surnom = models.CharField(default=' ',max_length=400)
	id_parc = models.CharField(default=' ',max_length=400)
	#Le vélo
	marque = models.CharField(default=' ',max_length=400)
	modele = models.CharField(default=' ',max_length=400)
	date_velo = models.DateField(null=True)
	#date
	date_debut = models.DateField(null=True)
	date_fin = models.DateField(null=True)
	#technique
	numero_cadre = models.CharField(default=' ',max_length=400)
	numero_moteur = models.CharField(default=' ',max_length=400)
	numero_battrie = models.CharField(default=' ',max_length=400)
	numero_bicycode = models.CharField(default=' ',max_length=400)
	numero_gps = models.CharField(default=' ',max_length=400)
	numero_cles_av = models.CharField(default=' ',max_length=400)
	numero_cles_bt = models.CharField(default=' ',max_length=400)
	kilometrage = models.CharField(default=' ',max_length=400)
	#Apartenance au client
	
	archive = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Les vélo"
		ordering = ['id']
	
	def __str__(self):
		return self.numero_cadre

class fiche_client(models.Model):
	#Information de facturations
	numero_client = models.CharField(default=' ',max_length=400)
	numero_contrat = models.CharField(default=' ',max_length=400)
	date_debut = models.DateField(null=True)
	date_fin = models.DateField(null=True)
	denomination_social = models.CharField(default=' ',max_length=400)
	adresse_facturation  = models.CharField(default=' ',max_length=400)

	#Informatin emplacement
	enseigne = models.CharField(default=' ',max_length=400)
	adresse_enseigne = models.CharField(default=' ',max_length=400) #Emplacement velos

	#Utilisateurs 
	utilisateur = models.ManyToManyField(utilisateur_client, verbose_name="Liste de utilisateurs")
	mes_velo = models.ManyToManyField(velo, verbose_name="Liste des velos")

	#Archive
	archive = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Les fiches client"
		ordering = ['numero_client']
	
	def __str__(self):
		return self.numero_client

class type_incident_technicien(models.Model):
	image = models.FileField(upload_to='type_incident_technicien/', null=True)
	nom = models.CharField(default=' ',max_length=400)
	description = models.CharField(default=' ',max_length=400)
	prix = models.CharField(default=' ',max_length=400)

	class Meta:
		verbose_name = "Les types d'incident"
		ordering = ['nom']
	
	def __str__(self):
		return self.nom



class type_incident_client(models.Model):
	image = models.FileField(upload_to='type_incident_client/', null=True)
	nom = models.CharField(default=' ',max_length=400)
	description = models.CharField(default=' ',max_length=400)

	class Meta:
		verbose_name = "Les types d'incident client"
		ordering = ['nom']
	
	def __str__(self):
		return self.nom


CHOICES = (
		   ('Panne','Panne'),
           ('Usure','Usure'),
           ('Casse','Casse')
       	  )

class incident(models.Model):
	photo_incident_technicien = models.FileField(upload_to='incident_technicien/', null=True)
	incident_technicien = models.ManyToManyField(type_incident_technicien, verbose_name="Liste des incident")
	incident_client = models.ManyToManyField(type_incident_client, verbose_name="Liste des incident")
	velo = models.ForeignKey(velo, on_delete=models.CASCADE, null=True)
	commentaire = models.TextField(default=' ',max_length=None)
	date_emmision = models.DateTimeField(default=timezone.now)
	client = models.ForeignKey(fiche_client, on_delete=models.CASCADE, null=True)

	type_reparation = models.CharField(choices=CHOICES,max_length=50, null=True)
	nom_technicien = models.CharField(default=' ',max_length=400)
	valider = models.BooleanField(default=False)
	date_validation = models.DateField(null=True)
	
	archive = models.BooleanField(default=False)

	class Meta:
		verbose_name = "Les incident"
		ordering = ['id']
	
	def __str__(self):
		return self.commentaire



