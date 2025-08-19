===================
Working with blocks
===================

    :Author: Joshua Munn


Goals
-----

Wagtail's killer feature is the `stream field system for flexible content <https://docs.wagtail.org/en/stable/topics/streamfield.html>`_. In this tutorial we will learn how to create and use factory classes that enable us to generate content for stream field blocks, just like we would with factories for Django models.

We assume a working knowledge of Wagtail and a passing knowledge of `factory boy <https://factoryboy.readthedocs.io/en/stable/>`_. This tutorial also assumes you've read `the getting started tutorial <getting-started.rst>`_, and have a Wagtail project with the structures, models, and factories as defined there.

Defining stream field blocks
----------------------------

Before creating any factories, we will create a Django model with a stream field and a set of blocks that define its content model. Create the following model for a fictional animal charity in ``home/models.py``.

.. code:: python

    from wagtail.fields import StreamField
    from wagtail.models import Page

    from home.blocks import PetsBlock


    class PetPage(Page):
        pets = StreamField(PetsBlock())

We need to define ``PetsBlock``, so create it in ``home/blocks.py``.

.. code:: python

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


    class PetStoryBlock(blocks.StreamBlock):
        text = blocks.TextBlock()
        link = blocks.URLBlock()
        image = ImageBlock()


    class PetBlock(blocks.StructBlock):
        story = PetStoryBlock()
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

The block definition contains a variety of structures:

- stream blocks (``PetsBlock``, ``PetBlock.story``);

- a list block;

- struct blocks;

- image blocks;

- choice blocks; and

- various atomic block types.

Create and run the migrations.

.. code:: bash

    uv run python manage.py makemigrations --noinput --no-color
    uv run python manage.py migrate --noinput --no-color

Block factories
---------------

With our model and block definitions in place, it's time to create our block factories. wagtail-factories provides us with the following tools:

- ``StreamBlockFactory``;

- ``StreamFieldFactory``;

- ``ListBlockFactory``;

- ``StructBlockFactory``;

- ``PageChooserBlockFactory``;

- ``ImageChooserBlockFactory``;

- ``DocumentChooserBlockFactory``;

- ``ImageBlockFactory``; and

- some factories atomic block types, although as we'll see they aren't as essential as the factories for compound block types.

We'll start with the bottom of the tree, a factory for ``ScheduledFeedingBlock``.

Factories for struct blocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the following code to ``home/factories.py``.

.. code:: python

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

We have:

- created a ``StructBlockFactory`` subclass for our ``StructBlock`` subclass;

- added a field for each field on the block definition; and

- added an inner ``Meta`` class with a ``model`` attribute which is the corresponding block class.

The ``Meta.model`` declaration is essential: wagtail-factories needs this to create values of the correct type. It should be the relevant block class.

In this example, we're using the API exposed by ``factory.Faker``. This helps us to generate reasonable-looking defaults for fields we don't specify explicit values for when creating block instances.

.. code:: python

    import home.factories as f


    f.ScheduledFeedingBlockFactory()

::

    StructValue([('time', datetime.time(17, 33, 0, 263039)),
                 ('portions', 53),
                 ('food', 'salmon')])


We can also specify values for some or all of the fields.

.. code:: python

    f.ScheduledFeedingBlockFactory(
        portions=3,
        food="kibble",
    )

::

    StructValue([('time', datetime.time(5, 25, 22, 876678)),
                 ('portions', 3),
                 ('food', 'kibble')])

Stream block factories
~~~~~~~~~~~~~~~~~~~~~~

Looking back at the definition of ``PetBlock``, we can see that it contains a stream block definition.

.. code:: python

    class PetStoryBlock(blocks.StreamBlock):
        text = blocks.TextBlock()
        link = blocks.URLBlock()
        image = ImageBlock()


    class PetBlock(blocks.StructBlock):
        ...
        story = PetStoryBlock()
        ...

Create a factory for ``PetStoryBlock`` in ``home/factories.py``. We'll use faker instances for the atomic fields, and a ``SubFactory`` for the nested ``ImageBlock``.

.. code:: python

    import factory
    from wagtail_factories import ImageBlockFactory, StreamBlockFactory

    from home.blocks import PetStoryBlock


    class PetStoryBlockFactory(StreamBlockFactory):
        image = factory.SubFactory(ImageBlockFactory)
        text = factory.Faker("sentence")
        link = factory.Faker("uri")

        class Meta:
            model = PetStoryBlock

Again, note the inner ``Meta`` class with ``model`` definition - this is required.

Using a stream block factory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's try using our new stream block value to generate a value.

.. code:: python

    import home.factories as f


    f.PetStoryBlockFactory()

::

    <StreamValue []>


With no parameters, an empty ``StreamValue`` is generated.

Given that a ``StreamValue`` is an ordered sequence type, how do we specify values for its elements? wagtail-factories supports a syntax for declaring parameters that includes indices for list block and stream block factories. That syntax comes in two flavours:

1. a "default value" flavour; and

2. a "specified value" flavour.

The default value flavour looks like this:

::

    <index>=<block name string>

So, to create an instance of ``PetStoryBlock`` where the first element is a text block, we would do the following:

.. code:: python

    f.PetStoryBlockFactory(**{"0": "text"})

::

    <StreamValue [<block text: 'That notice short tell support very inside.'>]>


Ideally, we wouldn't need the dict-unpacking to insert the keyword-argument parameters, but Python identifiers cannot begin with a numeric character. This will not be an issue when used in the context of a page (or other containing model), as you'll see in later examples.

The syntax for the "specified value" flavour looks like this:

::

    <index>\_\_<block name>=<value>

For example:

.. code:: python

    f.PetStoryBlockFactory(**{"0__text": "hello"})

::

    <StreamValue [<block text: 'hello'>]>


We can combine these two syntaxes arbitrarily, and create streams with multiple elements:

.. code:: python

    f.PetStoryBlockFactory(**{"0__text": "hello", "1": "link", "2": "text"})

::

    <StreamValue [<block text: 'hello'>, <block link: 'https://porter.com/tags/mainregister.htm'>, <block text: 'A research marriage score strategy eye though finally.'>]>


However, indices *must* start at zero, and *must* be sequential.

.. code:: python

    f.PetStoryBlockFactory(**{"0": "link", "7": "link"})

::

    wagtail\ :sub:`factories.builder.InvalidDeclaration`\:
      Parameters for <PetStoryBlockFactory for <class 'home.blocks.PetStoryBlock'>>
      missing required index 1

We can also use double-underscores to traverse the block definition tree, and specify values for nested compound blocks, such as the image block option in ``PetStoryBlock``.

.. code:: python

    with_image = f.PetStoryBlockFactory(**{"0__image__decorative": True})
    with_image[0].value.decorative

To specify multiple values for a particular nested block, we can add declarations with the same ``<index>__<block_name>`` prefix.

.. code:: python

    with_image = f.PetStoryBlockFactory(
        **{
            "0__image__decorative": False,
            "0__image__alt_text": "An orange cat lying in the sun",
        }
    )

    with_image[0].value.decorative, with_image[0].value.contextual_alt_text

Tying it all together
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from wagtail_factories import (
        CharBlockFactory,
        ListBlockFactory,
        PageFactory,
        StreamFieldFactory,
    )
    from home.blocks import PetBlock, get_colour_choices, CatBlock, DogBlock, PetsBlock
    from home.models import PetPage


    class PetBlockFactory(StructBlockFactory):
        story = factory.SubFactory(PetStoryBlockFactory)
        name = factory.Faker("name")
        date_of_birth = factory.Faker("date_object")
        feeding_schedule = ListBlockFactory(ScheduledFeedingBlockFactory)
        colour = factory.Faker(
            "random_element", elements=[x[0] for x in get_colour_choices()]
        )
        picture = factory.SubFactory(ImageBlockFactory)

        class Meta:
            model = PetBlock


    class CatBlockFactory(PetBlockFactory):
        class Meta:
            model = CatBlock


    class DogBlockFactory(PetBlockFactory):
        class Meta:
            model = DogBlock


    class PetsBlockFactory(StreamBlockFactory):
        cat = factory.SubFactory(CatBlockFactory)
        dog = factory.SubFactory(DogBlockFactory)

        class Meta:
            model = PetsBlock


    class PetPageFactory(PageFactory):
        pets = StreamFieldFactory(PetsBlockFactory)

        class Meta:
            model = PetPage
