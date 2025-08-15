# [[file:../docs/tutorials/getting-started.org::*Page factories][Page factories:1]]
import factory
from wagtail_factories import PageFactory

from home.models import HomePage


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage


# Page factories:1 ends here

# [[file:../docs/tutorials/getting-started.org::*Page factories][Page factories:4]]
from wagtail_factories import DocumentFactory, ImageFactory

from home.models import BlogPage


class BlogPageFactory(PageFactory):
    hero_image = factory.SubFactory(ImageFactory)
    splash_text = factory.Faker("paragraph")
    related_page = factory.SubFactory(PageFactory)
    policy = factory.SubFactory(DocumentFactory)

    class Meta:
        model = BlogPage


# Page factories:4 ends here
