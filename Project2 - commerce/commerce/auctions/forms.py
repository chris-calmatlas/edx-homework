from django import forms
from .models import Category, Bid

class NewListing(forms.Form):
    title=forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Title", 
                "required": True
            }
        )
    )
    
    description=forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Provide a description of your item",
                "required": True,
                "maxlength": "600"
            }
        )
    )

    startingBid=forms.DecimalField(
        label="",
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Starting Bid in Dollars ($)",
                "required": True
            }
        )
    )
    
    imageUrl=forms.URLField(
        label="",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Enter an URL for an image (optional)"
            }
        )
    )
    
    category=forms.ModelChoiceField(
        label="",
        required=False,
        queryset=Category.objects.all(),
        empty_label="Select a category (optional)",
        widget=forms.Select(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Choose a category"
            }
        )
    )

class NewBid(forms.Form):
    bidAmount=forms.DecimalField(
        label="",
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Bid now",
                "required": True
            }
        )
    )

class ConfirmForm(forms.Form):
    Confirm=forms.BooleanField(required=True)

class CommentForm(forms.Form):
    content=forms.CharField(
        label="",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Comment on this listing",
                "required": True,
                "maxlength": "600"
            }
        )
    )

class Checkbox(forms.Form):
    checked=forms.BooleanField(required=False)