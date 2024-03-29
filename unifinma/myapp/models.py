
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

"""
Models :
Utilisateur : modèle pour les utilisateurs enregistrés, qui contient les informations telles que le nom, le prénom, l'adresse de livraison et l'information bancaire d'achat.
Article : modèle pour les articles disponibles à l'achat, qui contient les informations telles que la couleur, le prix et les tailles disponibles.

"""

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=None )
    prix = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    
    def __str__(self):
        return self.nom


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relation avec la classe User
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.produit.nom} ({self.quantity})"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relation avec la classe User
    orders = models.ManyToManyField(Order)  
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.user.username


    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now() #gmt
            order.save()
                        
        self.orders.clear()
        super().delete(*args, **kwargs)