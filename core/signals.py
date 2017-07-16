from django.db.models.signals import post_save
from django.dispatch import receiver

from models import UserExtend
from restaurant.models import Restaurant
from foodie.models import Foodie

@receiver(post_save, sender=UserExtend)
def create_foodie(sender, instance, *args, **kwargs):
    if instance.type == 'F':
        # print "Creating Foodie Relationship..."
        Foodie.objects.get_or_create(user_id=instance.id)
    elif instance.type == 'R':
        # print "Creating Restaurant Relationship..."
        username_slug = instance.email + '_' + str(instance.pk)
        UserExtend.objects.filter(pk=instance.pk).update(username=username_slug)
        Restaurant.objects.get_or_create(user_id=instance.id)