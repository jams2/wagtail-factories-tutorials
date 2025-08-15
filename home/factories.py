# [[file:../docs/tutorials/working-with-blocks.org::*Prerequisites from getting-started tutorial][Prerequisites from getting-started tutorial:4]]
import factory
from wagtail_factories import PageFactory

from home.models import HomePage


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage


# Prerequisites from getting-started tutorial:4 ends here

# [[file:../docs/tutorials/working-with-blocks.org::*Prerequisites from getting-started tutorial][Prerequisites from getting-started tutorial:5]]
from wagtail_factories import DocumentFactory, ImageFactory

from home.models import BlogPage


class BlogPageFactory(PageFactory):
    hero_image = factory.SubFactory(ImageFactory)
    splash_text = factory.Faker("paragraph")
    related_page = factory.SubFactory(PageFactory)
    policy = factory.SubFactory(DocumentFactory)

    class Meta:
        model = BlogPage


# Prerequisites from getting-started tutorial:5 ends here
