import os
from typing import Any
from woocommerce import API


async def get_woocomerce_products() -> list[dict[str, Any]]:
    wcapi = API(
        url=os.getenv("WOOCOMMERCE_URL"),
        consumer_key=os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
        consumer_secret=os.getenv("WOOCOMMERCE_CONSUMER_SECRET"),
        version="wc/v3"
    )
    response = wcapi.get("products", params={"per_page": 100, "page": 1})
    products = response.json()
    return products


# async def get_woocomerce_products() -> list[dict[str, Any]]:
#     return [
#         {
#             "Product ID": 101,
#             "Name": "Power Whey Protein 1kg",
#             "Price": 69.90,
#             "Stock Status": "instock",
#             "Stock Quantity": 23,
#             "Link": "https://research.blazperic.com/product/power-whey-protein-1kg/",
#             "Description": "<p>Premium whey protein izolat s 27g proteina po serviranju. Idealan za brzu apsorpciju nakon treninga i izgradnju mišićne mase. Dostupan u okusima čokolade, vanilije i jagode.</p>",
#             "OnSale": False,
#             "weight": "1kg",
#             "average_raiting": 4.85,
#             "categories": [{"id": 21, "name": "Proteini", "slug": "proteini"}],
#             "tags": ["whey", "protein", "izgradnja mišića"],
#             "attributes": [{"name": "Okus", "options": ["Čokolada", "Vanilija", "Jagoda"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi>69,90&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 102,
#             "Name": "Mass Gainer Extreme 2kg",
#             "Price": 89.50,
#             "Stock Status": "instock",
#             "Stock Quantity": 15,
#             "Link": "https://research.blazperic.com/product/mass-gainer-extreme-2kg/",
#             "Description": "<p>Visokokalorični mass gainer s 45g proteina i 650 kalorija po serviranju. Savršen za hardgainere koji žele povećati tjelesnu težinu i mišićnu masu. Obogaćen vitaminima i mineralima.</p>",
#             "OnSale": True,
#             "weight": "2kg",
#             "average_raiting": 4.60,
#             "categories": [{"id": 22, "name": "Gaineri", "slug": "gaineri"}],
#             "tags": ["mass gainer", "povećanje težine", "kalorije"],
#             "attributes": [{"name": "Okus", "options": ["Čokolada", "Banana"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi><del>109,90</del> 89,50&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 103,
#             "Name": "BCAA Powder 300g",
#             "Price": 45.00,
#             "Stock Status": "instock",
#             "Stock Quantity": 42,
#             "Link": "https://research.blazperic.com/product/bcaa-powder-300g/",
#             "Description": "<p>Mješavina esencijalnih aminokiselina razgranatog lanca (leucin, izoleucin, valin) u omjeru 2:1:1. Pospješuje oporavak mišića i smanjuje mišićni katabolizam tijekom intenzivnih treninga.</p>",
#             "OnSale": False,
#             "weight": "300g",
#             "average_raiting": 4.90,
#             "categories": [{"id": 23, "name": "Aminokiseline", "slug": "aminokiseline"}],
#             "tags": ["BCAA", "aminokiseline", "oporavak"],
#             "attributes": [{"name": "Okus", "options": ["Limun", "Naranča", "Bez okusa"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi>45,00&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 104,
#             "Name": "Pre-Workout Energy Booster 250g",
#             "Price": 59.90,
#             "Stock Status": "instock",
#             "Stock Quantity": 8,
#             "Link": "https://research.blazperic.com/product/pre-workout-energy-booster-250g/",
#             "Description": "<p>Napredna formula za maksimalnu energiju, fokus i snagu prije treninga. Sadrži kofein, beta-alanin, kreatin i L-arginin. Povećava izdržljivost i intenzitet treninga.</p>",
#             "OnSale": True,
#             "weight": "250g",
#             "average_raiting": 4.75,
#             "categories": [{"id": 24, "name": "Pre-Workout", "slug": "pre-workout"}],
#             "tags": ["energija", "fokus", "snaga", "pre-workout"],
#             "attributes": [{"name": "Okus", "options": ["Tropical Punch", "Blue Raspberry"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi><del>74,90</del> 59,90&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 105,
#             "Name": "Kreatin Monohidrat 500g",
#             "Price": 39.90,
#             "Stock Status": "instock",
#             "Stock Quantity": 31,
#             "Link": "https://research.blazperic.com/product/kreatin-monohidrat-500g/",
#             "Description": "<p>100% čisti kreatin monohidrat najviše kvalitete. Povećava eksplozivnu snagu, izdržljivost i mišićni volumen. Jedno od najbolje istraženih i najučinkovitijih dodataka prehrani za sportaše.</p>",
#             "OnSale": False,
#             "weight": "500g",
#             "average_raiting": 5.00,
#             "categories": [{"id": 25, "name": "Kreatin", "slug": "kreatin"}],
#             "tags": ["kreatin", "snaga", "volumen mišića"],
#             "attributes": [{"name": "Oblik", "options": ["Prah"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi>39,90&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 106,
#             "Name": "Vitamin Complex Sport 90 kapsula",
#             "Price": 34.50,
#             "Stock Status": "instock",
#             "Stock Quantity": 19,
#             "Link": "https://research.blazperic.com/product/vitamin-complex-sport-90-kapsula/",
#             "Description": "<p>Kompleksna multivitaminska formula posebno prilagođena potrebama sportaša. Sadrži sve esencijalne vitamine i minerale u optimalnim dozama za aktivan životni stil.</p>",
#             "OnSale": False,
#             "weight": "150g",
#             "average_raiting": 4.70,
#             "categories": [{"id": 26, "name": "Vitamini i Minerali", "slug": "vitamini-minerali"}],
#             "tags": ["vitamini", "zdravlje", "imunitet"],
#             "attributes": [{"name": "Količina", "options": ["90 kapsula"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi>34,50&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 107,
#             "Name": "Vegan Protein Blend 750g",
#             "Price": 79.90,
#             "Stock Status": "instock",
#             "Stock Quantity": 11,
#             "Link": "https://research.blazperic.com/product/vegan-protein-blend-750g/",
#             "Description": "<p>Visokokvalitetna mješavina biljnih proteina iz graška, riže i konoplje. Sadrži 24g proteina po serviranju i kompletan aminokiselinski profil. Idealno za vegane i one s intolerancijom na laktozu.</p>",
#             "OnSale": False,
#             "weight": "750g",
#             "average_raiting": 4.80,
#             "categories": [{"id": 21, "name": "Proteini", "slug": "proteini"}, {"id": 27, "name": "Vegan", "slug": "vegan"}],
#             "tags": ["vegan", "biljni protein", "bez laktoze"],
#             "attributes": [{"name": "Okus", "options": ["Čokolada", "Vanilija", "Crveno voće"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi>79,90&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 108,
#             "Name": "L-Glutamin 400g",
#             "Price": 49.90,
#             "Stock Status": "instock",
#             "Stock Quantity": 27,
#             "Link": "https://research.blazperic.com/product/l-glutamin-400g/",
#             "Description": "<p>100% čisti L-glutamin u prahu. Pospješuje oporavak mišića, jača imunološki sustav i poboljšava zdravlje probavnog sustava. Neophodan za intenzivne treninge i održavanje mišića.</p>",
#             "OnSale": False,
#             "weight": "400g",
#             "average_raiting": 4.65,
#             "categories": [{"id": 23, "name": "Aminokiseline", "slug": "aminokiseline"}],
#             "tags": ["glutamin", "oporavak", "imunitet"],
#             "attributes": [{"name": "Oblik", "options": ["Prah"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi>49,90&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 109,
#             "Name": "Shaker Protein Shop 700ml",
#             "Price": 12.50,
#             "Stock Status": "instock",
#             "Stock Quantity": 50,
#             "Link": "https://research.blazperic.com/product/shaker-protein-shop-700ml/",
#             "Description": "<p>Profesionalni shaker s metalnom kuglicom za savršeno miješanje. Volumena 700ml s mjernom skalom. Izrađen od BPA-free materijala, siguran za pranje u perilici posuđa.</p>",
#             "OnSale": False,
#             "weight": "120g",
#             "average_raiting": 4.50,
#             "categories": [{"id": 28, "name": "Oprema", "slug": "oprema"}],
#             "tags": ["shaker", "oprema"],
#             "attributes": [{"name": "Boja", "options": ["Crna", "Plava", "Prozirna"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi>12,50&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         },
#         {
#             "Product ID": 110,
#             "Name": "Thermogenic Fat Burner 120 kapsula",
#             "Price": 54.90,
#             "Stock Status": "instock",
#             "Stock Quantity": 14,
#             "Link": "https://research.blazperic.com/product/thermogenic-fat-burner-120-kapsula/",
#             "Description": "<p>Napredna formula za ubrzavanje metabolizma i sagorijevanje masnih naslaga. Sadrži L-karnitin, zeleni čaj, kofein i krom. Pomaže u definiciji mišića i regulaciji apetita.</p>",
#             "OnSale": True,
#             "weight": "90g",
#             "average_raiting": 4.40,
#             "categories": [{"id": 29, "name": "Mršavljenje", "slug": "mrsavljenje"}],
#             "tags": ["fat burner", "definicija", "metabolizam"],
#             "attributes": [{"name": "Količina", "options": ["120 kapsula"]}],
#             "price_html": "<span class=\"woocommerce-Price-amount amount\"><bdi><del>64,90</del> 54,90&nbsp;<span class=\"woocommerce-Price-currencySymbol\">KM</span></bdi></span>"
#         }
#     ]
