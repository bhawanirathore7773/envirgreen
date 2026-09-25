def site_context(request):
    """Sitewide values available to every template (nav links, tagline, etc.)."""
    return {
        "SITE_NAME": "Envirgreen",
        "SITE_TAGLINE": "See it. Report it. Fix it — together.",
    }
