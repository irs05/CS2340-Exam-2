from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from movies.models import Movie, Region, MovieRegionStat

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.user.username
    
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

# --- Region key derivation and stat bumping ---
def _derive_region_key(order: 'Order') -> str:
    parts = [p for p in [order.city, order.state, order.country] if p]
    if parts:
        return ", ".join(parts).strip()
    if order.latitude is not None and order.longitude is not None:
        try:
            lat = round(float(order.latitude), 2)
            lon = round(float(order.longitude), 2)
            return f"{lat},{lon}"
        except (TypeError, ValueError):
            pass
    return "Unknown"

@receiver(post_save, sender=Item)
def bump_movie_region_stats_on_item_create(sender, instance: 'Item', created, **kwargs):
    if not created:
        return
    order = instance.order
    region_key = _derive_region_key(order)
    region, _ = Region.objects.get_or_create(name=region_key)
    stat, _ = MovieRegionStat.objects.get_or_create(
        movie=instance.movie,
        region=region,
        defaults={"views": 0},
    )
    # Increment once per quantity (coerce to int safely)
    try:
        qty = int(instance.quantity)
    except (TypeError, ValueError):
        qty = 1
    if qty <= 0:
        qty = 1
    MovieRegionStat.objects.filter(pk=stat.pk).update(views=F('views') + qty)
