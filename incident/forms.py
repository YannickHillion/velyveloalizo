from django import forms
from .models import type_incident_client
from .models import type_incident_technicien
from .models import incident

class type_incident_clientForm(forms.ModelForm):
	class Meta:
		model = type_incident_client
		fields = ('image','nom','description')
		widgets = {
			'image': forms.FileInput(attrs={'class': 'form-control-file','id':'file-input'}),
            'nom': forms.TextInput(attrs={'class': 'form-control','id':'text-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control','id':'text-input'}),
        }
	
class type_incident_technicienForm(forms.ModelForm):
	class Meta:
		model = type_incident_technicien
		fields = ('image','nom','description','prix')
		widgets = {
			'image': forms.FileInput(attrs={'class': 'form-control-file','id':'file-input'}),
            'nom': forms.TextInput(attrs={'class': 'form-control','id':'text-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control','id':'text-input'}),
            'prix': forms.TextInput(attrs={'class': 'form-control','id':'text-input'}),
        }