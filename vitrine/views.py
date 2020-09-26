from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound,Http404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def indexVitrine(request):
	context = locals()
	template = 'indexVitrine.html'
	return render(request,template,context)

def nos_velos(request):
	context = locals()
	template = 'nos_velos.html'
	return render(request,template,context)

def restauration(request):
	context = locals()
	template = 'restauration.html'
	return render(request,template,context)

def livreur_auto(request):
	context = locals()
	template = 'livreur_auto.html'
	return render(request,template,context)

def foodtech(request):
	context = locals()
	template = 'foodtech.html'
	return render(request,template,context)

def immobilier(request):
	context = locals()
	template = 'immobilier.html'
	return render(request,template,context)

def entreprises_particuliers(request):
	context = locals()
	template = 'entreprises_particuliers.html'
	return render(request,template,context)

def notre_societe(request):
	context = locals()
	template = 'notre_societe.html'
	return render(request,template,context)

def contact(request):

	if request.POST.get('envoyer'):
			Nom = request.POST.get('name')
			commentaire =  request.POST.get('envoyer')
			offre = request.POST.get('offre')
			tel = request.POST.get('tel')
			objet = request.POST.get('subject')
			subject = Nom + " - " + objet
			emailFrom = request.POST.get('email')

			message ='%s \n\n Voici le mail pour répondre à %s : %s \n Voici le téléphone pour répondre à %s : %s' %(commentaire, Nom, emailFrom, Nom,tel)
			emailTo =[settings.EMAIL_HOST_USER]
			send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
			confirm_message = "Merci, Votre message à bien été envoyé !"
			
	context = locals()
	template = 'contact.html'
	return render(request,template,context)
	
def notre_platforme(request):
	context = locals()
	template = 'notre_platforme.html'
	return render(request,template,context)

def temoignages(request):
	context = locals()
	template = 'temoignages.html'
	return render(request,template,context)