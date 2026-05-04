from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock


# ─────────────────────────────────────────────
#  Shared / reusable blocks
# ─────────────────────────────────────────────

class NavLinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=100, help_text="Link text shown in nav bar")
    anchor = blocks.CharBlock(max_length=100, help_text="Anchor id without #, e.g. 'hobbies'")

    class Meta:
        icon = "link"
        label = "Nav link"


class HeroPolaroidBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "image"
        label = "Hero polaroid"


# ─────────────────────────────────────────────
#  HomePage-specific blocks
# ─────────────────────────────────────────────

class HomeQuickLinkBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=False, help_text="Small icon image (shown above title)")
    title = blocks.CharBlock(required=True, max_length=255)
    description = blocks.TextBlock(required=False)
    link_label = blocks.CharBlock(
        required=False, max_length=100,
        help_text="CTA text, e.g. 'View Hobbies'"
    )
    link_anchor = blocks.CharBlock(
        required=False, max_length=100,
        help_text="Anchor id without #, e.g. 'hobbies'"
    )

    class Meta:
        icon = "link"
        label = "Quick link card"


class CreatorBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True, max_length=255)
    bio = blocks.TextBlock(required=False)
    avatar = ImageChooserBlock(required=False)
    profile_page = blocks.PageChooserBlock(
        required=False,
        help_text="Link to this person's profile page"
    )

    class Meta:
        icon = "user"
        label = "Creator"


# ─────────────────────────────────────────────
#  ProfilePage blocks (unchanged)
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

    # ── Topbar ──
    site_title = models.CharField(
        max_length=255, blank=True, default="Our Favorites ✨",
        help_text="Logo text shown top-left"
    )
    nav_links = StreamField([
        ("link", NavLinkBlock())
    ], blank=True, use_json_field=True, help_text="Nav links between Home and Contact")
    contact_label = models.CharField(
        max_length=100, blank=True, default="Contact Us",
        help_text="Contact button label (leave blank to hide)"
    )
    contact_url = models.CharField(
        max_length=255, blank=True,
        help_text="Contact button URL or mailto:"
    )

    # ── Hero ──
    hero_micro_title = models.CharField(max_length=255, blank=True)
    hero_heading = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_description = models.TextField(blank=True)
    hero_cta_text = models.CharField(max_length=100, blank=True)
    hero_cta_anchor = models.CharField(max_length=100, blank=True)
    hero_polaroids = StreamField([
        ("polaroid", HeroPolaroidBlock())
    ], blank=True, use_json_field=True)

    # ── Quick links ──
    quick_links = StreamField([
        ("quick_link", HomeQuickLinkBlock())
    ], blank=True, use_json_field=True)

    # ── Meet the Creators ──
    creators_heading = models.CharField(max_length=255, blank=True, default="Meet the Creators")
    creators_subheading = models.CharField(max_length=255, blank=True)
    creators = StreamField([
        ("creator", CreatorBlock())
    ], blank=True, use_json_field=True)

    # ── Footer ──
    footer_text = models.CharField(max_length=255, blank=True)

    # Legacy fields (kept so existing migrations don't break)
    subtitle = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("site_title"),
            FieldPanel("nav_links"),
            FieldPanel("contact_label"),
            FieldPanel("contact_url"),
        ], heading="Topbar / Navigation"),

        MultiFieldPanel([
            FieldPanel("hero_micro_title"),
            FieldPanel("hero_heading"),
            FieldPanel("hero_subtitle"),
            FieldPanel("hero_description"),
            FieldPanel("hero_cta_text"),
            FieldPanel("hero_cta_anchor"),
            FieldPanel("hero_polaroids"),
        ], heading="Hero Section"),

        FieldPanel("quick_links"),

        MultiFieldPanel([
            FieldPanel("creators_heading"),
            FieldPanel("creators_subheading"),
            FieldPanel("creators"),
        ], heading="Meet the Creators"),

        FieldPanel("footer_text"),
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
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
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

    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = "Profile Page"