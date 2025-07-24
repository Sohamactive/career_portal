from django import forms

class ApplicationForm(forms.Form):
    cover_letter = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}),
        required=False
    )
    
