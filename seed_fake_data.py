from nosql_products.models_nosql import Category, Product
from mongoengine import connect

# Connect to the MongoDB database
connect('telangana_handicrafts_db')

# Define your categories
categories_data = [
    {"name": "Handlooms", "description": "Traditional handwoven fabrics and garments."},
    {"name": "Metal Crafts", "description": "Exquisite metal handicrafts from Telangana."},
    {"name": "Textile & Embroidery", "description": "Embroidered fabrics and textile crafts."},
    {"name": "Paintings & Art", "description": "Hand-painted artworks and scrolls."},
    {"name": "Home Decor", "description": "Decorative items for home."},
    {"name": "Silver Crafts", "description": "Finely crafted silver items."}
]

# Step 1: Insert categories if not present and build a map of category name to object
category_map = {}
for cat_data in categories_data:
    category = Category.objects(name=cat_data["name"]).first()
    if not category:
        category = Category(**cat_data)
        category.save()
        print(f"Category '{cat_data['name']}' saved.")
    else:
        print(f"Category '{cat_data['name']}' already exists.")
    category_map[cat_data["name"]] = category  # Build map

# Step 2: Define sample products
products_data = [
    {
        "name": "Pochampally Silk Dupatta",
        "description": "Elegant silk dupatta in traditional Pochampally ikat patterns",
        "price": 900,
        "stock": 30,
        "category": "Handlooms"
    },
    {
        "name": "Gadwal Cotton Saree",
        "description": "Classic cotton saree with Gadwal zari border",
        "price": 1600,
        "stock": 25,
        "category": "Handlooms"
    },
    {
        "name": "Narayanpet Checked Saree",
        "description": "Narayanpet saree with vibrant checks and temple border",
        "price": 1300,
        "stock": 20,
        "category": "Handlooms"
    },
    {
        "name": "Dokra Tortoise Figurine",
        "description": "Handmade dokra metal tortoise for decor and good luck",
        "price": 850,
        "stock": 40,
        "category": "Metal Crafts"
    },
    {
        "name": "Bidri Hookah Base",
        "description": "Decorative Bidriware hookah base with silver inlay",
        "price": 1800,
        "stock": 15,
        "category": "Metal Crafts"
    },
    {
        "name": "Pembarthi Wall Hanging",
        "description": "Brass wall art handcrafted in Pembarthi tradition",
        "price": 2200,
        "stock": 10,
        "category": "Metal Crafts"
    },
    {
        "name": "Banjara Embroidered Cushion Cover",
        "description": "Bright hand-stitched cushion cover with mirror work",
        "price": 400,
        "stock": 50,
        "category": "Textile & Embroidery"
    },
    {
        "name": "Banjara Beaded Pouch",
        "description": "Small embroidered pouch with traditional Banjara beads",
        "price": 250,
        "stock": 60,
        "category": "Textile & Embroidery"
    },
    {
        "name": "Cheriyal Village Life Scroll",
        "description": "Colorful scroll depicting rural life in Cheriyal style",
        "price": 2700,
        "stock": 15,
        "category": "Paintings & Art"
    },
    {
        "name": "Nirmal Wooden Tray",
        "description": "Decorative wooden tray with Nirmal floral painting",
        "price": 750,
        "stock": 25,
        "category": "Paintings & Art"
    },
    {
        "name": "Lacquer Jewelry Box",
        "description": "Handcrafted lacquer ware box for jewelry and trinkets",
        "price": 550,
        "stock": 30,
        "category": "Home Decor"
    },
    {
        "name": "Warangal Cotton Rug",
        "description": "Durable handwoven rug made in Warangal weaving tradition",
        "price": 1900,
        "stock": 20,
        "category": "Home Decor"
    },
    {
        "name": "Filigree Jewelry Box",
        "description": "Miniature silver filigree box with intricate design",
        "price": 2000,
        "stock": 15,
        "category": "Silver Crafts"
    },
    {
        "name": "Silver Filigree Earrings",
        "description": "Elegant handcrafted silver earrings in filigree style",
        "price": 1100,
        "stock": 30,
        "category": "Silver Crafts"
    },
]

# Step 3: Insert products if not already present
for product_data in products_data:
    # Check if product already exists
    if Product.objects(name=product_data["name"]).first():
        print(f"Product '{product_data['name']}' already exists. Skipping.")
        continue
    
    category_obj = category_map.get(product_data["category"])
    if not category_obj:
        print(f"Category '{product_data['category']}' not found for product '{product_data['name']}'. Skipping.")
        continue
    
    product = Product(
        name=product_data["name"],
        description=product_data["description"],
        price=product_data["price"],
        stock=product_data["stock"],
        category=category_obj,
        images=[],
        tags=[],
        available=True
    )
    product.save()
    print(f"Product '{product.name}' saved.")

print("Data seeding complete.")
