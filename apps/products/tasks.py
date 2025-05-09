from celery import shared_task
from django.conf import settings
from geoip2.database import Reader

from apps.commons.services import EmailService

from .models import Product, ProductRetrieve

DEFAULT_COUNTRY = "México"
DEFAULT_CITY = "Ciudad de México"


@shared_task
def track_product_retrieve(product_id, metadata):
    try:
        product = Product.objects.get(id=product_id)
        reader = Reader(settings.GEOIP_DB_PATH)
        ip = metadata.get("ip")

        try:
            response = reader.city(ip)
            metadata.update(
                {
                    "country": response.country.name or DEFAULT_COUNTRY,
                    "city": response.city.name or DEFAULT_CITY,
                }
            )
        except Exception:
            metadata.update({"country": DEFAULT_COUNTRY, "city": DEFAULT_CITY})

        reader.close()
        ProductRetrieve.objects.create(product=product, metadata=metadata)
    except Product.DoesNotExist:
        pass


@shared_task
def send_product_update_email(subject: str, content: str, to_emails: list[str]):
    EmailService.send_email(subject, content, to_emails)
