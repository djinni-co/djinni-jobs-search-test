# Generated by Django 4.2.4 on 2024-08-11 18:00

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations
from django.contrib.postgres.search import SearchVector


def update_search_vector(apps, schema_editor):
    JobPosting = apps.get_model('jobs', 'JobPosting')
    JobPosting.objects.update(search_vector=SearchVector('position', 'long_description', 'primary_keyword', 'secondary_keyword', 'extra_keywords'))


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobposting_search_vector_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF position, long_description, primary_keyword,
            secondary_keyword, extra_keywords
            ON jobs_jobposting
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
            search_vector, 'pg_catalog.english', position, long_description, primary_keyword,
            secondary_keyword, extra_keywords
            );
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON jobs_jobposting;
            """,
        ),
        migrations.RunPython(
            update_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
