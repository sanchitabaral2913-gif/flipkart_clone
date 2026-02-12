from django import forms
from .models import Product, Review, Category

class ProductForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'description',
            'price',
            'image_front',
            'image_back',
            'image_left',
            'image_right',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter product description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product price'
            }),
            'image_front': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_back': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_left': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_right': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                attrs={'class': 'form-select'},
                choices=[(i, str(i)) for i in range(1, 6)]
            ),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review'}
            ),
        }
