from django import forms
from jobs.models import Category, RemoteType, EnglishLevel, RelocateType, Experience, Location


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


class OrderSelectionForm(forms.Form):
    """
    Order job postings by these fields
    """
    selected_order = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(OrderSelectionForm, self).__init__(*args, **kwargs)
        self.order_choices = [("-applications_count", "Application counts (from highest)"),
                              ("-published", "Publishing Date (from newest)"),
                              ("applications_count", "Application counts (from lowest)"),
                              ("published", "Publishing Date (from oldest)")]


class CategoryFilterForm(forms.Form):
    """
    Encapsulate remaining filters extraction in one form
    """
    selected_category = forms.CharField(widget=forms.HiddenInput(), required=False)
    selected_remote_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    selected_english_level = forms.CharField(widget=forms.HiddenInput(), required=False)
    selected_experience_level = forms.CharField(widget=forms.HiddenInput(), required=False)
    selected_company = forms.CharField(
        required=False,
        label="Select company from dropdown",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Start typing company name', 'id': 'companies'})
    )
    selected_country = forms.CharField(
        required=False,
        label="Select country from dropdown",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Start typing country', 'id': 'countries'})
    )
    selected_location = forms.CharField(
        required=False,
        label="Select location from dropdown",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Start typing location', 'id': 'locations', 'disabled': True})
    )

    salary = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args, **kwargs)
        categories = Category.choices
        self.category_choices = [(value, label) for value, label in categories]
        remote_type = RemoteType.choices
        self.remote_type_choices = [(value, label) for value, label in remote_type]
        english_level = EnglishLevel.choices
        self.english_level_choices = [(value, label) for value, label in english_level]
        experience_level = Experience.choices
        self.experience_level_choices = [(value, label) for value, label in experience_level]
        locations = Location.choices
        self.location_choices = [(value, label) for value, label in locations]