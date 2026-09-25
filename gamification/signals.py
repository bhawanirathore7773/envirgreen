from django.db.models.signals import post_save
from django.dispatch import receiver

from trees.models import TreeVerification
from campaigns.models import CampaignMember
from . import rules


@receiver(post_save, sender=TreeVerification)
def on_tree_verification(sender, instance, created, **kwargs):
    if created and instance.tree.planter_id:
        rules.check_first_tree(instance.tree.planter)


@receiver(post_save, sender=CampaignMember)
def on_campaign_join(sender, instance, created, **kwargs):
    if created:
        rules.check_clean_start(instance.user)
