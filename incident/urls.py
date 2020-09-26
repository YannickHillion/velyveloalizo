from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.indexEquipe, name='indexEquipe'),

	url(r'^technicien/', views.page_technicien, name='technicien'),
	url(r'^create_client/', views.create_client, name='create_client'),
	url(r'^liste_fiche_client/', views.liste_fiche_client, name='liste_fiche_client'),
	url(r'^page_fiche_client/(?P<id_fiche_client>\w+)/', views.page_fiche_client, name='page_fiche_client'),
	url(r'^page_type_incident_client/', views.page_type_incident_client, name='page_type_incident_client'),
	url(r'^page_type_incident_technicien/', views.page_type_incident_technicien, name='page_type_incident_technicien'),
	url(r'^create_velo/', views.create_velo, name='create_velo'),
	url(r'^liste_velo/', views.liste_velo, name='liste_velo'),
	url(r'^page_velo/(?P<id_velo>\w+)/', views.page_velo, name='page_velo'),
	url(r'^liste_incident/', views.liste_incident, name='liste_incident'),
	url(r'^page_incident/(?P<id_incident>\w+)/', views.page_incident, name='page_incident'),


	#client
	url(r'^flotte/(?P<id_fiche_client>\w+)/', views.flotte, name='flotte'),
	url(r'^liste_incidents_client/(?P<id_fiche_client>\w+)/', views.liste_incidents_client, name='liste_incidents_client'),

] 
