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

# [[file:../docs/tutorials/working-with-blocks.org::*Factories for struct blocks][Factories for struct blocks:1]]
import factory
from wagtail_factories import StructBlockFactory

from home.blocks import ScheduledFeedingBlock


class ScheduledFeedingBlockFactory(StructBlockFactory):
    time = factory.Faker("time_object")
    portions = factory.Faker("random_int", min=1, max=100)
    food = factory.Faker(
        "random_element", elements=["kibble", "tuna", "salmon", "carrots"]
    )

    class Meta:
        model = ScheduledFeedingBlock


# Factories for struct blocks:1 ends here

# [[file:../docs/tutorials/working-with-blocks.org::*Stream block factories][Stream block factories:2]]
import factory
from wagtail_factories import ImageBlockFactory, StreamBlockFactory

from home.blocks import PetStoryBlock


class PetStoryBlockFactory(StreamBlockFactory):
    image = factory.SubFactory(ImageBlockFactory)
    text = factory.Faker("sentence")
    link = factory.Faker("uri")

    class Meta:
        model = PetStoryBlock


# Stream block factories:2 ends here

# [[file:../docs/tutorials/working-with-blocks.org::*Factories for list blocks][Factories for list blocks:1]]
from wagtail_factories import (
    ListBlockFactory,
    PageFactory,
    StreamFieldFactory,
)

from home.blocks import PetBlock, get_colour_choices


class PetBlockFactory(StructBlockFactory):
    story = StreamFieldFactory(PetStoryBlockFactory)
    name = factory.Faker("name")
    date_of_birth = factory.Faker("date_object")
    feeding_schedule = ListBlockFactory(ScheduledFeedingBlockFactory)
    colour = factory.Faker(
        "random_element", elements=[x[0] for x in get_colour_choices()]
    )
    picture = factory.SubFactory(ImageBlockFactory)

    class Meta:
        model = PetBlock


# Factories for list blocks:1 ends here

# [[file:../docs/tutorials/working-with-blocks.org::*Tying it all together][Tying it all together:1]]
from home.blocks import CatBlock, DogBlock


class CatBlockFactory(PetBlockFactory):
    class Meta:
        model = CatBlock


class DogBlockFactory(PetBlockFactory):
    class Meta:
        model = DogBlock


# Tying it all together:1 ends here

# [[file:../docs/tutorials/working-with-blocks.org::*Tying it all together][Tying it all together:2]]
from home.blocks import PetsBlock


class PetsBlockFactory(StreamBlockFactory):
    cat = factory.SubFactory(CatBlockFactory)
    dog = factory.SubFactory(DogBlockFactory)

    class Meta:
        model = PetsBlock


# Tying it all together:2 ends here

# [[file:../docs/tutorials/working-with-blocks.org::*Tying it all together][Tying it all together:3]]
from wagtail_factories import (
    PageFactory,
    StreamFieldFactory,
)

from home.models import PetPage


class PetPageFactory(PageFactory):
    pets = StreamFieldFactory(PetsBlockFactory)

    class Meta:
        model = PetPage


# Tying it all together:3 ends here
