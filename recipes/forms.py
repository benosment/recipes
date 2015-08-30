from django import forms

from recipes.models import Recipe

class RecipeForm(forms.models.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title',
                  'ingredients',
                  'directions',
                  'servings',
                  'source',
                  'source_url',
                  'img_url',
                  'cooking_time',
                  'total_time',
                  'notes')
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter the title of the recipe',
                'class': 'form-control',
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'directions': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'servings': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'source': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'source_url': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'img_url': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'cooking_time': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'total_time': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }
