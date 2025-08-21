import json

from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from django.core.management.base import BaseCommand

from countries.models import Country, Region


class Command(BaseCommand):
    help = "Loads country data from an external JSON file."

    IMPORT_URL = "https://storage.googleapis.com/dcr-django-test/countries.json"

    def get_data(self):
        try:
            with urlopen(self.IMPORT_URL) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            self.stderr.write(
                self.style.ERROR("HTTP Error: {} - {}".format(e.code, e.reason))
            )
        except URLError as e:
            self.stderr.write(self.style.ERROR("URL Error: {}".format(e.reason)))
        return data

    def handle(self, *args, **options):
        data = self.get_data()
        for row in data:
            region, region_created = Region.objects.get_or_create(name=row["region"])
            if region_created:
                self.stdout.write(
                    self.style.SUCCESS("Region: {} - Created".format(region))
                )
            country, country_created = Country.objects.update_or_create(
                name=row["name"],
                defaults={
                    "alpha2Code": row["alpha2Code"],
                    "alpha3Code": row["alpha3Code"],
                    "topLevelDomain": row["topLevelDomain"][0],
                    "population": row["population"],
                    "capital": row["capital"],
                    "region": region,
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "{} - {}".format(
                        country, "Created" if country_created else "Updated"
                    )
                )
            )
