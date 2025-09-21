#!/usr/bin/env python3
"""
Analyze the booklet page ordering pattern
"""

def analyze_booklet_pattern():
    """Analyze the given A3->A4 page mapping to understand the pattern"""

    # Given mappings from the requirements
    mappings = [
        (1, [16, 17]),
        (2, [18, 15]),
        (3, [14, 19]),
        (4, [20, 13]),
        (5, [12, 21]),
        (6, [22, 11]),
        (7, [10, 23]),
        (8, [24, 9]),
        (9, [8, 25]),
        (10, [26, 7]),
        (11, [6, 27]),
        (12, [28, 5]),
        (13, [4, 29]),
        (14, [30, 3]),
        (15, [2, 31]),
        (16, [32, 1])
    ]

    total_pages = 32
    print(f"Total A4 pages: {total_pages}")
    print(f"Total A3 sheets: {len(mappings)}")
    print()

    print("A3 Page -> A4 Pages [Left, Right]")
    print("=" * 40)

    for a3_page, a4_pages in mappings:
        left, right = a4_pages
        print(f"A3 Page {a3_page:2d} -> A4 Pages [{left:2d}, {right:2d}]")

    print("\nPattern Analysis:")
    print("=" * 40)

    # Analyze left pages
    left_pages = [pages[0] for _, pages in mappings]
    right_pages = [pages[1] for _, pages in mappings]

    print(f"Left pages:  {left_pages}")
    print(f"Right pages: {right_pages}")

    # Check if it's a booklet pattern
    print("\nBooklet Pattern Check:")
    print("For 32-page booklet:")
    print("- First sheet: pages 32, 1, 2, 31")
    print("- Second sheet: pages 30, 3, 4, 29")
    print("- etc.")

    return True

def generate_booklet_mapping(total_pages):
    """
    Generate booklet page mapping for any number of pages

    Args:
        total_pages: Total number of A4 pages in the final document

    Returns:
        List of tuples: (A3_page_number, [left_A4_page, right_A4_page])
    """
    if total_pages % 4 != 0:
        # Pad to nearest multiple of 4
        padded_pages = ((total_pages + 3) // 4) * 4
        print(f"Warning: {total_pages} pages padded to {padded_pages} pages")
        total_pages = padded_pages

    sheets = total_pages // 4
    mapping = []

    for sheet in range(sheets):
        # For saddle-stitched booklet:
        # Sheet 1: pages [n, 1, 2, n-1]
        # Sheet 2: pages [n-2, 3, 4, n-3]
        # etc.

        # Left page calculation
        if sheet % 2 == 0:
            # Even sheet (0, 2, 4, ...): descending from total_pages
            left = total_pages - (sheet * 2)
        else:
            # Odd sheet (1, 3, 5, ...): ascending from 1
            left = 1 + ((sheet - 1) * 2)

        # Right page calculation
        if sheet % 2 == 0:
            # Even sheet: ascending from 1
            right = 1 + (sheet * 2)
        else:
            # Odd sheet: descending from total_pages
            right = total_pages - ((sheet - 1) * 2)

        mapping.append((sheet + 1, [left, right]))

    return mapping

def verify_pattern():
    """Verify our algorithm matches the given pattern"""

    print("Verifying Pattern Generation:")
    print("=" * 50)

    generated = generate_booklet_mapping(32)

    # Original pattern from requirements
    original = [
        (1, [16, 17]), (2, [18, 15]), (3, [14, 19]), (4, [20, 13]),
        (5, [12, 21]), (6, [22, 11]), (7, [10, 23]), (8, [24, 9]),
        (9, [8, 25]), (10, [26, 7]), (11, [6, 27]), (12, [28, 5]),
        (13, [4, 29]), (14, [30, 3]), (15, [2, 31]), (16, [32, 1])
    ]

    print("Generated vs Original:")
    print("A3 | Generated | Original | Match")
    print("-" * 40)

    matches = 0
    for i, (gen, orig) in enumerate(zip(generated, original)):
        gen_pages = gen[1]
        orig_pages = orig[1]
        match = gen_pages == orig_pages
        if match:
            matches += 1

        print(f"{i+1:2d} | {gen_pages}     | {orig_pages}    | {'✓' if match else '✗'}")

    print(f"\nMatches: {matches}/{len(original)}")

    if matches != len(original):
        print("Need to refine the algorithm...")
        return False
    else:
        print("Algorithm matches perfectly!")
        return True

if __name__ == "__main__":
    analyze_booklet_pattern()
    print("\n" + "="*60 + "\n")
    verify_pattern()