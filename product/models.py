from django.db import models

class Product(models.Model):
    """
    Represents a product in the system.
    """

    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Product model.
        
        Returns:
            str: The product's name for easy identification in admin and queries.
        """
        return self.name
