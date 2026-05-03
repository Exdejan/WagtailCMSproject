from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page


class ProfileQuickLinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    description = blocks.TextBlock(required=False)

    class Meta:
        icon = "link"
        label = "Quick link"


class ProfileSectionItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    subtitle = blocks.CharBlock(required=False, max_length=255)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "image"
        label = "Section item"


class ProfileSectionBlock(blocks.StructBlock):
    section_id = blocks.CharBlock(required=True, max_length=100, help_text="Anchor id like hobbies, games, food")
    section_title = blocks.CharBlock(required=True, max_length=255)
    section_description = blocks.TextBlock(required=False)
    items = blocks.ListBlock(ProfileSectionItemBlock())

    class Meta:
        icon = "list-ul"
        label = "Profile section"


class HeroPolaroidBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "image"
        label = "Hero polaroid"


class HomePage(Page):
    template = "home/home_page.html"
    subtitle = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    # Only allow profile pages as children
    subpage_types = ['home.EdrianeProfilePage']

    def get_context(self, request):
        context = super().get_context(request)
        context['profile_pages'] = self.get_children().live().specific()
        return context

    class Meta:
        verbose_name = "Home Page"


class EdrianeProfilePage(Page):
    template = "home/profile_page.html"

    profile_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    hero_polaroids = StreamField([
        ("polaroid", HeroPolaroidBlock())
    ], blank=True, use_json_field=True)

    intro_text = RichTextField(blank=True)
    hero_micro_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_cta_text = models.CharField(max_length=255, blank=True)
    hero_cta_anchor = models.CharField(max_length=255, blank=True)
    bio = RichTextField(blank=True)
    hobbies_title = models.CharField(max_length=255, blank=True)
    hobbies_description = RichTextField(blank=True)
    hobbies_cards = StreamField([
        ("card", ProfileSectionItemBlock())
    ], blank=True, use_json_field=True)
    about_heading = models.CharField(max_length=255, blank=True)
    quick_links = StreamField([
        ("quick_link", ProfileQuickLinkBlock())
    ], blank=True, use_json_field=True)
    profile_sections = StreamField([
        ("section", ProfileSectionBlock())
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("profile_image"),
        FieldPanel("hero_image"),
        FieldPanel("hero_polaroids"),
        FieldPanel("hero_micro_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_cta_text"),
        FieldPanel("hero_cta_anchor"),
        FieldPanel("intro_text"),
        FieldPanel("bio"),
        FieldPanel("about_heading"),
        FieldPanel("hobbies_title"),
        FieldPanel("hobbies_description"),
        FieldPanel("hobbies_cards"),
        FieldPanel("quick_links"),
        FieldPanel("profile_sections"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["profile_pages"] = self.get_parent().get_children().live().specific()
        return context

    # This page can only live under HomePage
    parent_page_types = ['home.HomePage']
    subpage_types = []  # No children allowed under a profile

    class Meta:
        verbose_name = "Profile Page"