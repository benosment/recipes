from django import forms

from recipes.models import Recipe

EMPTY_TITLE_ERROR = "You can't have an empty recipe title"

class RecipeForm(forms.models.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title',)
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter the title of the recipe',
                'class': 'form-control input-lg',
            }),
        }

        error_messages = {
            'title': {'required': EMPTY_TITLE_ERROR}
        }
