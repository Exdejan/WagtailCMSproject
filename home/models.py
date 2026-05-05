from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page


# ─────────────────────────────────────────────
#  Shared blocks
# ─────────────────────────────────────────────

class HeroPolaroidBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "image"
        label = "Hero polaroid"


# ─────────────────────────────────────────────
#  HomePage blocks
# ─────────────────────────────────────────────

class HomeQuickLinkBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    description = blocks.TextBlock(required=False)
    icon_emoji = blocks.CharBlock(
        required=False, max_length=8,
        help_text="Single emoji for the card icon, e.g. 🎮 🍜 🎵"
    )
    link_label = blocks.CharBlock(
        required=False, max_length=100,
        help_text="CTA text, e.g. 'View Games'"
    )
    link_anchor = blocks.CharBlock(
        required=False, max_length=100,
        help_text="Anchor id without #, e.g. 'games'"
    )

    class Meta:
        icon = "link"
        label = "Feature card"


class CreatorBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True, max_length=255)
    bio = blocks.TextBlock(required=False, help_text="Short one-liner shown on the card")
    avatar = ImageChooserBlock(required=False)
    profile_page = blocks.PageChooserBlock(
        required=False,
        help_text="Links the 'View Archive' button to this person's profile page"
    )

    class Meta:
        icon = "user"
        label = "Creator"


# ─────────────────────────────────────────────
#  ProfilePage blocks
# ─────────────────────────────────────────────

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
    section_id = blocks.CharBlock(
        required=True, max_length=100,
        help_text="Anchor id like hobbies, games, food"
    )
    section_title = blocks.CharBlock(required=True, max_length=255)
    section_description = blocks.TextBlock(required=False)
    items = blocks.ListBlock(ProfileSectionItemBlock())

    class Meta:
        icon = "list-ul"
        label = "Profile section"


# ─────────────────────────────────────────────
#  Pages
# ─────────────────────────────────────────────

class HomePage(Page):
    template = "home/home_page.html"

    # ── Navbar ──
    site_title = models.CharField(
        max_length=255, blank=True, default="Artist Archive ✨",
        help_text="Logo text shown top-left in the navbar"
    )
    about_label = models.CharField(
        max_length=100, blank=True,
        help_text="Optional 'About Us' nav link label (links to #about)"
    )
    contact_text = models.CharField(
        max_length=100, blank=True,
        help_text="Contact Us button label in the navbar, e.g. 'Contact Us'"
    )
    contact_url = models.CharField(
        max_length=255, blank=True,
        help_text="URL or mailto: for the contact button"
    )

    # ── Hero ──
    hero_micro_title = models.CharField(
        max_length=255, blank=True,
        help_text="Small uppercase eyebrow label above the main heading"
    )
    hero_heading = models.CharField(
        max_length=255, blank=True,
        help_text="Main hero heading, e.g. 'Our Favorites'"
    )
    hero_subtitle = models.CharField(
        max_length=255, blank=True,
        help_text="Italic green continuation of the heading, e.g. 'Our World.'"
    )
    hero_description = models.TextField(
        blank=True,
        help_text="Short paragraph below the heading"
    )
    hero_cta_text = models.CharField(
        max_length=100, blank=True,
        help_text="CTA button label, e.g. 'Explore Our Favorites'"
    )
    hero_cta_anchor = models.CharField(
        max_length=100, blank=True,
        help_text="Section id the CTA scrolls to, e.g. 'creators'"
    )
    hero_polaroids = StreamField([
        ("polaroid", HeroPolaroidBlock())
    ], blank=True, use_json_field=True,
        help_text="Up to 3 polaroid-style photo cards stacked on the right side of the hero"
    )

    # ── Feature cards (quick links) ──
    quick_links = StreamField([
        ("quick_link", HomeQuickLinkBlock())
    ], blank=True, use_json_field=True,
        help_text="Horizontal strip of feature cards below the hero — one per section"
    )

    # ── Meet the Creators ──
    creators_heading = models.CharField(
        max_length=255, blank=True, default="Meet the Creators",
        help_text="Section heading"
    )
    creators_subheading = models.CharField(
        max_length=255, blank=True,
        help_text="Optional subtitle below the heading"
    )
    creators = StreamField([
        ("creator", CreatorBlock())
    ], blank=True, use_json_field=True,
        help_text="One card per creator — avatar, name, bio, and link to their profile"
    )

    # ── Footer ──
    footer_text = models.CharField(
        max_length=255, blank=True,
        help_text="Footer line, e.g. '© 2025 Artist Archive. All rights reserved. ♡'"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("site_title"),
            FieldPanel("about_label"),
            FieldPanel("contact_text"),
            FieldPanel("contact_url"),
        ], heading="Navbar"),

        MultiFieldPanel([
            FieldPanel("hero_micro_title"),
            FieldPanel("hero_heading"),
            FieldPanel("hero_subtitle"),
            FieldPanel("hero_description"),
            FieldPanel("hero_cta_text"),
            FieldPanel("hero_cta_anchor"),
            FieldPanel("hero_polaroids"),
        ], heading="Hero Section"),

        MultiFieldPanel([
            FieldPanel("quick_links"),
        ], heading="Feature Cards"),

        MultiFieldPanel([
            FieldPanel("creators_heading"),
            FieldPanel("creators_subheading"),
            FieldPanel("creators"),
        ], heading="Meet the Creators"),

        MultiFieldPanel([
            FieldPanel("footer_text"),
        ], heading="Footer"),
    ]

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
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
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

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = "Profile Page"