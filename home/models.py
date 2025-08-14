from django.db import models
from wagtail.models import Page


class HomePage(Page):
    pass


class BlogPage(Page):
    hero_image = models.ForeignKey(
        "wagtailimages.image",
        on_delete=models.PROTECT,
        related_name="+",
    )
    splash_text = models.TextField(blank=True)
    related_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="related_pages",
    )
