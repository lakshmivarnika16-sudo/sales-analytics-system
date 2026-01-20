import requests


BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries

    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    try:
        url = f"{BASE_URL}?limit=100"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        simplified = []
        for p in products:
            simplified.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating"),
            })

        print(f"✓ Successfully fetched {len(simplified)} products from API")
        return simplified

    except Exception as e:
        print(" Failed to fetch products from API:", str(e))
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Parameters: api_products from fetch_all_products()
    Returns: dictionary mapping product IDs to info
    """
    mapping = {}

    for p in api_products:
        pid = p.get("id")
        if pid is None:
            continue

        mapping[int(pid)] = {
            "title": p.get("title"),
            "category": p.get("category"),
            "brand": p.get("brand"),
            "rating": p.get("rating"),
            "price": p.get("price"),
        }

    return mapping


def extract_numeric_product_id(product_id):
    """
    Extract numeric ID from ProductID
    Example:
    P101 -> 101
    P5 -> 5
    """
    try:
        if not product_id:
            return None

        s = str(product_id).strip()

        # remove leading P or p
        if s.lower().startswith("p"):
            s = s[1:]

        # keep only digits
        digits = "".join(ch for ch in s if ch.isdigit())

        return int(digits) if digits else None

    except:
        return None


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information

    Logic:
    - Extract numeric ID from ProductID (P101 → 101)
    - If ID exists in mapping -> add API fields
    - Else -> API_Match False and fields None
    """
    enriched = []

    for t in transactions:
        new_t = dict(t)  # copy original transaction

        try:
            pid_raw = new_t.get("ProductID") or new_t.get("product_id") or new_t.get("productId")
            numeric_id = extract_numeric_product_id(pid_raw)

            if numeric_id is not None and numeric_id in product_mapping:
                info = product_mapping[numeric_id]

                new_t["API_Category"] = info.get("category")
                new_t["API_Brand"] = info.get("brand")
                new_t["API_Rating"] = info.get("rating")
                new_t["API_Match"] = True
            else:
                new_t["API_Category"] = None
                new_t["API_Brand"] = None
                new_t["API_Rating"] = None
                new_t["API_Match"] = False

        except:
            new_t["API_Category"] = None
            new_t["API_Brand"] = None
            new_t["API_Rating"] = None
            new_t["API_Match"] = False

        enriched.append(new_t)

    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file (pipe delimited)

    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """

    if not enriched_transactions:
        # create empty file with headers
        with open(filename, "w", encoding="utf-8") as f:
            f.write("TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n")
        return

    # Keep original keys order + new fields at end
    base_fields = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region"
    ]
    api_fields = ["API_Category", "API_Brand", "API_Rating", "API_Match"]

    headers = base_fields + api_fields

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = []
            for h in headers:
                val = t.get(h)

                if val is None:
                    row.append("")
                else:
                    row.append(str(val))

            f.write("|".join(row) + "\n")
