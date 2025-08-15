======================================
Getting started with wagtail-factories
======================================

    :Author: Joshua Munn


Goals
-----

In this tutorial, you will learn how to use the wagtail-factories library to create `factory boy <https://factoryboy.readthedocs.io/en/stable/>`_ factories for a Wagtail project. These factories facilitate the easy creation of model instances, which is particularly useful for tests.

We'll learn about factories for Wagtail's models - factories for stream field blocks will be covered in another document.

We assume working familiarity with Wagtail, and a passing familiarity with factory boy.

Page models
-----------

To get started, we'll create some basic page models. Wagtail gives us a ``HomePage`` model by default - we'll keep that.

.. code:: python

    from wagtail.models import Page


    class HomePage(Page):
        pass

Add a ``BlogPage`` type with an ``ImageField``, a ``TextField``, and a foreign key to Wagtail's ``Page`` model.

.. code:: python

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

Create and run the migrations.

.. code:: bash

    uv run python manage.py makemigrations --noinput --no-color
    uv run python manage.py migrate --noinput --no-color

With some models created, we are ready to create the corresponding factory classes.

Page factories
--------------

First, we'll create a factory for the ``HomePage`` type.

.. code:: python

    import factory
    from wagtail_factories import PageFactory

    from home.models import HomePage


    class HomePageFactory(PageFactory):
        class Meta:
            model = HomePage

This one's simple. We can use it to create ``HomePage`` instances:

.. code:: python

    HomePageFactory(title="My temporary home page")

::

    <HomePage: My temporary home page>


Let's create ``BlogPageFactory`` with some more declarations.

.. code:: python

    from wagtail_factories import DocumentFactory, ImageFactory

    from home.models import BlogPage


    class BlogPageFactory(PageFactory):
        hero_image = factory.SubFactory(ImageFactory)
        splash_text = factory.Faker("paragraph")
        related_page = factory.SubFactory(PageFactory)
        policy = factory.SubFactory(DocumentFactory)

        class Meta:
            model = BlogPage

First, let's generate an instance without any specific parameters.

.. code:: python

    blog_page = BlogPageFactory()

    blog_page

::

    <BlogPage: Test page>


A title has been generated

.. code:: python

    blog_page.title

::

    'Test page'


As has an image...

.. code:: python

    blog_page.hero_image.file

::

    <WagtailImageFieldFile: original_images/example_m1sHYJn.jpg>


...a document...

.. code:: python

    blog_page.policy.file

::

    <FieldFile: documents/example_BcceLrr.dat>


...and text.

.. code:: python

    blog_page.splash_text

::

    ('Type first street surface foot yes. Source national new window improve '
     'church. Just executive forget company almost get some.')


A related page was also generated: we can inspect its attributes.

.. code:: python

    blog_page.related_page.pk

::

    49

More control
------------

``PageFactory`` subclasses are ultimately ``factory.django.DjangoModelFactory`` subclasses. This means that factory boy's full feature set is available to us, so we can specify the values of our instances, even spanning relationships.


.. code:: python

    blog_2 = BlogPageFactory(
        title="My new blog",
        related_page__title="Closely related page",
        splash_text=factory.LazyAttribute(lambda o: f"{o.related_page.title} is closely related"),
    )

    blog_2.splash_text

::

    'Closely related page is closely related'


See the `factory boy docs <https://factoryboy.readthedocs.io/en/stable/index.html>`_ for all the details.

The page tree
~~~~~~~~~~~~~
