import random
from typing import List, Dict, Any
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker in French
fake = Faker('fr_FR')

def generate_firstname() -> str:
    """Generate a random first name."""
    return fake.first_name()

def generate_lastname() -> str:
    """Generate a random last name."""
    return fake.last_name()

def generate_date() -> str:
    """Generate a random date in DD/MM/YYYY format."""
    return fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%d/%m/%Y")

def generate_time() -> str:
    """Generate a random time in HH:MM format."""
    return fake.time(pattern="%H:%M")

def generate_phone() -> str:
    """Generate a random French phone number."""
    phone_type = random.choice(['mobile', 'landline'])
    
    if phone_type == 'mobile':
        prefix = random.choice(['06', '07'])
        return f"{prefix} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"
    else:
        prefix = random.choice(['01', '02', '03', '04', '05'])
        return f"{prefix} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"



def generate_username() -> str:
    """Generate a random username."""
    return fake.user_name()

def generate_gender() -> str:
    """Generate a random gender."""
    genders = ["Homme", "Femme", "Autre", "Non spécifié"]
    return random.choice(genders)

def generate_city() -> str:
    """Generate a random French city."""
    return fake.city()

def generate_state() -> str:
    """Generate a random French region/department."""
    regions = [
        "Île-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes",
        "Nouvelle-Aquitaine", "Occitanie", "Hauts-de-France", "Grand Est",
        "Pays de la Loire", "Bretagne", "Normandie", "Bourgogne-Franche-Comté",
        "Centre-Val de Loire", "Corse"
    ]
    return random.choice(regions)

def generate_url() -> str:
    """Generate a random URL."""
    return fake.url()

def generate_jobarea() -> str:
    """Generate a random job area/field."""
    job_areas = [
        "Informatique", "Finance", "Marketing", "Ressources Humaines", "Vente",
        "Ingénierie", "Santé", "Éducation", "Juridique", "Communication",
        "Logistique", "Production", "Recherche et Développement"
    ]
    return random.choice(job_areas)

def generate_email() -> str:
    """Generate a random email address."""
    return fake.email()

def generate_jobtype() -> str:
    """Generate a random job type."""
    job_types = [
        "CDI", "CDD", "Stage", "Freelance", "Intérim", "Apprentissage",
        "Temps partiel", "Temps plein", "Télétravail"
    ]
    return random.choice(job_types)

def generate_companyname() -> str:
    """Generate a random company name."""
    return fake.company()

def generate_jobtitle() -> str:
    """Generate a random job title."""
    return fake.job()

def generate_street() -> str:
    """Generate a random street address."""
    return fake.street_address()

def generate_county() -> str:
    """Generate a random French department (county)."""
    departments = [
        "Paris", "Seine-et-Marne", "Yvelines", "Essonne", "Hauts-de-Seine",
        "Seine-Saint-Denis", "Val-de-Marne", "Val-d'Oise", "Nord", "Pas-de-Calais",
        "Bouches-du-Rhône", "Rhône", "Gironde", "Loire-Atlantique", "Haute-Garonne"
    ]
    return random.choice(departments)

def generate_age() -> str:
    """Generate a random age."""
    return str(random.randint(18, 99))

def generate_accountname() -> str:
    """Generate a random account name."""
    return f"{fake.first_name().lower()}.{fake.last_name().lower()}"

def generate_accountnumber() -> str:
    """Generate a random account number."""
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

def generate_password() -> str:
    """Generate a random password."""
    return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

def generate_iban() -> str:
    """Generate a random French IBAN."""
    return fake.iban()



PII_GENERATORS: Dict[str, callable] = {
    "FIRSTNAME": generate_firstname,
    "LASTNAME": generate_lastname,
    "DATE": generate_date,
    "TIME": generate_time,
    "PHONE": generate_phone,
    "USERNAME": generate_username,
    "GENDER": generate_gender,
    "CITY": generate_city,
    "STATE": generate_state,
    "URL": generate_url,
    "JOBAREA": generate_jobarea,
    "EMAIL": generate_email,
    "JOBTYPE": generate_jobtype,
    "COMPANYNAME": generate_companyname,
    "JOBTITLE": generate_jobtitle,
    "STREET": generate_street,
    "COUNTY": generate_county,
    "AGE": generate_age,
    "ACCOUNTNAME": generate_accountname,
    "ACCOUNTNUMBER": generate_accountnumber,
    "PASSWORD": generate_password,
    "IBAN": generate_iban,
}

def generate_random_pii(pii_type: str) -> str:
    """
    Generate a random value for a given PII type.
    """
    if pii_type not in PII_GENERATORS:
        raise ValueError(f"Unsupported PII type: {pii_type}. Supported types: {list(PII_GENERATORS.keys())}")
    
    return PII_GENERATORS[pii_type]()

def generate_multiple_pii(pii_types: List[str], count_per_type: int = 1) -> Dict[str, List[str]]:
    """
    Generate multiple PII values for given types.
    """
    result = {}
    for pii_type in pii_types:
        result[pii_type] = [generate_random_pii(pii_type) for _ in range(count_per_type)]
    
    return result

def get_available_pii_types() -> List[str]:
    """Return a list of all available PII types."""
    return list(PII_GENERATORS.keys())

if __name__ == "__main__":
    print("Testing PII generators:")
    print("=" * 50)
    
    for pii_type in get_available_pii_types():
        try:
            value = generate_random_pii(pii_type)
            print(f"{pii_type:15}: {value}")
        except Exception as e:
            print(f"{pii_type:15}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print("Testing multiple PII generation:")
    test_types = ["FIRSTNAME", "LASTNAME", "EMAIL", "PHONE"]
    result = generate_multiple_pii(test_types, count_per_type=2)
    for pii_type, values in result.items():
        print(f"{pii_type}: {values}") 