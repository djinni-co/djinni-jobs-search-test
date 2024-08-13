from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from jobs.models import JobPosting, EnglishLevel, RemoteType, Experience
import pycountry
from django.views import generic

remote_type_mapping = {value: key for key, value in RemoteType.choices}
english_level_mapping = {value: key for key, value in EnglishLevel.choices}
experience_mapping = {value: key for key, value in Experience.choices}


def jobs_list(request):
    JOBS_PER_PAGE = 20
    jobs = JobPosting.objects.select_related("company", "recruiter")

    primary_keywords = jobs.values("primary_keyword").distinct()
    salary_min = jobs.order_by("salary_min").first().salary_min if jobs.exists() else 0
    salary_max = jobs.order_by("-salary_min").first().salary_max if jobs.exists() else 0
    countries = sorted(
        {
            (
                pycountry.countries.get(alpha_3=j).name
                if pycountry.countries.get(alpha_3=j)
                else j
            )
            for i in jobs.values("country").distinct()
            if i["country"]
            for j in i["country"].split(",")
        }
    )
    cities = []

    if param := request.GET.get("q"):
        param = param.strip()
        jobs = jobs.filter(
            Q(position__icontains=param)
            | Q(long_description__icontains=param)
            | Q(company__name__icontains=param)
        )

    if primary_keyword := request.GET.get("primary_keyword"):
        primary_keyword = primary_keyword.strip()
        jobs = jobs.filter(
            Q(primary_keyword__icontains=primary_keyword)
            | Q(secondary_keyword__icontains=primary_keyword)
            | Q(extra_keywords__icontains=primary_keyword)
        ).distinct()

    if salary_value := request.GET.get("salary_value"):
        jobs = jobs.filter(salary_min__gte=salary_value)

    if remote_type := request.GET.get("remote_type"):
        remote_type_db_value = remote_type_mapping.get(remote_type)
        if remote_type_db_value:
            jobs = jobs.filter(remote_type=remote_type_db_value)

    if country := request.GET.get("country"):
        country = (
            pycountry.countries.get(name=country).alpha_3
            if pycountry.countries.get(name=country)
            else country
        )
        jobs = jobs.filter(country__icontains=country)
        cities = jobs.values("location").distinct()

    if location := request.GET.get("location"):
        jobs = jobs.filter(location__icontains=location)

    if english_level := request.GET.get("english_level"):
        english_level_db_value = english_level_mapping.get(english_level)
        if english_level_db_value:
            index = list(english_level_mapping.values()).index(english_level_db_value)
            levels = list(english_level_mapping.values())[: index + 1]
            jobs = jobs.filter(english_level__in=levels)

    if experience_year := request.GET.get("experience_year"):
        experience_year_db_value = experience_mapping.get(experience_year)
        match experience_year_db_value:
            case "no_exp":
                jobs = jobs.filter(experience_years__lte=0)
            case "10y":
                pass
            case _:
                jobs = jobs.filter(experience_years__lte=int(experience_year_db_value[:-1]))

    paginator = Paginator(jobs, JOBS_PER_PAGE)
    page = request.GET.get("page", 1)

    try:
        job_list = paginator.page(page)
    except PageNotAnInteger:
        job_list = paginator.page(1)
    except EmptyPage:
        job_list = paginator.page(paginator.num_pages)

    context = {
        "jobs": job_list,
        "primary_keywords": {
            primary_keyword.get("primary_keyword")
            for primary_keyword in primary_keywords
        },
        "is_paginated": job_list.has_other_pages(),
        "page_obj": job_list,
        "paginator": paginator,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "remote_types": [remote[1] for remote in RemoteType.choices],
        "counties": countries,
        "cities": sorted(
            {
                city.strip()
                for city_list in cities
                if city_list.get("location")
                for city in city_list.get("location").split(",")
            }
        ),
        "english_levels": [level[1] for level in EnglishLevel.choices],
        "experience_years": [year[1] for year in Experience.choices],
    }

    return render(request, "jobs/list.html", context)


class JobPostingDetailView(generic.DetailView):
    model = JobPosting
