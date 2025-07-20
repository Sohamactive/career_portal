from django import forms
from .models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import re
from .models import UserProfile,Certificate


class SignUpEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'you@example.com'}),
        required=True
    )

    dob=forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'class':'form-control','type':'date'}),
        required=True
    )

    #validation to ensure email is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email
    
    #validation to ensure the age is >=18
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            today = now().date()
            age = today.year - dob.year - ((today.month,today.day)<(dob.month,dob.day))
            if age < 18 :
                raise ValidationError("You must be at least 18 year old to register.")
        return dob
    


class OtpForm(forms.Form):

    otp = forms.CharField(
        max_length=6,
        min_length = 6,
        widget=forms.HiddenInput()
    )



class SetPasswordForm(forms.Form):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Custom strength rules
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Password must contain at least one special character.")
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Include all fields from the model that the user can edit
        fields = [
            'full_name',
            'profile_picture',
            'bio',
            'resume',
            'linkedin_url',
            'github_url',
        ]
        # Add widgets to apply CSS classes to the form fields
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

# We also need a form for the certificates
class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'file']
