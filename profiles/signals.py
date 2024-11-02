from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from.models import Profile, Review


@receiver(post_save, sender=Review)
def update_profile_rating_on_save(sender, instance, **kwargs):
    reviewed_profile = Profile.objects.get(user=instance.reviewed)
    reviewed_profile.calculate_rating()


@receiver(post_delete, sender=Review)
def update_profile_rating_on_delete(sender, instance, **kwargs):
    reviewed_profile = Profile.objects.get(user=instance.reviewed)
    reviewed_profile.calculate_rating()
