import os
import django

# Setup django environment if run directly
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartReport.settings")
    django.setup()

from apps.regions.models import Province, District

NEPAL_REGIONS = [
    {
        "name": "Koshi",
        "code": "P1",
        "districts": [
            "Bhojpur", "Dhankuta", "Ilam", "Jhapa", "Khotang", "Morang", 
            "Okhaldhunga", "Panchthar", "Sankhuwasabha", "Solukhumbu", 
            "Sunsari", "Taplejung", "Terhathum", "Udayapur"
        ]
    },
    {
        "name": "Madhesh",
        "code": "P2",
        "districts": [
            "Bara", "Dhanusha", "Mahottari", "Parsa", "Rautahat", 
            "Saptari", "Sarlahi", "Siraha"
        ]
    },
    {
        "name": "Bagmati",
        "code": "P3",
        "districts": [
            "Bhaktapur", "Chitwan", "Dhading", "Dolakha", "Kathmandu", 
            "Kavrepalanchok", "Lalitpur", "Makwanpur", "Nuwakot", 
            "Ramechhap", "Rasuwa", "Sindhuli", "Sindhupalchok"
        ]
    },
    {
        "name": "Gandaki",
        "code": "P4",
        "districts": [
            "Baglung", "Gorkha", "Kaski", "Lamjung", "Manang", 
            "Mustang", "Myagdi", "Nawalpur", "Parbat", "Syangja", "Tanahun"
        ]
    },
    {
        "name": "Lumbini",
        "code": "P5",
        "districts": [
            "Arghakhanchi", "Banke", "Bardiya", "Dang", "Eastern Rukum", 
            "Gulmi", "Kapilvastu", "Parasi", "Palpa", "Pyuthan", 
            "Rolpa", "Rupandehi"
        ]
    },
    {
        "name": "Karnali",
        "code": "P6",
        "districts": [
            "Dailekh", "Dolpa", "Humla", "Jajarkot", "Jumla", 
            "Kalikot", "Mugu", "Salyan", "Surkhet", "Western Rukum"
        ]
    },
    {
        "name": "Sudurpashchim",
        "code": "P7",
        "districts": [
            "Achham", "Baitadi", "Bajhang", "Bajura", "Dadeldhura", 
            "Darchula", "Doti", "Kailali", "Kanchanpur"
        ]
    }
]

def run():
    print("Starting region seed script...")
    total_districts_created = 0

    for province_data in NEPAL_REGIONS:
        province_name = province_data["name"]
        province_code = province_data["code"]
        districts = province_data["districts"]

        province, created = Province.objects.get_or_create(
            code=province_code,
            defaults={"name": province_name}
        )
        if not created and province.name != province_name:
            province.name = province_name
            province.save()

        districts_created = 0
        for i, district_name in enumerate(districts, 1):
            district_code = f"{province_code}-D{str(i).zfill(2)}"
            district, d_created = District.objects.get_or_create(
                name=district_name,
                province=province,
                defaults={"code": district_code}
            )
            if d_created:
                districts_created += 1

        total_districts_created += districts_created
        status_str = "Created" if created else "Updated/Skipped"
        print(f"Province '{province_name}' ({province_code}): {status_str} - Seeded {len(districts)} districts.")

    print(f"\nSeed process completed successfully!")
    print(f"Total new districts created: {total_districts_created}")
    print(f"Total provinces in DB: {Province.objects.count()}")
    print(f"Total districts in DB: {District.objects.count()}")

if __name__ == "__main__":
    run()
