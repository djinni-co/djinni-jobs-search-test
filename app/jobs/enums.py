from django.db import models

from django.utils.translation import gettext_lazy as _


class Experience(models.TextChoices):
    ZERO = 'no_exp', _('No experience')
    ONE = '1y', _('1 year')
    TWO = '2y', _('2 years')
    THREE = '3y', _('3 years')
    FIVE = '5y', _('5 years')


class RemoteType(models.TextChoices):
    OFFICE = 'office', _('Office Work')
    PARTLY_REMOTE = 'partly_remote', _('Hybrid Remote')
    FULL_REMOTE = 'full_remote', _('Full Remote')
    CANDIDATE_CHOICE = 'candidate_choice', _('Office/Remote of your choice')


class RelocateType(models.TextChoices):
    NO_RELOCATE = 'no_relocate', _('No relocation')
    CANDIDATE_PAID = 'candidate_paid', _('Covered by candidate')
    COMPANY_PAID = 'company_paid', _('Covered by company')


class AcceptRegion(models.TextChoices):
    OFFICE_LOCATIONS = 'office_locations', _('Office locations')
    WORLDWIDE = '', _('Worldwide')
    UKRAINE = 'ukraine', _('Only Ukraine')
    EUROPE_ONLY = 'europe_only', _('Only Europe')
    EUROPE = 'europe', _('Ukraine + Europe')
    CUSTOM_SELECTION = 'custom_selection', _('Custom selection')


class EnglishLevel(models.TextChoices):
    NONE = ('no_english', 'No English')
    BASIC = ('basic', 'Beginner/Elementary')
    PRE = ('pre', 'Pre-Intermediate')
    INTERMEDIATE = ('intermediate', 'Intermediate')
    UPPER = ('upper', 'Upper-Intermediate')
    FLUENT = ('fluent', 'Advanced/Fluent')


class JobDomain(models.TextChoices):
    ADULT = 'adult', 'Adult'
    ADTECH = 'advertising', 'Advertising / Marketing'
    AUTOMOTIVE = 'automotive', 'Automotive'
    CRYPTO = 'crypto', 'Blockchain / Crypto'
    DATING = 'dating', 'Dating'
    ECOMMERCE = 'ecommerce', 'E-commerce / Marketplace'
    EDUTECH = 'edutech', 'Education'
    FINTECH = 'fintech', 'Fintech'
    GAMBLING = 'gambling', 'Gambling'
    GAMEDEV = 'gamedev', 'Gamedev'
    HARDWARE = 'hardware', 'Hardware / IoT'
    HEALTHCARE = 'healthcare', 'Healthcare / MedTech'
    MANUFACTURING = 'manufacturing', 'Manufacturing'
    ML = 'ml', 'Machine Learning / Big Data'
    MEDIA = 'media', 'Media'
    MILTECH = 'miltech', 'MilTech'
    MOBILE = 'mobile', 'Mobile'
    SAAS = 'saas', 'SaaS'
    SECURITY = 'security', 'Security'
    TELECOM = 'telecom', 'Telecom / Communications'
    TRAVEL = 'travel', 'Travel / Tourism'
    OTHER = 'other', 'Other'


class CompanyType(models.TextChoices):
    AGENCY = 'agency', _('Agency')
    OUTSOURCE = 'outsource', _('Outsource')
    OUTSTAFF = 'outstaff', _('Outstaff')
    PRODUCT = 'product', _('Product')
    STARTUP = 'startup', _('Startup')


class RemoteType(models.TextChoices):
    OFFICE = 'office', _('Office Work')
    PARTLY_REMOTE = 'partly_remote', _('Hybrid Remote')
    FULL_REMOTE = 'full_remote', _('Full Remote')
    CANDIDATE_CHOICE = 'candidate_choice', _('Office/Remote of your choice')


class CompanyType(models.TextChoices):
    AGENCY = ('agency/freelance', 'agency/freelance')
    PRODUCT = ('product', 'product')
    OUTSOURCE = ('outsource/outstaff', 'outsource/outstaff')
    OTHER = ('other', 'other')


class Status(models.TextChoices):
    """
    Цей клас був створений пілся StatusReview та StatusPublic як уніфіковані статуси
    для міграції на один статус, без подвійного флоу з StatusPublic та StatusReview.
    """

    DRAFT = 'draft', _('Draft')
    REVIEW = 'review', _('Review')
    PUBLISHED = 'published', _('Published')
    CLOSED = 'closed', _('Closed')
    ARCHIVED = 'archived', _('Archived')
    FAILED = 'failed', _('Failed')
