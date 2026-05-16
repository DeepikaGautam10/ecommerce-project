"""
Presentational helpers for the storefront templates.

These tags add customer-style star ratings to the product cards without
touching the Product model or the database. Each rating is derived
deterministically from the product's primary key, so a given product
always shows the same rating and review count on every page.
"""
import hashlib

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Weighted toward strong ratings - this is a curated demo catalogue.
_RATING_POOL = [3.5, 4.0, 4.0, 4.5, 4.5, 4.5, 4.5, 5.0, 5.0]


def _seed(product):
    """Return a stable integer derived from a product's identity."""
    key = f"{getattr(product, 'pk', '') or ''}:{getattr(product, 'slug', '') or ''}"
    return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)


@register.filter
def rating_value(product):
    """A stable rating between 3.5 and 5.0 for the given product."""
    return _RATING_POOL[_seed(product) % len(_RATING_POOL)]


@register.filter
def review_count(product):
    """A stable, plausible review count for the given product."""
    return 18 + _seed(product) % 472


@register.simple_tag
def star_rating(product, show_count=True):
    """Render a Font Awesome star rating for use inside product templates."""
    rating = rating_value(product)
    full = int(rating)
    has_half = (rating - full) >= 0.5

    stars = []
    for i in range(5):
        if i < full:
            stars.append('<i class="fas fa-star"></i>')
        elif i == full and has_half:
            stars.append('<i class="fas fa-star-half-stroke"></i>')
        else:
            stars.append('<i class="far fa-star"></i>')

    html = (
        f'<span class="star-rating">'
        f'<span class="stars">{"".join(stars)}</span>'
        f'<span class="rating-score">{rating:g}</span>'
    )
    if show_count:
        html += f'<span class="rating-count">({review_count(product)})</span>'
    html += '</span>'
    return mark_safe(html)
