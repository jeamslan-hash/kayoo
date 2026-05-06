from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Property(models.Model):
    TRANSACTION_CHOICES = [
        ("vente", "À vendre"),
        ("location", "À louer"),
    ]

    STATUS_CHOICES = [
        ("disponible", "Disponible"),
        ("vendu", "Vendu"),
        ("loue", "Loué"),
        ("reserve", "Réservé"),
    ]

    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="properties",
        verbose_name="Catégorie"
    )

    transaction_type = models.CharField(
        "Type de transaction",
        max_length=20,
        choices=TRANSACTION_CHOICES,
        default="vente"
    )

    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default="disponible"
    )

    price = models.DecimalField("Prix", max_digits=12, decimal_places=2)
    currency = models.CharField("Devise", max_length=10, default="USD")

    city = models.CharField("Ville", max_length=100)
    address = models.CharField("Adresse", max_length=255, blank=True)

    area = models.DecimalField("Surface", max_digits=10, decimal_places=2, null=True, blank=True)
    area_unit = models.CharField("Unité surface", max_length=20, default="m²")

    bedrooms = models.PositiveIntegerField("Chambres", null=True, blank=True)
    bathrooms = models.PositiveIntegerField("Toilettes / salles de bain", null=True, blank=True)
    floors = models.PositiveIntegerField("Niveaux", null=True, blank=True)

    short_description = models.TextField("Description courte")
    full_description = models.TextField("Description complète", blank=True)

    has_water = models.BooleanField("Eau disponible", default=False)
    has_electricity = models.BooleanField("Électricité disponible", default=False)
    has_parking = models.BooleanField("Parking", default=False)
    has_garden = models.BooleanField("Jardin", default=False)
    has_pool = models.BooleanField("Piscine", default=False)

    is_featured = models.BooleanField("Mettre en avant", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bien immobilier"
        verbose_name_plural = "Biens immobiliers"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Property.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Bien immobilier"
    )
    image = models.ImageField("Image", upload_to="properties/")
    caption = models.CharField("Légende", max_length=150, blank=True)
    is_main = models.BooleanField("Image principale", default=False)

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    def __str__(self):
        return f"Photo de {self.property.title}"