from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound,Http404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from xlwt import Workbook
 
# les models
from .models import utilisateur_technicien
from .models import fiche_client
from .models import utilisateur_client
from .models import type_incident_client
from .models import type_incident_technicien
from .models import velo
from .models import incident
from .models import CHOICES

# les formulaire
from .forms import type_incident_clientForm
from .forms import type_incident_technicienForm
#Fonctions annexe
def is_technicien(request):
	try:
		utilisateur_technicien.objects.get(mail=request.user.email)
		return True
	except:
		return False

def is_client(request):
	try:
		utilisateur_client.objects.get(mail=request.user.email)
		return True
	except:
		return False






#Fonctions Pages
@login_required
def indexEquipe(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	count_magasin = fiche_client.objects.all().count()
	count_velo = velo.objects.all().count()
	count_incident_en_cours = incident.objects.filter(valider=False).count()
	count_incident_finie = incident.objects.exclude(valider=False).count()
	#info
	if technicien:
		return HttpResponseRedirect('/dms/liste_incident/')
	#info2
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'indexEquipe.html'
	return render(request,template,context)


@login_required
def page_technicien(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#liste des technicien
	liste_des_technicien = utilisateur_technicien.objects.exclude(archive=True)
	#créer et envoyer un mail au technicien
	if request.POST.get('create_technicien'):
		utilisateur_technicien(prenom=request.POST.get('prenom'),nom=request.POST.get('nom'),mail=request.POST.get('mail'),telephone=request.POST.get('tel')).save()
		send_mail('Compte - Velyvelo','Pour créer son compte velyvelo : velyvelo.com/accounts/signup/',settings.EMAIL_HOST_USER,[request.POST.get('mail')],fail_silently=False,)
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'technicien.html'
	return render(request,template,context)



@login_required
def create_client(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#créer la fiche client
	if request.POST.get('create_fiche_client'):
		fiche_client(numero_client=request.POST.get('numero_client'),numero_contrat=request.POST.get('numero_contrat'),denomination_social=request.POST.get('denomination_social'),adresse_facturation=request.POST.get('adresse_facturation'),enseigne=request.POST.get('enseigne'),adresse_enseigne=request.POST.get('adresse_enseigne')).save()
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'create_client.html'
	return render(request,template,context)


@login_required
def liste_fiche_client(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#liste des technicien
	liste_des_fiche_client = fiche_client.objects.exclude(archive=True)
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'liste_fiche_client.html'
	return render(request,template,context)


 
@login_required
def page_fiche_client(request,id_fiche_client):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#mise a jours
	if request.POST.get('majour'):
		info_fiche_client = fiche_client.objects.get(id=id_fiche_client)
		info_fiche_client.numero_client=request.POST.get('numero_client')
		info_fiche_client.numero_contrat=request.POST.get('numero_contrat')
		info_fiche_client.denomination_social=request.POST.get('denomination_social')
		info_fiche_client.adresse_facturation=request.POST.get('adresse_facturation')
		info_fiche_client.enseigne=request.POST.get('enseigne')
		info_fiche_client.adresse_enseigne=request.POST.get('adresse_enseigne')
		info_fiche_client.save()
		return HttpResponseRedirect('/dms/page_fiche_client/' + id_fiche_client + '/')
	#archiver
	if request.POST.get('supprfiche'):
		info_fiche_client = fiche_client.objects.get(id=id_fiche_client)
		info_fiche_client.archive = True
		info_fiche_client.save()
		return HttpResponseRedirect('/dms/liste_fiche_client/')
	#ajouter un utilisateur
	if request.POST.get('ajouter_client'):
		try:
			gars = utilisateur_client.objects.get(mail=request.POST.get('mail'))
			fiche_client.objects.get(id=id_fiche_client).utilisateur.add(utilisateur_client.objects.get(mail=request.POST.get('mail')))
		except:
			utilisateur_client(prenom=request.POST.get('prenom'),nom=request.POST.get('nom'),mail=request.POST.get('mail'),telephone=request.POST.get('telephone')).save()
			if request.user.is_superuser:
				plus = utilisateur_client.objects.get(mail=request.POST.get('mail'))
				plus.admin = True
				plus.save()
			send_mail('Mon Compte Velyvelo',"Bienvenue sur la plateforme VelyVelo,\n\nVous trouverez ci-dessous le lien vers notre formulaire de création de compte :\nvelyvelo.com/accounts/signup/\n\nNous nous tenons à votre disposition pour toutes vos questions.\n\nL’équipe VelyVelo",settings.EMAIL_HOST_USER,[request.POST.get('mail')],fail_silently=False,)
			fiche_client.objects.get(id=id_fiche_client).utilisateur.add(utilisateur_client.objects.get(mail=request.POST.get('mail')))
		
	if request.POST.get('remove_utilisateur'):
		fiche_client.objects.get(id=id_fiche_client).utilisateur.remove(utilisateur_client.objects.get(mail=request.POST.get('mail_remove')))
	
	if request.POST.get('ajouter_velo'):
		gars = velo.objects.get(id=request.POST.get('mes_velo'))
		gars.date_fin = request.POST.get('date_fin')
		gars.date_debut = request.POST.get('date_debut')
		fiche_client.objects.get(id=id_fiche_client).mes_velo.add(velo.objects.get(id=request.POST.get('mes_velo')))

	if request.POST.get('remove_velo'):
		fiche_client.objects.get(id=id_fiche_client).mes_velo.remove(velo.objects.get(id=request.POST.get('mes_velo_remove')))
	#Information client
	info_fiche_client = fiche_client.objects.get(id=id_fiche_client)
	liste_utilisateur_client = fiche_client.objects.get(id=id_fiche_client).utilisateur.all()
	liste_des_velo = velo.objects.exclude(archive=True)
	liste_mes_velo = fiche_client.objects.get(id=id_fiche_client).mes_velo.all()
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'page_fiche_client.html'
	return render(request,template,context)



@login_required
def page_type_incident_client(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	# le formulaire
	if request.POST.get('client_incident'):
		formdevis = type_incident_clientForm(request.POST, request.FILES)
		if formdevis.is_valid():
			post = formdevis.save(commit=False)
			post.save()
	else:
		formdevis = type_incident_clientForm()
	#suprimer incident
	if request.POST.get('remove_incident'):
		type_incident_client.objects.get(id=request.POST.get('incident_remove')).delete()
	#Information client
	#liste incident client
	liste_incident_client = type_incident_client.objects.all()
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'page_type_incident_client.html'
	return render(request,template,context)



@login_required
def page_type_incident_technicien(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	# le formulaire
	if request.POST.get('client_incident'):
		formdevis = type_incident_technicienForm(request.POST, request.FILES)
		if formdevis.is_valid():
			post = formdevis.save(commit=False)
			post.save()
	else:
		formdevis = type_incident_technicienForm()
	#suprimer incident
	if request.POST.get('remove_incident'):
		type_incident_technicien.objects.get(id=request.POST.get('incident_remove')).delete()
	#liste incident client
	liste_incident_technicien = type_incident_technicien.objects.all()
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'page_type_incident_technicien.html'
	return render(request,template,context)


@login_required
def create_velo(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#créer la fiche client
	if request.POST.get('create_velo'):
		velo(marque=request.POST.get('marque'),modele=request.POST.get('modele'),date_velo=request.POST.get('date_velo'),kilometrage=request.POST.get('kilometrage'),numero_cadre=request.POST.get('numero_cadre'),numero_moteur=request.POST.get('numero_moteur'),numero_battrie=request.POST.get('numero_battrie'),numero_bicycode=request.POST.get('numero_bicycode'),numero_gps=request.POST.get('numero_gps'),numero_cles_av=request.POST.get('numero_cles_av'),numero_cles_bt=request.POST.get('numero_cles_bt'),id_parc=request.POST.get('id_parc')).save()
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'create_velo.html'
	return render(request,template,context)


@login_required
def liste_velo(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#liste des technicien
	liste_des_velo = velo.objects.exclude(archive=True)
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'liste_velo.html'
	return render(request,template,context)



@login_required
def page_velo(request,id_velo):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#majour
	if request.POST.get('majour'):
		info_velo = velo.objects.get(id=id_velo)
		info_velo.marque = request.POST.get('marque')
		info_velo.modele = request.POST.get('modele')
		info_velo.date_velo = request.POST.get('date_velo')
		info_velo.numero_cadre = request.POST.get('numero_cadre')
		info_velo.numero_moteur = request.POST.get('numero_moteur')
		info_velo.numero_battrie = request.POST.get('numero_battrie')
		info_velo.numero_bicycode = request.POST.get('numero_bicycode')
		info_velo.numero_gps = request.POST.get('numero_gps')
		info_velo.numero_cles_av = request.POST.get('numero_cles_av')
		info_velo.numero_cles_bt = request.POST.get('numero_cles_bt')
		info_velo.kilometrage = request.POST.get('kilometrage')
		info_velo.save()
		return HttpResponseRedirect('/dms/page_velo/' + id_velo + '/')
	#archiver
	if request.POST.get('supprfiche'):
		info_velo = velo.objects.get(id=id_velo)
		info_velo.archive = True
		info_velo.save()
		return HttpResponseRedirect('/dms/liste_velo/')

	#Incident
	
	if request.POST.get('Envoyer'):
		inci = incident.objects.create(velo=velo.objects.get(id=id_velo),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=id_velo)))
		inci.commentaire = "Notif"
		for ob in request.POST.getlist('checks'):
			inci.incident_client.add(type_incident_client.objects.get(id=ob))
		inci.save()
		message = "Notification de nouvelles incidents,\nDate : " + str(inci.date_emmision) + " \n Client : " + fiche_client.objects.get(mes_velo=velo.objects.get(id=id_velo)).enseigne + " \n Dénomination social : " + fiche_client.objects.get(mes_velo=velo.objects.get(id=id_velo)).denomination_social + " \n\nvelyvelo.com/dms/liste_incident/"
		print(message)
		send_mail('INCIDENT - velyvelo',message,settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER],fail_silently=False,)
	#info velo
	info_velo = velo.objects.get(id=id_velo)
	liste_des_fiche_client = fiche_client.objects.exclude(archive=True)
	les_type_incident_client = type_incident_client.objects.all()
	liste_des_incident = incident.objects.exclude(archive=True).filter(velo=velo.objects.get(id=id_velo))
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'page_velo.html'
	return render(request,template,context)


def liste_incident(request):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#liste des technicien
	liste_des_incident_T = incident.objects.exclude(archive=True).filter(valider=True)
	liste_des_incident_F = incident.objects.exclude(archive=True).filter(valider=False)

	excel = "ok"
	if excel == "ok" and liste_des_incident_T.count() > 0:
		book = Workbook()
		feuil1 = book.add_sheet('Intervention')
		feuil1.write(0,0,'Client')
		feuil1.write(0,1,'Date')
		feuil1.write(0,2,'Vélos')
		feuil1.write(0,3,'Incidents')
		feuil1.write(0,4,'KM')
		feuil1.write(0,5,'Pièces')
		feuil1.write(0,6,'Prix')
		feuil1.write(0,7,'Action')
		feuil1.write(0,8,'Cause')

		countinci = 1
		for inci in liste_des_incident_T:
			ligne1 = feuil1.row(countinci)
			print(str([oa.nom for oa in inci.incident_client.all()][0]))
			ligne1.write(0,str(inci.client.denomination_social))
			ligne1.write(1,str(inci.date_emmision))
			ligne1.write(2,str(inci.velo.marque))
			ligne1.write(3,str([oa.nom for oa in inci.incident_client.all()][0]) )
			ligne1.write(4,int(inci.velo.kilometrage))
			try:
				ligne1.write(5,str([oa.nom for oa in inci.incident_technicien.all()][0]))
			except:
				ligne1.write(5,' ')
			try:
				ligne1.write(6,int([oa.prix for oa in inci.incident_technicien.all()][0]))
			except:
				ligne1.write(6,0)
			ligne1.write(7,' ')
			ligne1.write(8,str(inci.type_reparation))
			countinci += 1

		book.save('media/excel/intervention.xls')
	
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'liste_incident.html'
	return render(request,template,context)



def page_incident(request,id_incident):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#analyse
	if request.POST.get('REPARATION'):
		inci = incident.objects.get(id=id_incident)
		try:
			inci.nom_technicien = request.user.email
		except:
			pass
		inci.commentaire = request.POST.get('commentaire')
		inci.type_reparation = request.POST.get('type_rep')
		inci.valider = True
		for ob in request.POST.getlist('checks'):
			inci.incident_technicien.add(type_incident_technicien.objects.get(id=ob))
		inci.save()
		velometrage = velo.objects.get(id=incident.objects.get(id=id_incident).velo.id)
		velometrage.kilometrage = request.POST.get('kilometragein')
		velometrage.save()
	#INFO
	info_incident = incident.objects.get(id=id_incident)
	les_type_incident_technicien = type_incident_technicien.objects.all()
	info_reparation = CHOICES
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'page_incident.html'
	return render(request,template,context)





@login_required
def flotte(request,id_fiche_client):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#liste des technicien

	if request.POST.get('envoyer'):
 		if request.POST.get('mes_velo1') != 'veloun' and request.POST.get('mes_velo11') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo1')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo1'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo11')))
 			inci.save()
 		if request.POST.get('mes_velo2') != 'veloun' and request.POST.get('mes_velo22') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo2')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo2'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo22')))
 			inci.save()
 		if request.POST.get('mes_velo3') != 'veloun' and request.POST.get('mes_velo33') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo3')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo3'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo33')))
 			inci.save()
 		if request.POST.get('mes_velo4') != 'veloun' and request.POST.get('mes_velo44') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo4')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo4'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo44')))
 			inci.save()
 		if request.POST.get('mes_velo5') != 'veloun' and request.POST.get('mes_velo55') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo5')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo5'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo55')))
 			inci.save()
 		if request.POST.get('mes_velo6') != 'veloun' and request.POST.get('mes_velo66') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo6')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo6'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo66')))
 			inci.save()
 		if request.POST.get('mes_velo7') != 'veloun' and request.POST.get('mes_velo77') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo7')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo7'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo77')))
 			inci.save()
 		if request.POST.get('mes_velo8') != 'veloun' and request.POST.get('mes_velo88') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo8')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo8'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo88')))
 			inci.save()
 		if request.POST.get('mes_velo9') != 'veloun' and request.POST.get('mes_velo99') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo9')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo9'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo99')))
 			inci.save()
 		if request.POST.get('mes_velo100') != 'veloun' and request.POST.get('mes_velo100100') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo100')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo100'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo100100')))
 			inci.save()
 		if request.POST.get('mes_velo200') != 'veloun' and request.POST.get('mes_velo200200') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo200')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo200'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo200200')))
 			inci.save()
 		if request.POST.get('mes_velo300') != 'veloun' and request.POST.get('mes_velo300300') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo300')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo300'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo300300')))
 			inci.save()
 		if request.POST.get('mes_velo400') != 'veloun' and request.POST.get('mes_velo400400') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo400')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo400'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo400400')))
 			inci.save()
 		if request.POST.get('mes_velo500') != 'veloun' and request.POST.get('mes_velo500500') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo500')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo500'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo500500')))
 			inci.save()
 		if request.POST.get('mes_velo600') != 'veloun' and request.POST.get('mes_velo600600') != 'aucun':
 			inci = incident.objects.create(velo=velo.objects.get(id=request.POST.get('mes_velo600')),client=fiche_client.objects.get(mes_velo=velo.objects.get(id=request.POST.get('mes_velo600'))))
 			inci.commentaire = "Notif"
 			inci.incident_client.add(type_incident_client.objects.get(id=request.POST.get('mes_velo600600')))
 			inci.save()


	liste_des_velo = fiche_client.objects.get(id=id_fiche_client).mes_velo.all()
	liste_incident_client = type_incident_client.objects.all()
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'client/flotte.html'
	return render(request,template,context)



@login_required
def liste_incidents_client(request,id_fiche_client):
	#restriction
	technicien = is_technicien(request)
	client = is_client(request)
	#liste des technicien
	liste_des_incident_T = incident.objects.exclude(archive=True).filter(valider=True).filter(client=id_fiche_client)
	liste_des_incident_F = incident.objects.exclude(archive=True).filter(valider=False).filter(client=id_fiche_client)
	
	#info
	try:
		liste_des_magasin = fiche_client.objects.exclude(archive=True).filter(utilisateur=utilisateur_client.objects.get(mail=request.user.email))
	except:
		pass
	nb_incident_f = incident.objects.filter(valider=False).count()
	#Classique
	context = locals()
	template = 'client/liste_incidents_client.html'
	return render(request,template,context)
