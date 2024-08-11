from django import forms
from .models import JobPosting, Experience, RemoteType, EnglishLevel, CompanyType

class JobFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search jobs'}))
    position = forms.CharField(required=False, label='Position', widget=forms.TextInput(attrs={'placeholder': 'Python Developer'}))
    long_description = forms.CharField(required=False, label='Description', widget=forms.TextInput(attrs={'placeholder': 'Machine Learning Engineer'}))
    primary_keyword = forms.CharField(required=False, label='Primary Keyword', widget=forms.TextInput(attrs={'placeholder': 'Python'}))
    secondary_keyword = forms.CharField(required=False, label='Secondary Keyword', widget=forms.TextInput(attrs={'placeholder': 'Django'}))
    extra_keywords = forms.CharField(required=False, label='Extra Keywords', widget=forms.TextInput(attrs={'placeholder': 'Junior'}))
    salary_min = forms.IntegerField(required=False, label='Min Salary', widget=forms.TextInput(attrs={'placeholder': '1000'}))
    salary_max = forms.IntegerField(required=False, label='Max Salary', widget=forms.TextInput(attrs={'placeholder': '2000'}))
    remote_type = forms.ChoiceField(choices=RemoteType.choices, required=False, label='Remote Type')
    country = forms.CharField(required=False, label='Country', widget=forms.TextInput(attrs={'placeholder': 'Ukraine'}))
    location = forms.CharField(required=False, label='Location', widget=forms.TextInput(attrs={'placeholder': 'Lviv'}))
    english_level = forms.ChoiceField(choices=EnglishLevel.choices, required=False, label='English Level')
    experience_years = forms.ChoiceField(choices=Experience.choices, required=False, label='Experience Years')
    company_name = forms.CharField(required=False, label='Company Name', widget=forms.TextInput(attrs={'placeholder': 'Djinni'}))
