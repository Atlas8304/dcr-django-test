import pytest

from countries.models import Region, Country

@pytest.fixture
def create_sample_data():
    # Create 3 regions, 2 with countries, 1 without
    region1 = Region.objects.create(name="Region 1")
    region2 = Region.objects.create(name="Region 2")
    Region.objects.create(name="Region 3")

    # Create countries for the first two regions, one with population None/NULL
    Country.objects.create(name="Country A", population=1000, region=region1)
    Country.objects.create(name="Country B", population=2000, region=region1)
    Country.objects.create(name="Country C", population=0, region=region2)


@pytest.mark.django_db
def test_region_with_country_and_population(client, create_sample_data):
    response = client.get("/countries/stats/")
    assert response.status_code == 200
    data = response.json()

    region1 = next((r for r in data["regions"] if r["name"] == "Region 1"), None)
    assert region1 is not None
    assert region1["number_countries"] == 2
    assert region1["total_population"] == 3000

@pytest.mark.django_db
def test_region_with_country_and_zero_population(client, create_sample_data):
    response = client.get("/countries/stats/")
    assert response.status_code == 200
    data = response.json()

    region2 = next((r for r in data["regions"] if r["name"] == "Region 2"), None)
    assert region2 is not None
    assert region2["number_countries"] == 1
    assert region2["total_population"] == 0

@pytest.mark.django_db
def test_region_with_no_country(client, create_sample_data):
    response = client.get("/countries/stats/")
    assert response.status_code == 200
    data = response.json()

    region3 = next((r for r in data["regions"] if r["name"] == "Region 3"), None)
    assert region3 is not None
    assert region3["number_countries"] == 0
    assert region3["total_population"] == 0