from django import forms
from jobs.models import Category

class JobFilterForm(forms.Form):
    """
    Construct initial form to filter jobs
    """
    q = forms.CharField(
        required=False,
        label="All Keywords",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search jobs'})
    )
    search_position = forms.BooleanField(
        required=False,
        label="Search by Position",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    search_long_description = forms.BooleanField(
        required=False,
        label="Search by Long Description",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    any_keywords = forms.CharField(
        required=False,
        label="Any of Keywords",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keywords separated by space'})
    )
    exclude_keywords = forms.CharField(
        required=False,
        label="Exclude Keywords",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keywords separated by space'})
    )

class CategoryFilterForm(forms.Form):
    """
    Primary keyword selection
    """
    selected_category = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args, **kwargs)
        categories = Category.choices
        self.category_choices = [(value, label) for value, label in categories]
