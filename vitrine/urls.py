from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.indexVitrine, name='indexVitrine'),
    url(r'^nos_velos', views.nos_velos, name='nos_velos'),
    url(r'^nos_offres/restauration', views.restauration, name='restauration'),
    url(r'^nos_offres/livreur_auto-entrepreneur', views.livreur_auto, name='livreur_auto'),
    url(r'^nos_offres/foodtech', views.foodtech, name='foodtech'),
    url(r'^nos_offres/immobilier', views.immobilier, name='immobilier'),
    url(r'^nos_offres/entreprises_particuliers', views.entreprises_particuliers, name='entreprises_particuliers'),
    url(r'^notre_societe', views.notre_societe, name='notre_societe'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^notre_platforme', views.notre_platforme, name='notre_platforme'),
    url(r'^temoignages', views.temoignages, name='temoignages'),

]
