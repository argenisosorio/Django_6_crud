from django.db import models
from apps.product.models import Product

class Person(models.Model):
    """
    Represents a person in the system.
    
    This model stores basic information about individuals including their name,
    email, age, and timestamps for record creation and updates.
    """

    # Personal Information Fields
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    
    # Relationship: Many-to-One
    # Una persona puede estar relacionada a 1 producto y un producto puede estar relacionado a muchas personas.
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='people')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Person model.
        
        Returns:
            str: The person's name for easy identification in admin and queries.
        """
        return self.name