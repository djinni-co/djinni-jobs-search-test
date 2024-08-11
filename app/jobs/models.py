from django.db import models
from django.utils.translation import gettext_lazy as _


CATEGORIES = {
    'JavaScript / Front-End': 'JavaScript',
    'Fullstack': 'Fullstack',
    'Java': 'Java',
    'C# / .NET': '.NET',
    'Python': 'Python',
    'PHP': 'PHP',
    'Node.js': 'Node.js',
    'iOS': 'iOS',
    'Android': 'Android',
    'React Native': 'React Native',
    'C / C++ / Embedded': 'C++',
    'Flutter': 'Flutter',
    'Golang': 'Golang',
    'Ruby': 'Ruby',
    'Scala': 'Scala',
    'Salesforce': 'Salesforce',
    'Rust': 'Rust',
    'Elixir': 'Elixir',
    'Kotlin': 'Kotlin',
    'ERP Systems': 'ERP',
    'QA Manual': 'QA',
    'QA Automation': 'QA Automation',
    'Design': 'Design',
    '2D/3D Artist / Illustrator': 'Artist',
    'Gamedev': 'Unity',
    'Project Manager': 'Project Manager',
    'Product Manager': 'Product Manager',
    'Product Owner': 'Product Owner',
    'Delivery Manager': 'Delivery Manager',
    'Scrum Master / Agile Coach': 'Scrum Master',
    'Tech Leadership': 'Lead',
    'DevOps': 'DevOps',
    'Security': 'Security',
    'Sysadmin': 'Sysadmin',
    'Business Analyst': 'Business Analyst',
    'Data Science (ML / AI)': 'ML AI',
    'Web Analyst': 'Web Analyst',
    'Data Analyst': 'Data Analyst',
    'Data Engineer': 'Data Engineer',
    'SQL / DBA': 'SQL',
    'Technical Writing': 'Technical Writing',
    'Marketing': 'Marketing',
    'Sales': 'Sales',
    'Lead Generation': 'Lead Generation',
    'SEO': 'SEO',
    'HR': 'HR',
    'Recruiter': 'Recruiter',
    'Customer/Technical Support': 'Support',
    'Head / Chief': 'Head Chief',
    'Finances': 'Finances',
    '(Other)': 'Other'
}

SUBCATEGORIES = {
    'JavaScript': {
        'Angular': 'Angular',
        'React.js': 'React.js',
        'Svelte': 'Svelte',
        'Vue.js': 'Vue.js',
        'Markup': 'Markup'
    },

    'PHP': {
        'WordPress': 'WordPress',
        'Yii': 'Yii',
        'Drupal': 'Drupal',
        'Laravel': 'Laravel',
        'Magento': 'Magento',
        'Symfony': 'Symfony'
    },

    'C++': {
        'C': 'C Lang',
        'Embedded': 'Embedded',
        'C++': 'CPP'
    },

    'ERP': {
        'MS Dynamics / Business Central': 'MS Dynamics',
        'Odoo': 'Odoo',
        'SAP': 'SAP'
    },

    'Design': {
        'Content Design / UX writer': 'Content Design',
        'Graphic Design': 'Graphic Design',
        'Product Design': 'Product Design',
        'UI/UX': 'UI UX',
        'UX Research': 'UX Research'
    },

    'Artist': {
        '3D Animation': '3D Animation',
        '2D Artist': '2D Artist',
        '3D Artist': '3D Artist',
        'Illustrator': 'Illustrator',
        'Motion Design': 'Motion Design',
        'VFX Artist': 'VFX Artist',
        'Video Editor': 'Video Editor',
        '2D Animation': '2D Animation'
    },

    'Unity': {
        'Game Design': 'Game Design',
        'Game Developer': 'Game Developer',
        'Unreal Developer': 'Unreal Developer',
        'Unity Developer': 'Unity Developer',
        'Level Design': 'Level Design'
    },

    'Lead': {
        'CTO': 'CTO',
        'Software Architect': 'Architect',
        'Engineering Manager': 'Engineering Manager'
    },

    'Security': {
        'Information Security': 'Information Security',
        'Security Analyst': 'Security Analyst',
        'Penetration Tester': 'Penetration Tester'
    },

    'Marketing': {
        'Affiliate Manager': 'Affiliate Manager',
        'Media Buying': 'Media Buying',
        'PPC': 'PPC',
        'Content Writer / Copywriter / Editor': 'Content Marketing',
        'Marketing Analyst': 'Marketing Analyst',
        'Social Media': 'Social Media',
        'PR Manager': 'PR Manager'
    },

    'Head Chief': {
        'Chief Executive Officer (CEO)': 'CEO',
        'Chief Financial Officer (CFO)': 'CFO',
        'Chief Information Officer (CIO)': 'CIO',
        'Chief Operating Officer (COO)': 'COO',
        'Chief Product Officer (CPO)': 'CPO',
        'Chief Security Officer (CSO)': 'CSO',
        'Chief Marketing Officer (CMO)': 'CMO',
        'Chief Business Development Officer (CBDO)': 'CBDO',
        'Chief Commercial Officer (CCO)': 'CCO'
    }
}

EU_COUNTRY_CODES = (
    'AUT', 'BEL', 'BGR', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'IRL', 'ITA',
    'LVA', 'LTU', 'LUX', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP', 'SWE'
)


class Country(models.TextChoices):
    UKRAINE = 'UKR', _('Ukraine')
    POLAND = 'POL', _('Poland')
    GERMANY = 'DEU', _('Germany')
    SPAIN = 'ESP', _('Spain')
    PORTUGAL = 'PRT', _('Portugal')
    AZERBAIJAN = 'AZE', _('Azerbaijan')
    EUROPE = 'EU', _('Europe countries')


class Order(models.TextChoices):
    PUBLISHED_NEW_TO_OLD = '-published', _('Published (new to old)')
    PUBLISHED_OLD_TO_NEW = 'published', _('Published (old to new)')
    APPLICATIONS_HIGH_TO_LOW = '-applications_count', _('Number of applications (highest to lowest)')
    APPLICATIONS_LOW_TO_HIGH = 'applications_count', _('Number of applications (lowest to highest)')


class Experience(models.TextChoices):
        ZERO = '0y', _('No experience')
        ONE = '1y', _('1 year')
        TWO = '2y', _('2 years')
        THREE = '3y', _('3 years')
        FOUR = '4y', _('4 years')
        FIVE = '5y', _('5 years')
        SIX = '6y', _('6 years')
        SEVEN = '7y', _('7 years')
        EIGHT = '8y', _('8 years')
        NINE = '9y', _('9 years')
        TEN = '10y', _('10 years')


class RemoteType(models.TextChoices):
    OFFICE = "office", _("Office")
    PARTLY_REMOTE = "partly_remote", _("Hybrid")
    FULL_REMOTE = "full_remote", _("Remote")
    CANDIDATE_CHOICE = "candidate_choice", _("Office/Remote of your choice")


class RelocateType(models.TextChoices):
    NO_RELOCATE = "no_relocate", _("No relocation")
    CANDIDATE_PAID = "candidate_paid", _("Covered by candidate")
    COMPANY_PAID = "company_paid", _("Covered by company")


class Location(models.TextChoices):
    """
        Перелік міст, які можна вибрати в вакансіях було вирішено захардкодити таким чином, оскільки в БД вони
        зберігаютсья російською і присутні тільки ці міста. Також в БД є запис, де 'location' - Kyiv, але оскільки
        всі інші міста уніфіковані та зберігаються російською, то було вирішено захардкодити міста в такому вигляді
        скіпнувши даний кейс.

        Вибір унікальних міст з БД та їх динамічний переклад сповільнює перфоманс сайту, тому такий варіант не було
        використано.

        Також є варіант з тим, щоб звести всі міста до однієї мови запитом в БД, але я не маю повного бачення як саме
        задаються/обираються міста при створенні вакансії, тому вирішив залишити так, як є.
    """
    KYIV = 'Киев', _('Kyiv')
    LVIV = 'Львов', _('Lviv')
    KHARKIV = 'Харьков', _('Kharkiv')
    DNIPRO = 'Днепр', _('Dnipro')
    IVANO_FRANKIVSK = 'Ивано-Франковск', _('Ivano-Frankivsk')
    VINNYTSIA = 'Винница', _('Vinnytsia')
    ODESA = 'Одесса', _('Odesa')
    KHMELNYTSKYI = 'Хмельницкий', _('Khmelnytskyi')
    UZHHOROD = 'Ужгород', _('Uzhhorod')
    ZAPORIZHZHIA = 'Запорожье', _('Zaporizhzhia')
    CHERNIVTSI = 'Черновцы', _('Chernivtsi')
    CHERKASY = 'Черкассы', _('Cherkasy')
    MYKOLAIV = 'Николаев', _('Mykolaiv')
    CHERNIHIV = 'Чернигов', _('Chernihiv')
    ZHYTOMYR = 'Житомир', _('Zhytomyr')
    TERNOPIL = 'Тернополь', _('Ternopil')


LOCATION_CHOICES = {str(choices[0]): str(choices[1]) for choices in Location.choices}


class AcceptRegion(models.TextChoices):
    OFFICE_LOCATIONS = "office_locations", _("Office locations")
    WORLDWIDE = "", _("Worldwide")
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
    search_count = models.IntegerField(blank=False, default=0)  # unused, how many candidates for this job
    views_count = models.IntegerField(blank=False, default=0)
    applications_count = models.IntegerField(blank=False, default=0)
    sent_count = models.IntegerField(blank=False, default=0)

    recruiter = models.ForeignKey('Recruiter', on_delete=models.CASCADE, blank=True, null=True, db_index=True)
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
