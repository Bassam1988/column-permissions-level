from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm 
from .models import CustomUser 
 
class CustomUserCreationForm(UserCreationForm):    
    class Meta:        
        model = CustomUser        
        fields = ('email', 'username', 'password1', 'password2')  
        
class CustomUserChangeForm(UserChangeForm):    
    class Meta:        
        model = CustomUser        
        fields = UserChangeForm.Meta.fields