# [[file:../docs/tutorials/getting-started.org::*Page models][Page models:1]]
from wagtail.models import Page


class HomePage(Page):
    pass


# Page models:1 ends here

# [[file:../docs/tutorials/getting-started.org::*Page models][Page models:2]]
from django.db import models
from wagtail.documents import get_document_model
from wagtail.images import get_image_model


class BlogPage(Page):
    hero_image = models.ForeignKey(
        get_image_model(),
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
    policy = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )


# Page models:2 ends here
