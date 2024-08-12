from django.db import models
from django.utils.translation import gettext_lazy as _


class Experience(models.TextChoices):
    ZERO = "0", _("No experience")
    ONE = "1", _("1 year")
    TWO = "2", _("2 years")
    THREE = "3", _("3 years")
    FOUR = "4", _("4 years")
    FIVE = "5", _("5 years")
    SIX = "6", _("6 years")
    SEVEN = "7", _("7 years")
    EIGHT = "8", _("8 years")
    NINE = "9", _("9 years")
    TEN = "10", _("10 years")


class RemoteType(models.TextChoices):
    OFFICE = "office", _("Office Work")
    PARTLY_REMOTE = "partly_remote", _("Hybrid Remote")
    FULL_REMOTE = "full_remote", _("Full Remote")
    CANDIDATE_CHOICE = "candidate_choice", _("Office/Remote of your choice")


class RelocateType(models.TextChoices):
    NO_RELOCATE = "no_relocate", _("No relocation")
    CANDIDATE_PAID = "candidate_paid", _("Covered by candidate")
    COMPANY_PAID = "company_paid", _("Covered by company")


class AcceptRegion(models.TextChoices):
    OFFICE_LOCATIONS = "office_locations", _("Office locations")
    WORLDWIDE = "worldwide", _("Worldwide")
    UKRAINE = "ukraine", _("Only Ukraine")
    EUROPE_ONLY = "europe_only", _("Only Europe")
    EUROPE = "europe", _("Ukraine + Europe")
    CUSTOM_SELECTION = "custom_selection", _("Custom selection")


class EnglishLevel(models.TextChoices):
    NONE = ("no_english", "No English")
    BASIC = ("basic", "Beginner/Elementary")
    PRE = ("pre", "Pre-Intermediate")
    INTERMEDIATE = ("intermediate", "Intermediate")
    UPPER = ("upper", "Upper-Intermediate")
    FLUENT = ("fluent", "Advanced/Fluent")


class JobDomain(models.TextChoices):
    ADULT = "adult", "Adult"
    ADTECH = "advertising", "Advertising / Marketing"
    AUTOMOTIVE = "automotive", "Automotive"
    CRYPTO = "crypto", "Blockchain / Crypto"
    DATING = "dating", "Dating"
    ECOMMERCE = "ecommerce", "E-commerce / Marketplace"
    EDUTECH = "edutech", "Education"
    FINTECH = "fintech", "Fintech"
    GAMBLING = "gambling", "Gambling"
    GAMEDEV = "gamedev", "Gamedev"
    HARDWARE = "hardware", "Hardware / IoT"
    HEALTHCARE = "healthcare", "Healthcare / MedTech"
    MANUFACTURING = "manufacturing", "Manufacturing"
    ML = "ml", "Machine Learning / Big Data"
    MEDIA = "media", "Media"
    MILTECH = "miltech", "MilTech"
    MOBILE = "mobile", "Mobile"
    SAAS = "saas", "SaaS"
    SECURITY = "security", "Security"
    TELECOM = "telecom", "Telecom / Communications"
    TRAVEL = "travel", "Travel / Tourism"
    OTHER = "other", "Other"


class CompanyType(models.TextChoices):
    AGENCY = "agency", _("Agency")
    OUTSOURCE = "outsource", _("Outsource")
    OUTSTAFF = "outstaff", _("Outstaff")
    PRODUCT = "product", _("Product")
    STARTUP = "startup", _("Startup")


class Country(models.TextChoices):
    UKRAINE = "UKR", _("Ukraine")
    POLAND = "POL", _("Poland")
    PORTUGAL = "PRT", _("Portugal")
    CYPRUS = "CYP", _("Cyprus")
    USA = "USA", _("USA")
    ARMENIA = "ARM", _("Armenia")
    BULGARIA = "BGR", _("Bulgaria")
    ROMANIA = "ROU", _("Romania")
    GEORGIA = "GEO", _("Georgia")
    GERMANY = "DEU", _("Germany")
    OTHER = "OTH", _("Other")


# Duplicate of an existing 'RemoteType class'
# class RemoteType(models.TextChoices):
#         OFFICE = "office", _("Office Work")
#         PARTLY_REMOTE = "partly_remote", _("Hybrid Remote")
#         FULL_REMOTE = "full_remote", _("Full Remote")
#         CANDIDATE_CHOICE = "candidate_choice", _("Office/Remote of your choice")

# Duplicate of an existing 'CompanyType class'
# class CompanyType(models.TextChoices):
#     AGENCY = ("agency/freelance", "agency/freelance")
#     PRODUCT = ("product", "product")
#     OUTSOURCE = ("outsource/outstaff", "outsource/outstaff")
#     OTHER = ("other", "other")


class JobPosting(models.Model):
    class Status(models.TextChoices):
        """
        Цей клас був створений пілся StatusReview та StatusPublic як уніфіковані статуси
        для міграції на один статус, без подвійного флоу з StatusPublic та StatusReview.
        """

        DRAFT = "draft", _("Draft")
        REVIEW = "review", _("Review")
        PUBLISHED = "published", _("Published")
        CLOSED = "closed", _("Closed")
        ARCHIVED = "archived", _("Archived")
        FAILED = "failed", _("Failed")

    # Job description fields
    position = models.CharField(max_length=250, blank=False, default='')
    primary_keyword = models.CharField(max_length=50, blank=True, default="", null=True)
    secondary_keyword = models.CharField(max_length=50, blank=True, default="", null=True)
    long_description = models.TextField(blank=True, default='')

    domain = models.CharField(
        max_length=20,
        blank=True,
        default="",
        null=True,
        choices=JobDomain.choices,
    )
    company_type = models.CharField(
        max_length=20,
        blank=True,
        default="",
        null=True,
        choices=CompanyType.choices,
    )

    salary_min = models.IntegerField(blank=True, null=True, default=0)
    salary_max = models.IntegerField(blank=True, null=True, default=0)
    public_salary_min = models.IntegerField(blank=True, null=True, default=0)
    public_salary_max = models.IntegerField(blank=True, null=True, default=0)

    # Skills
    extra_keywords = models.CharField(max_length=250, blank=True, null=True, default="")
    experience_years = models.FloatField(default=0)
    english_level = models.CharField(
        max_length=15, blank=True, default="", null=True, choices=EnglishLevel.choices
    )

    country = models.CharField(max_length=250, blank=True, default="", null=True)
    location = models.CharField(max_length=250, blank=True, default="", null=True)
    accept_region = models.CharField(
        max_length=20,
        blank=True,
        default="",
        null=True,
        choices=AcceptRegion.choices,
    )
    remote_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
        choices=RemoteType.choices,
    )

    is_parttime = models.BooleanField(default=False, db_index=True)
    has_test = models.BooleanField(default=False, db_index=True)
    requires_cover_letter = models.BooleanField(default=False, db_index=True)
    is_ukraine_only = models.BooleanField(default=False, db_index=True)
    is_reserving_from_mobilisation = models.BooleanField(default=False)

    # Counts
    unread_count = models.IntegerField(blank=False, default=0)
    search_count = models.IntegerField(
        blank=False,
        default=0
    )  # unused, how many candidates for this job
    views_count = models.IntegerField(blank=False, default=0)
    applications_count = models.IntegerField(blank=False, default=0)
    sent_count = models.IntegerField(blank=False, default=0)

    recruiter = models.ForeignKey(
        'Recruiter',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_index=True
    )
    company = models.ForeignKey(
        "Company", models.SET_NULL, blank=True, null=True, db_index=True
    )

    # Meta fields
    status = models.CharField(
        blank=True,
        default=Status.DRAFT,
        db_index=True,
        choices=Status.choices,
        max_length=10,
    )
    last_modified = models.DateTimeField(blank=True, null=True, auto_now=True, db_index=True)
    published = models.DateTimeField(blank=True, null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Recruiter(models.Model):
    email = models.EmailField(blank=False, db_index=True, unique=True)
    name = models.CharField(max_length=250, blank=False, default="")
    company_id = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()


class Company(models.Model):
    name = models.CharField(max_length=250, blank=False, default="")
    company_type = models.CharField(
        max_length=20, blank=True, null=True, default="", choices=CompanyType.choices,
    )
    country_code = models.CharField(
        max_length=3,
        blank=True, null=True,
        default="",
        db_index=True,
    )
    is_international = models.BooleanField(default=False)
    dou_link = models.CharField(max_length=255, blank=True, null=True, default="")
    shortcode = models.CharField(
        max_length=10, db_index=True, blank=False, default="", unique=True
    )
    logo_url = models.CharField(max_length=255, blank=True, null=True, default="")
    created = models.DateTimeField(auto_now_add=True, db_index=True)
