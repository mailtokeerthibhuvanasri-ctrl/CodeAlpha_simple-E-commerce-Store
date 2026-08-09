PRODUCTS = [
    # Electronics
    dict(name="Aria Wireless Headphones", category="Electronics", price=129.00, compare_price=159.00,
         tagline="Studio-tuned sound, all day comfort",
         description="Over-ear wireless headphones with adaptive noise cancellation, 40-hour battery life and "
                      "a memory-foam headband built for long listening sessions.",
         icon_key="headphones", accent="emerald", rating=4.8, reviews=342),
    dict(name="Pulse Smart Watch", category="Electronics", price=189.00, compare_price=None,
         tagline="Your day, tracked with quiet precision",
         description="A refined fitness companion with heart-rate tracking, sleep insights and a seven-day "
                      "battery, wrapped in a brushed aluminium case.",
         icon_key="smartwatch", accent="clay", rating=4.6, reviews=201),
    dict(name="Ember Bluetooth Speaker", category="Electronics", price=79.00, compare_price=99.00,
         tagline="Room-filling sound in your palm",
         description="A compact speaker with 360-degree sound, IPX7 water resistance and 18 hours of playtime "
                      "for the kitchen, the beach or the balcony.",
         icon_key="speaker", accent="gold", rating=4.7, reviews=158),
    dict(name="Halo Mirrorless Camera", category="Electronics", price=649.00, compare_price=None,
         tagline="Every detail, exactly as you saw it",
         description="A lightweight mirrorless camera with a 24MP sensor, in-body stabilisation and a fold-out "
                      "touchscreen for effortless framing.",
         icon_key="camera", accent="emerald", rating=4.9, reviews=87),
    dict(name="Level Laptop Stand", category="Electronics", price=45.00, compare_price=None,
         tagline="A better angle for a better back",
         description="An anodised aluminium stand that lifts your laptop to eye level, folds flat for travel "
                      "and fits every 13 to 17 inch laptop.",
         icon_key="laptop-stand", accent="clay", rating=4.5, reviews=276),
    dict(name="Glide Wireless Mouse", category="Electronics", price=39.00, compare_price=49.00,
         tagline="Precision that disappears into your hand",
         description="An ergonomic wireless mouse with silent clicks, a 4000 DPI sensor and up to three months "
                      "of battery life on a single charge.",
         icon_key="mouse", accent="gold", rating=4.4, reviews=193),

    # Fashion
    dict(name="Wanderer Leather Jacket", category="Fashion", price=249.00, compare_price=299.00,
         tagline="Full-grain leather, broken in from day one",
         description="A timeless biker-cut jacket in full-grain leather with a quilted lining, built to soften "
                      "and mould to you over years of wear.",
         icon_key="jacket", accent="clay", rating=4.8, reviews=124),
    dict(name="Current Running Shoes", category="Fashion", price=119.00, compare_price=None,
         tagline="Built for the mile you haven't run yet",
         description="A responsive foam midsole and breathable knit upper designed to keep pace from your "
                      "first kilometre to your next personal best.",
         icon_key="sneaker", accent="emerald", rating=4.7, reviews=410),
    dict(name="Straight Cut Denim Jeans", category="Fashion", price=89.00, compare_price=None,
         tagline="A silhouette that never dates",
         description="Rigid selvedge denim cut with a relaxed straight leg, finished with brass hardware and "
                      "a fade that's uniquely yours over time.",
         icon_key="jeans", accent="gold", rating=4.5, reviews=167),
    dict(name="Meridian Sunglasses", category="Fashion", price=69.00, compare_price=89.00,
         tagline="Polarised clarity, understated frame",
         description="Hand-polished acetate frames with polarised UV400 lenses, striking a quiet balance "
                      "between classic and contemporary.",
         icon_key="sunglasses", accent="emerald", rating=4.6, reviews=98),
    dict(name="Atelier Leather Handbag", category="Fashion", price=179.00, compare_price=None,
         tagline="Structured shape, softened by hand",
         description="A structured tote in vegetable-tanned leather with a suede-lined interior and a strap "
                      "sized for the shoulder or the crook of the arm.",
         icon_key="handbag", accent="clay", rating=4.9, reviews=142),
    dict(name="Drift Wool Scarf", category="Fashion", price=49.00, compare_price=None,
         tagline="Merino warmth, woven not knitted",
         description="A generously sized merino wool scarf, woven in a soft herringbone that pairs with "
                      "everything from wool coats to denim jackets.",
         icon_key="scarf", accent="gold", rating=4.4, reviews=76),

    # Home & Kitchen
    dict(name="Brew Pour-Over Coffee Maker", category="Home & Kitchen", price=59.00, compare_price=69.00,
         tagline="Slow coffee, made simple",
         description="A borosilicate glass carafe and stainless steel filter designed to draw out full "
                      "flavour without a single paper filter.",
         icon_key="coffee-maker", accent="clay", rating=4.7, reviews=231),
    dict(name="Arc Table Lamp", category="Home & Kitchen", price=89.00, compare_price=None,
         tagline="Warm light, sculpted in brass",
         description="A dimmable table lamp with a hand-spun brass shade and a linen cord, casting a warm, "
                      "diffused glow across any reading corner.",
         icon_key="lamp", accent="gold", rating=4.6, reviews=118),
    dict(name="Terra Ceramic Vase", category="Home & Kitchen", price=39.00, compare_price=None,
         tagline="One shape, thrown by hand",
         description="A stoneware vase glazed in a soft matte finish, each piece kept slightly, deliberately "
                      "imperfect on the potter's wheel.",
         icon_key="vase", accent="emerald", rating=4.8, reviews=64),
    dict(name="Forge Cookware Set", category="Home & Kitchen", price=219.00, compare_price=259.00,
         tagline="Five pieces you'll reach for daily",
         description="A five-piece stainless steel cookware set with a tri-ply base for even heat, oven-safe "
                      "to 260°C and finished with riveted stay-cool handles.",
         icon_key="cookware", accent="clay", rating=4.7, reviews=189),
    dict(name="Hollow Throw Pillow", category="Home & Kitchen", price=35.00, compare_price=None,
         tagline="A softer corner of the room",
         description="A heavyweight cotton-linen cover with a feather-down insert, finished with a hidden "
                      "zip and a hand-stitched edge.",
         icon_key="pillow", accent="gold", rating=4.5, reviews=93),
    dict(name="Interval Wall Clock", category="Home & Kitchen", price=55.00, compare_price=None,
         tagline="Time, kept quietly on the wall",
         description="A silent-sweep wall clock in powder-coated steel with a minimal face designed to sit "
                      "well in any room.",
         icon_key="clock", accent="emerald", rating=4.4, reviews=71),

    # Books
    dict(name="The Long Horizon", category="Books", price=22.00, compare_price=None,
         tagline="A novel about leaving, and returning",
         description="A quietly gripping novel following three siblings across a decade of choices, coastlines "
                      "and the pull of home.",
         icon_key="book", accent="clay", rating=4.6, reviews=305),
    dict(name="Nightshade & Company", category="Books", price=19.00, compare_price=24.00,
         tagline="A mystery that rewards close readers",
         description="A slow-burn mystery set in a fog-bound coastal town, where every neighbour has a reason "
                      "to keep a secret.",
         icon_key="book", accent="emerald", rating=4.5, reviews=212),
    dict(name="The Kitchen Table", category="Books", price=28.00, compare_price=None,
         tagline="Recipes worth cooking twice",
         description="A collection of unfussy, seasonal recipes built around one good pan, one sharp knife "
                      "and ingredients worth seeking out.",
         icon_key="book", accent="gold", rating=4.8, reviews=156),

    # Sports & Outdoors
    dict(name="Even Ground Yoga Mat", category="Sports & Outdoors", price=45.00, compare_price=None,
         tagline="Grip that holds through every pose",
         description="A 5mm natural rubber mat with a moisture-wicking top layer, rolled to lie flat from "
                      "the very first practice.",
         icon_key="yogamat", accent="emerald", rating=4.7, reviews=249),
    dict(name="Basin Insulated Bottle", category="Sports & Outdoors", price=32.00, compare_price=38.00,
         tagline="Cold for a day, hot for twelve hours",
         description="A double-walled stainless steel bottle that keeps drinks at temperature far longer than "
                      "it has any right to, in a leak-proof shell.",
         icon_key="bottle", accent="clay", rating=4.6, reviews=318),
    dict(name="Basecamp Tent, 2-Person", category="Sports & Outdoors", price=159.00, compare_price=None,
         tagline="Shelter that goes up in four minutes",
         description="A freestanding two-person tent with a taped-seam rainfly, built to shrug off wind and "
                      "pitch quickly at the end of a long day.",
         icon_key="tent", accent="gold", rating=4.7, reviews=104),
    dict(name="Anchor Dumbbell Set", category="Sports & Outdoors", price=99.00, compare_price=None,
         tagline="A full range of resistance, one shelf",
         description="An adjustable dumbbell set covering five weight settings each, replacing a full rack "
                      "with something that fits in a closet.",
         icon_key="dumbbell", accent="emerald", rating=4.5, reviews=138),
]
