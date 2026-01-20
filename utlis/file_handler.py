def read_sales_data(file_path):
    """
    Reads sales data file safely (handles encoding issues)
    Returns: list of cleaned transaction lines (50-100 lines)
    """

    try:
        # Try UTF-8 first
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    except UnicodeDecodeError:
        # If UTF-8 fails, try latin-1
        with open(file_path, "r", encoding="latin-1") as f:
            lines = f.readlines()

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    # Remove empty lines and strip spaces/newlines
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # Return only 50-100 lines (safe limit)
    return cleaned_lines[:100]
