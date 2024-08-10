from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from jobs.models import JobPosting


class JobSearchService:
    def __init__(self, query):
        """
        Initializes the JobSearchService object with the provided query.

        Parameters:
            query (str): The search query provided by the user.

        Returns:
            None
        """
        self.query = query
        self.search_vector = (
            SearchVector('position', weight='A') +
            SearchVector('long_description', weight='B') +
            SearchVector('primary_keyword', weight='C') +
            SearchVector('secondary_keyword', weight='C') +
            SearchVector('extra_keywords', weight='D') +
            SearchVector('company__name', weight='A')
        )
        
    def search_jobs(self):
        """
        Searches for jobs based on the provided query.

        This function takes into account various parameters such as search terms, 
        exclude terms, and ranking. It filters jobs based on exact matches, 
        annotates them with a ranking score, and orders them by relevance.

        Parameters:
            self.query (str): The search query provided by the user.

        Returns:
            jobs (QuerySet): A queryset of JobPosting objects that match the search query.
        """
        jobs = JobPosting.objects.all()

        if self.query:
            search_terms, exclude_terms = self.parse_query(self.query)
            search_query = SearchQuery(f"'{search_terms}'", search_type='plain')
            
            exact_match_filter = (
                Q(position__iregex=r'\m' + search_terms + r'\M') |
                Q(long_description__iregex=r'\m' + search_terms + r'\M') |
                Q(primary_keyword__iregex=r'\m' + search_terms + r'\M') |
                Q(secondary_keyword__iregex=r'\m' + search_terms + r'\M') |
                Q(extra_keywords__iregex=r'\m' + search_terms + r'\M') |
                Q(company__name__iregex=r'\m' + search_terms + r'\M')
            )

            jobs = jobs.annotate(
                rank=SearchRank(self.search_vector, search_query)
            ).filter(
                exact_match_filter,
                rank__gt=0
            ).order_by('-rank')

            if exclude_terms:
                exclude_filter = Q()
                for term in exclude_terms:
                    exclude_filter |= (
                        Q(position__icontains=term) |
                        Q(long_description__icontains=term) |
                        Q(primary_keyword__icontains=term) |
                        Q(secondary_keyword__icontains=term) |
                        Q(extra_keywords__icontains=term) |
                        Q(company__name__icontains=term)
                    )
                jobs = jobs.exclude(exclude_filter)
                    
        return jobs

    def parse_query(self, query):
        """
        Parses the search query and separates it into search terms and exclude terms.

        Args:
            query (str): The search query provided by the user.

        Returns:
            tuple: A tuple containing two lists - search_terms and exclude_terms.
                - search_terms (str): The search terms extracted from the query.
                - exclude_terms (list): The exclude terms extracted from the query.

        Example:
            >>> parse_query('python -backend')
            ('python', ['backend'])
        """
        terms = query.split()
        search_terms = ' '.join(term for term in terms if not term.startswith('-'))
        exclude_terms = [term[1:] for term in terms if term.startswith('-')]
        return search_terms, exclude_terms
