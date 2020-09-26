from django.contrib import admin

# Register your models here.
from .models import notre_equipe_bdd


class notre_equipe_bddAdmin(admin.ModelAdmin):
	list_display = ('nomPrenom','ordre')


admin.site.register(notre_equipe_bdd,notre_equipe_bddAdmin)
