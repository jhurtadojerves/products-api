from celery import shared_task
from django.conf import settings
from geoip2.database import Reader

from apps.commons.services import EmailService

from .models import Product, ProductRetrieve

DEFAULT_COUNTRY = "México"
DEFAULT_CITY = "Ciudad de México"


@shared_task
def track_product_retrieve(product_id: int, metadata: dict):
    """
    Tracks a product retrieval event and stores metadata.

    This task retrieves a product by its ID, enriches the provided metadata
    with geolocation information based on the client's IP address, and stores
    the data in the `ProductRetrieve` model.

    Args:
        product_id (int): The ID of the product being retrieved.
        metadata (dict): Metadata about the retrieval event, including the client's IP address.

    Returns:
        None
    """
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
    """
    Send an email notification about a product update.

    This task uses the `EmailService` to send an email with the provided
    subject, content, and recipient list.

    Args:
        subject (str): The subject of the email.
        content (str): The body content of the email.
        to_emails (list[str]): A list of recipient email addresses.

    Returns:
        None
    """
    EmailService.send_email(subject, content, to_emails)
