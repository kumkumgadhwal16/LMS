from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "price"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter course title"
            }),
            "description": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Enter course description"
            }),
            "price": forms.NumberInput(attrs={
                "min": "0",
                "step": "0.01"
            }),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError(
                "Price cannot be negative."
            )

        return price