from django.contrib import admin

# Register your models here.
from .models import utilisateur_client
from .models import utilisateur_technicien
from .models import fiche_client
from .models import velo
from .models import type_incident_technicien
from .models import type_incident_client
from .models import incident

class utilisateur_clientAdmin(admin.ModelAdmin):
	list_display = ('mail','admin')

class utilisateur_technicienAdmin(admin.ModelAdmin):
	list_display = ('id','mail')

class fiche_clientAdmin(admin.ModelAdmin):
	list_display = ('numero_client','numero_contrat')

class veloAdmin(admin.ModelAdmin):
	list_display = ('id','surnom')

class type_incident_clientAdmin(admin.ModelAdmin):
	list_display = ('id','nom')

class type_incident_technicienAdmin(admin.ModelAdmin):
	list_display = ('id','nom')

class incidentAdmin(admin.ModelAdmin):
	list_display = ('velo','client')



    
admin.site.register(utilisateur_client,utilisateur_clientAdmin)
admin.site.register(utilisateur_technicien,utilisateur_technicienAdmin)
admin.site.register(fiche_client,fiche_clientAdmin)
admin.site.register(velo,veloAdmin)
admin.site.register(type_incident_technicien,type_incident_technicienAdmin)
admin.site.register(type_incident_client,type_incident_clientAdmin)
admin.site.register(incident,incidentAdmin)