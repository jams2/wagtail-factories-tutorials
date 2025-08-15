# [[file:../docs/tutorials/working-with-blocks.org::*Defining stream field blocks][Defining stream field blocks:2]]
from wagtail import blocks
from wagtail.images.blocks import ImageBlock


def get_colour_choices():
    return [
        ("calico", "Calico"),
        ("tabby", "Tabby"),
        ("orange", "Orange"),
    ]


class ScheduledFeedingBlock(blocks.StructBlock):
    time = blocks.TimeBlock()
    portions = blocks.IntegerBlock()
    food = blocks.CharBlock()


class PetBlock(blocks.StructBlock):
    story = blocks.StreamBlock(
        [
            ("text", blocks.TextBlock()),
            ("link", blocks.URLBlock()),
            ("image", ImageBlock()),
        ]
    )
    name = blocks.CharBlock()
    date_of_birth = blocks.DateBlock()
    feeding_schedule = blocks.ListBlock(ScheduledFeedingBlock())
    colour = blocks.ChoiceBlock(choices=get_colour_choices)
    picture = ImageBlock()


class CatBlock(PetBlock):
    pass


class DogBlock(PetBlock):
    pass


class PetsBlock(blocks.StreamBlock):
    cat = CatBlock()
    dog = DogBlock()


# Defining stream field blocks:2 ends here
