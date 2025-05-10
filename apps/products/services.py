import datetime
from typing import TypeAlias

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from user_agents import parse

from apps.products.models.product import Product
from apps.products.tasks import send_product_update_email

UserType: TypeAlias = AbstractBaseUser
User = get_user_model()


class ProductVisitMetadataBuilder:
    """
    Service class for building metadata related to product visits.

    This class extracts metadata from the request, such as IP address,
    user agent, device type, and other relevant information.
    """

    def __init__(self, request):
        self.request = request
        self.ua = parse(request.headers.get("User-Agent", ""))

    def build(self) -> dict:
        """
        Build a dictionary containing metadata about the product visit.

        Returns:
            dict: Metadata including IP address, user agent, device type, OS, browser, etc.
        """
        return {
            "ip": self._get_ip(),
            "user_agent": self.request.headers.get("User-Agent", ""),
            "device": self.ua.device.family,
            "device_type": self._get_device_type(),
            "os": self.ua.os.family,
            "browser": self.ua.browser.family,
            "is_mobile": self.ua.is_mobile,
            "is_tablet": self.ua.is_tablet,
            "is_pc": self.ua.is_pc,
            "referer": self.request.headers.get("Referer"),
        }

    def _get_ip(self) -> str:
        """
        Retrieve the IP address from the request.

        Returns:
            str: The IP address of the client making the request.
        """
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()

        return self.request.META.get("REMOTE_ADDR")

    def _get_device_type(self) -> str:
        """
        Determine the type of device based on the user agent.

        Returns:
            str: The type of device (e.g., "mobile", "tablet", "pc", "bot", or "unknown").
        """
        if self.ua.is_mobile:
            return "mobile"
        elif self.ua.is_tablet:
            return "tablet"
        elif self.ua.is_pc:
            return "pc"
        elif self.ua.is_bot:
            return "bot"
        return "unknown"


class ProductEmailService:
    """
    Service class for handling product-related email notifications.

    This class provides methods to build and send email notifications
    when a product is updated.

    Methods:
    - build: Creates the subject and body of the email notification.
    - send_email: Sends the email notification to administrators.
    """

    @classmethod
    def build(cls, product: Product, user: UserType) -> tuple[str, str]:
        """
        Build the subject and body for a product update email.

        Args:
            product (Product): The product that was updated.
            user (UserType): The user who made the update.

        Returns:
            tuple[str, str]: The email subject and body.
        """
        subject = f"[Catálogo] Producto actualizado: {product.name} ({product.sku})"

        body = f"""
            Hola equipo,

            Se ha realizado una modificación en el siguiente producto:

            🏍️ Nombre: {product.name}
            🔖 SKU: {product.sku}
            🏷️ Marca: {product.brand.name}
            💰 Precio actual: ${product.price:.2f}

            Modificado por: {user.email if user else 'Desconocido'}
            Fecha y hora: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

            Si no reconoces esta acción, por favor revisa el historial o contacta al equipo de soporte.

            Saludos,
            Catálogo Automatizado
        """

        return subject, body

    @classmethod
    def send_email(cls, product: Product, user: UserType) -> None:
        """
        Send an email notification about a product update to administrators.

        Args:
            product (Product): The product that was updated.
            user (UserType): The user who made the update.

        Returns:
            None
        """
        admins = User.objects.filter(is_staff=True, is_active=True).exclude(
            email=user.email
        )
        to_emails = [admin.email for admin in admins]

        if to_emails:
            subject, body = cls.build(product=product, user=user)
            send_product_update_email.delay(subject, body, to_emails)
