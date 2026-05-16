"""
Rebuild the Watch House product catalogue with demo data.

Usage (from the project folder that contains manage.py):
    python load_sample_data.py

What it does
------------
* Creates / refreshes the 6 watch categories.
* Loads only the products that have a real watch photo under media/, so
  every product card shows a proper image (no generated placeholders).
* Removes any product whose slug is no longer listed here, keeping the
  database in sync with this file.
* Is safe to run repeatedly - it uses update_or_create, so a second run
  simply refreshes prices / stock / descriptions instead of duplicating.

Only data is touched here; the Django models and views are left untouched.
"""
import os

import django
from django.core.files.storage import default_storage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from products.models import Category, Product  # noqa: E402


# ---------------------------------------------------------------------------
# Categories - every category already has a real cover photo under media/.
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        'name': 'Luxury Watches',
        'slug': 'luxury-watches',
        'description': 'Premium timepieces from the world\'s most iconic '
                       'houses - Swiss craftsmanship, precious metals and '
                       'movements built to last a lifetime.',
        'image': 'categories/luxury_watches.jpg',
    },
    {
        'name': 'Smart Watches',
        'slug': 'smart-watches',
        'description': 'Connected wearables with health tracking, GPS, '
                       'notifications and vivid always-on displays for a '
                       'life in sync.',
        'image': 'categories/smart_watches.jpg',
    },
    {
        'name': 'Sports Watches',
        'slug': 'sports-watches',
        'description': 'Rugged, water-resistant watches built for athletes '
                       'and the outdoors - shock proof, trail ready and '
                       'tough enough for any adventure.',
        'image': 'categories/sports_watches.jpg',
    },
    {
        'name': 'Fashion Watches',
        'slug': 'fashion-watches',
        'description': 'Style-led watches that finish any outfit - clean '
                       'dials, on-trend finishes and everyday versatility.',
        'image': 'categories/fashion_watches.jpg',
    },
    {
        'name': 'Classic Watches',
        'slug': 'classic-watches',
        'description': 'Timeless designs with mechanical and automatic '
                       'movements - understated dress watches that never '
                       'go out of style.',
        'image': 'categories/classic_watches.jpg',
    },
    {
        'name': 'Digital Watches',
        'slug': 'digital-watches',
        'description': 'Iconic digital watches with alarms, stopwatches and '
                       'backlights - dependable, affordable and effortlessly '
                       'retro.',
        'image': 'categories/digital_watches.jpg',
    },
]


# ---------------------------------------------------------------------------
# Products - only items with a real photo already in media/products/.
# More can be added later once their photos are available.
# ---------------------------------------------------------------------------
PRODUCTS = [
    # -------------------- Luxury --------------------
    {
        'name': 'Rolex Submariner Date', 'slug': 'rolex-submariner-date',
        'category': 'luxury-watches', 'price': 1850000.00, 'stock': 4,
        'featured': True, 'image': 'products/rolex_submariner.jpg',
        'description': 'The benchmark luxury diver. A 41mm Oystersteel case '
                       'with a unidirectional Cerachrom bezel, the '
                       'self-winding Calibre 3235 movement and a 70-hour '
                       'power reserve. Water resistant to 300 metres and '
                       'instantly recognisable on any wrist.',
    },
    {
        'name': 'TAG Heuer Carrera Chronograph', 'slug': 'tag-heuer-carrera-chronograph',
        'category': 'luxury-watches', 'price': 612000.00, 'stock': 9,
        'featured': True, 'image': 'products/tag_heuer_carrera.jpg',
        'description': 'Motorsport heritage in a 44mm case. An automatic '
                       'Calibre Heuer 02 chronograph with an 80-hour power '
                       'reserve, skeleton dial and a date window. Built for '
                       'drivers who measure life in split seconds.',
    },

    # -------------------- Smart --------------------
    {
        'name': 'Samsung Galaxy Watch 6 Classic', 'slug': 'samsung-galaxy-watch-6-classic',
        'category': 'smart-watches', 'price': 52999.00, 'stock': 38,
        'featured': True, 'image': 'products/samsung_galaxy_watch_6.jpg',
        'description': 'A premium Wear OS smartwatch with the much-loved '
                       'rotating bezel. Advanced sleep coaching, body '
                       'composition analysis, heart-rate and a crisp Super '
                       'AMOLED display in a stainless-steel case.',
    },

    # -------------------- Sports --------------------
    {
        'name': 'Casio G-Shock GA-2100', 'slug': 'casio-g-shock-ga-2100',
        'category': 'sports-watches', 'price': 14999.00, 'stock': 90,
        'featured': True, 'image': 'products/casio_gshock_ga2100.jpg',
        'description': 'The cult-favourite "CasiOak". A slim octagonal case '
                       'with the famous Carbon Core Guard structure, shock '
                       'resistance and 200m water resistance. Analog-digital '
                       'styling that looks far more expensive than it is.',
    },

    # -------------------- Fashion --------------------
    {
        'name': 'Daniel Wellington Classic Petite', 'slug': 'daniel-wellington-classic-petite',
        'category': 'fashion-watches', 'price': 17999.00, 'stock': 55,
        'featured': True, 'image': 'products/daniel_wellington_classic.jpg',
        'description': 'Scandinavian minimalism at its finest. A slim 28mm '
                       'case, clean white dial and an interchangeable mesh '
                       'strap. Understated, elegant and endlessly easy to '
                       'style.',
    },
    {
        'name': 'Fossil Grant Chronograph', 'slug': 'fossil-grant-chronograph',
        'category': 'fashion-watches', 'price': 21999.00, 'stock': 42,
        'featured': False, 'image': 'products/fossil_grant_chronograph.jpg',
        'description': 'A vintage-inspired chronograph with bold Roman '
                       'numerals, three sub-dials and a rich genuine-leather '
                       'strap. A statement dress watch with real presence on '
                       'the wrist.',
    },

    # -------------------- Classic --------------------
    {
        'name': 'Seiko 5 Sports Automatic', 'slug': 'seiko-5-sports-automatic',
        'category': 'classic-watches', 'price': 28999.00, 'stock': 60,
        'featured': True, 'image': 'products/seiko_5_automatic.jpg',
        'description': 'The watch that introduced a generation to mechanical '
                       'timekeeping. A reliable automatic movement with '
                       'hand-winding and hacking, a day-date display and an '
                       'exhibition caseback. Outstanding value for an '
                       'automatic.',
    },
    {
        'name': 'Orient Bambino V4', 'slug': 'orient-bambino-v4',
        'category': 'classic-watches', 'price': 23999.00, 'stock': 44,
        'featured': False, 'image': 'products/orient_bambino.jpg',
        'description': 'A beloved entry-level dress watch. A beautifully '
                       'domed crystal, applied indices and an in-house '
                       'automatic movement. Elegant proportions that punch '
                       'well above their price.',
    },
    {
        'name': 'Tissot PRX Powermatic 80', 'slug': 'tissot-prx-powermatic-80',
        'category': 'classic-watches', 'price': 89999.00, 'stock': 21,
        'featured': True, 'image': 'products/tissot_prx_powermatic_80.jpg',
        'description': 'A 70s-inspired integrated-bracelet watch that took '
                       'the world by storm. A waffle-textured dial, sharp '
                       'tonneau case and the Powermatic 80 movement with an '
                       '80-hour power reserve.',
    },

    # -------------------- Digital --------------------
    {
        'name': 'SKMEI Dual-Time Digital Steel', 'slug': 'skmei-dual-time-digital-steel',
        'category': 'digital-watches', 'price': 2999.00, 'stock': 120,
        'featured': True, 'image': 'products/digital1.jpg',
        'description': 'A retro-styled digital watch with a tough '
                       'stainless-steel case and bracelet. Packed with '
                       'everyday functions - dual time, alarm, chronograph, '
                       'a countdown timer and an EL backlight - and rated '
                       'water resistant to 30 metres. Big value with a bold, '
                       'unmistakable retro look.',
    },
]


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------
def _assign_image(instance, rel_path):
    """Point an ImageField at an existing media file without re-copying it."""
    if rel_path and default_storage.exists(rel_path):
        if instance.image.name != rel_path:
            instance.image.name = rel_path
            instance.save(update_fields=['image'])
        return True
    return False


def run():
    print('Rebuilding the Watch House catalogue...\n')

    print('Categories')
    for data in CATEGORIES:
        category, created = Category.objects.update_or_create(
            slug=data['slug'],
            defaults={'name': data['name'], 'description': data['description']},
        )
        has_image = _assign_image(category, data['image'])
        flag = 'created' if created else 'updated'
        print(f"  [{flag}{' +img' if has_image else ''}] {category.name}")

    print('\nProducts')
    for data in PRODUCTS:
        category = Category.objects.get(slug=data['category'])
        product, created = Product.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'name': data['name'],
                'description': data['description'],
                'price': data['price'],
                'stock': data['stock'],
                'featured': data['featured'],
                'category': category,
            },
        )
        _assign_image(product, data['image'])
        flag = 'created' if created else 'updated'
        print(f"  [{flag}] {product.name} - NPR {product.price:,.0f}")

    # Keep the database in sync with this file - drop anything no longer listed.
    keep = {data['slug'] for data in PRODUCTS}
    stale = Product.objects.exclude(slug__in=keep)
    if stale.exists():
        print('\nRemoving products not listed here')
        for product in stale:
            print(f'  [removed] {product.name}')
        stale.delete()

    print('\n' + '=' * 52)
    print('Catalogue rebuild complete.')
    print(f"  Categories : {Category.objects.count()}")
    print(f"  Products   : {Product.objects.count()}")
    print(f"  Featured   : {Product.objects.filter(featured=True).count()}")
    print(f"  In stock   : {Product.objects.filter(stock__gt=0).count()}")
    print('=' * 52)


if __name__ == '__main__':
    run()
