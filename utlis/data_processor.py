from collections import defaultdict


def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float (total revenue)
    Expected Output: sum of (Quantity * UnitPrice)
    """
    total = 0.0

    for t in transactions:
        try:
            qty = int(t.get("Quantity", 0))
            price = float(t.get("UnitPrice", 0))
            total += qty * price
        except:
            continue

    return total


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary with region statistics
    Requirements:
    - total sales per region
    - transaction count per region
    - percentage of total sales
    - sorted by total_sales descending
    """
    region_data = defaultdict(lambda: {"total_sales": 0.0, "transaction_count": 0})

    overall_total = calculate_total_revenue(transactions)

    for t in transactions:
        try:
            region = t.get("Region", "Unknown")
            qty = int(t.get("Quantity", 0))
            price = float(t.get("UnitPrice", 0))
            amount = qty * price

            region_data[region]["total_sales"] += amount
            region_data[region]["transaction_count"] += 1
        except:
            continue

    # Add percentage
    for region in region_data:
        sales = region_data[region]["total_sales"]
        pct = (sales / overall_total * 100) if overall_total else 0.0
        region_data[region]["percentage"] = round(pct, 2)

    # Sort by total_sales desc and return as normal dict
    sorted_items = sorted(region_data.items(), key=lambda x: x[1]["total_sales"], reverse=True)

    result = {}
    for region, stats in sorted_items:
        result[region] = {
            "total_sales": round(stats["total_sales"], 2),
            "transaction_count": stats["transaction_count"],
            "percentage": stats["percentage"]
        }

    return result


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples
    Format:
    [('Laptop', 45, 2250000.0), ...]
    Sorted by total quantity desc
    """
    product_qty = defaultdict(int)
    product_revenue = defaultdict(float)

    for t in transactions:
        try:
            name = t.get("ProductName", "Unknown")
            qty = int(t.get("Quantity", 0))
            price = float(t.get("UnitPrice", 0))

            product_qty[name] += qty
            product_revenue[name] += qty * price
        except:
            continue

    items = []
    for name in product_qty:
        items.append((name, product_qty[name], round(product_revenue[name], 2)))

    items.sort(key=lambda x: x[1], reverse=True)  # sort by quantity
    return items[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary sorted by total_spent descending
    """
    customer_data = defaultdict(lambda: {
        "total_spent": 0.0,
        "purchase_count": 0,
        "products_bought": set()
    })

    for t in transactions:
        try:
            cid = t.get("CustomerID", "Unknown")
            pname = t.get("ProductName", "Unknown")
            qty = int(t.get("Quantity", 0))
            price = float(t.get("UnitPrice", 0))

            amount = qty * price

            customer_data[cid]["total_spent"] += amount
            customer_data[cid]["purchase_count"] += 1
            customer_data[cid]["products_bought"].add(pname)
        except:
            continue

    # Build final dict with avg order value and unique products list
    customers_list = []
    for cid, stats in customer_data.items():
        total_spent = stats["total_spent"]
        count = stats["purchase_count"]
        avg_order = (total_spent / count) if count else 0.0

        customers_list.append((
            cid,
            round(total_spent, 2),
            count,
            round(avg_order, 2),
            sorted(list(stats["products_bought"]))
        ))

    # sort by total_spent desc
    customers_list.sort(key=lambda x: x[1], reverse=True)

    result = {}
    for cid, total_spent, count, avg_order, products in customers_list:
        result[cid] = {
            "total_spent": total_spent,
            "purchase_count": count,
            "avg_order_value": avg_order,
            "products_bought": products
        }

    return result


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """
    daily = defaultdict(lambda: {
        "revenue": 0.0,
        "transaction_count": 0,
        "unique_customers": set()
    })

    for t in transactions:
        try:
            date = t.get("Date", "Unknown")
            cid = t.get("CustomerID", "Unknown")
            qty = int(t.get("Quantity", 0))
            price = float(t.get("UnitPrice", 0))

            daily[date]["revenue"] += qty * price
            daily[date]["transaction_count"] += 1
            daily[date]["unique_customers"].add(cid)
        except:
            continue

    # Convert sets to counts and sort by date
    sorted_dates = sorted(daily.keys())

    result = {}
    for d in sorted_dates:
        result[d] = {
            "revenue": round(daily[d]["revenue"], 2),
            "transaction_count": daily[d]["transaction_count"],
            "unique_customers": len(daily[d]["unique_customers"])
        }

    return result


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """
    trend = daily_sales_trend(transactions)

    best_date = None
    best_rev = -1
    best_count = 0

    for date, stats in trend.items():
        if stats["revenue"] > best_rev:
            best_rev = stats["revenue"]
            best_date = date
            best_count = stats["transaction_count"]

    if best_date is None:
        return ("N/A", 0.0, 0)

    return (best_date, best_rev, best_count)


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales (quantity < threshold)
    Returns: list of tuples sorted by quantity asc
    Format:
    [('Webcam', 4, 12000.0), ...]
    """
    product_qty = defaultdict(int)
    product_revenue = defaultdict(float)

    for t in transactions:
        try:
            name = t.get("ProductName", "Unknown")
            qty = int(t.get("Quantity", 0))
            price = float(t.get("UnitPrice", 0))

            product_qty[name] += qty
            product_revenue[name] += qty * price
        except:
            continue

    low = []
    for name in product_qty:
        if product_qty[name] < threshold:
            low.append((name, product_qty[name], round(product_revenue[name], 2)))

    low.sort(key=lambda x: x[1])  # sort by qty ascending
    return low




