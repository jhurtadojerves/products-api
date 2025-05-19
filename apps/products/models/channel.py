from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """
        Return a string representation of the Channel instance.

        This method returns the name of the channel, which is useful for
        displaying the channel in the Django admin or other interfaces.

        Returns:
            str: The name of the channel.
        """
        return self.name
