import sys
from utils.file_handler import read_sales_file, save_enriched_data
from utils.data_processor import (
    parse_transactions,
    clean_transactions,
    validate_transactions,
    analyze_sales_data,
    generate_sales_report
)
from utils.api_handler import fetch_products_from_api, enrich_sales_data


def main():
    """
    Main execution function
    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
    5. Apply filters if user wants
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations
    """

    try:
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1/10] Reading sales data
        print("[1/10] Reading sales data...")
        raw_data = read_sales_file("data/sales_data.txt")  # must handle encoding inside file_handler
        print(f"✓ Successfully read {len(raw_data)} transactions")

        # [2/10] Parsing and cleaning
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        transactions = clean_transactions(transactions)
        print(f"✓ Parsed {len(transactions)} records")

        # [3/10] Filter options
        print("[3/10] Filter Options Available:")

        regions = sorted({t.get("region", "Unknown") for t in transactions})
        amounts = [float(t.get("sales_amount", 0)) for t in transactions if str(t.get("sales_amount", "")).strip() != ""]
        min_amt = min(amounts) if amounts else 0
        max_amt = max(amounts) if amounts else 0

        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min_amt:,.0f} - ₹{max_amt:,.0f}")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        if choice == "y":
            region_filter = input("Enter region to filter (or press Enter to skip): ").strip()
            min_filter = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_filter = input("Enter maximum amount (or press Enter to skip): ").strip()

            filtered = []
            for t in transactions:
                ok = True

                if region_filter:
                    ok = ok and (str(t.get("region", "")).lower() == region_filter.lower())

                if min_filter:
                    ok = ok and (float(t.get("sales_amount", 0)) >= float(min_filter))

                if max_filter:
                    ok = ok and (float(t.get("sales_amount", 0)) <= float(max_filter))

                if ok:
                    filtered.append(t)

            transactions = filtered
            print(f"✓ Filter applied. Remaining records: {len(transactions)}")
        else:
            print("✓ No filter applied")

        # [4/10] Validation
        print("[4/10] Validating transactions...")
        valid_transactions, invalid_transactions = validate_transactions(transactions)
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {len(invalid_transactions)}")

        # [5/10] Analysis
        print("[5/10] Analyzing sales data...")
        analysis_results = analyze_sales_data(valid_transactions)  # call all Part 2 functions inside this
        print("✓ Analysis complete")

        # [6/10] Fetch API products
        print("[6/10] Fetching product data from API...")
        products_data = fetch_products_from_api()
        print(f"✓ Fetched {len(products_data)} products")

        # [7/10] Enrichment
        print("[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, products_data)

        enriched_count = sum(1 for t in enriched_transactions if t.get("enriched") is True)
        total_valid = len(valid_transactions)
        success_rate = (enriched_count / total_valid * 100) if total_valid else 0

        print(f"✓ Enriched {enriched_count}/{total_valid} transactions ({success_rate:.1f}%)")

        # [8/10] Save enriched file
        print("[8/10] Saving enriched data...")
        enriched_file_path = "data/enriched_sales_data.txt"
        save_enriched_data(enriched_transactions, enriched_file_path)
        print(f"✓ Saved to: {enriched_file_path}")

        # [9/10] Generate report
        print("[9/10] Generating report...")
        report_path = generate_sales_report(
            valid_transactions,
            enriched_transactions,
            output_file="output/sales_report.txt"
        )
        print(f"✓ Report saved to: {report_path}")

        # [10/10] Done
        print("[10/10] Process Complete!")
        print("=" * 40)

    except FileNotFoundError:
        print(" Error: sales_data.txt not found. Please check data/sales_data.txt")
    except Exception as e:
        print(" Something went wrong!")
        print("Error details:", str(e))


if __name__ == "__main__":
    main()










from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data

api_products = fetch_all_products()
product_mapping = create_product_mapping(api_products)

enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
save_enriched_data(enriched_transactions, "data/enriched_sales_data.txt")





total_revenue = calculate_total_revenue(valid_transactions)
region_stats = region_wise_sales(valid_transactions)
top_products = top_selling_products(valid_transactions, n=5)
customers = customer_analysis(valid_transactions)
trend = daily_sales_trend(valid_transactions)
peak_day = find_peak_sales_day(valid_transactions)
low_products = low_performing_products(valid_transactions, threshold=10)

