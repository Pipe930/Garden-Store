from django import forms

class FormularioContacto(forms.Form):
    nombreUsuario = forms.CharField(label="Nombre de Usuario", max_length=40, required=True)
    email = forms.EmailField(label="Correo", max_length=60, required=True)
    mensaje = forms.CharField(label="Mensaje", max_length=200, widget=forms.Textarea)