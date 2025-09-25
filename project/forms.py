# forms.py
from django import forms
from .models import Project
from django.core.exceptions import ValidationError


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            # 'builder',
            'description',
            'image',
            'bedrooms',
            'bathrooms',
            'area',
            'floor',
            'parking',
            'price',
            'status',
            # 'created_at',
            # 'updated_at',
        ]
        
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) <= 3:
            raise ValidationError("Title must be longer than 3 characters.")
        return title
    
    def clean_bedrooms(self):
        bedrooms = self.cleaned_data.get('bedrooms')
        if bedrooms is not None and bedrooms <= 0:
            raise ValidationError("Bedrooms cannot be zero.")
        return bedrooms
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price in [None, '']:
            return 0.00
        return price

    
