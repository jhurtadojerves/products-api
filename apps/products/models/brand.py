from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """
        Return a string representation of the Brand instance.

        This method returns the name of the brand, which is useful for
        displaying the brand in the Django admin or other interfaces.

        Returns:
            str: The name of the brand.
        """
        return self.name
