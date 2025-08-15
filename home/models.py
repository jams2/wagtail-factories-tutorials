# [[file:../docs/tutorials/working-with-blocks.org::*Prerequisites from getting-started tutorial][Prerequisites from getting-started tutorial:2]]
from wagtail.models import Page


class HomePage(Page):
    pass


# Prerequisites from getting-started tutorial:2 ends here

# [[file:../docs/tutorials/working-with-blocks.org::*Prerequisites from getting-started tutorial][Prerequisites from getting-started tutorial:3]]
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


# Prerequisites from getting-started tutorial:3 ends here

# [[file:../docs/tutorials/working-with-blocks.org::*Defining stream field blocks][Defining stream field blocks:1]]
from wagtail.fields import StreamField
from wagtail.models import Page

from home.blocks import PetsBlock


class PetPage(Page):
    pets = StreamField(PetsBlock())


# Defining stream field blocks:1 ends here
