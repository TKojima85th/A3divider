#!/usr/bin/env python3
"""
Deep analysis of the actual page ordering pattern
"""

def analyze_actual_pattern():
    """Analyze the actual pattern from the data"""

    # Given mappings from requirements
    data = [
        (1, [16, 17]), (2, [18, 15]), (3, [14, 19]), (4, [20, 13]),
        (5, [12, 21]), (6, [22, 11]), (7, [10, 23]), (8, [24, 9]),
        (9, [8, 25]), (10, [26, 7]), (11, [6, 27]), (12, [28, 5]),
        (13, [4, 29]), (14, [30, 3]), (15, [2, 31]), (16, [32, 1])
    ]

    print("Detailed Pattern Analysis:")
    print("=" * 50)

    # Analyze the sequence of left and right pages
    left_pages = []
    right_pages = []

    for a3_page, (left, right) in data:
        left_pages.append(left)
        right_pages.append(right)
        print(f"A3 Page {a3_page:2d}: Left={left:2d}, Right={right:2d}")

    print(f"\nLeft pages sequence:  {left_pages}")
    print(f"Right pages sequence: {right_pages}")

    # Check patterns in left pages
    print("\nLeft pages pattern:")
    for i, page in enumerate(left_pages):
        if i > 0:
            diff = page - left_pages[i-1]
            print(f"  Position {i+1}: {page:2d} (diff: {diff:+3d})")
        else:
            print(f"  Position {i+1}: {page:2d} (start)")

    # Check patterns in right pages
    print("\nRight pages pattern:")
    for i, page in enumerate(right_pages):
        if i > 0:
            diff = page - right_pages[i-1]
            print(f"  Position {i+1}: {page:2d} (diff: {diff:+3d})")
        else:
            print(f"  Position {i+1}: {page:2d} (start)")

    # Look for alternating pattern
    print("\nAlternating pattern analysis:")
    print("Left pages by A3 position:")
    odd_left = [left_pages[i] for i in range(0, len(left_pages), 2)]  # positions 1,3,5...
    even_left = [left_pages[i] for i in range(1, len(left_pages), 2)]  # positions 2,4,6...

    print(f"  Odd A3 positions (1,3,5...): {odd_left}")
    print(f"  Even A3 positions (2,4,6...): {even_left}")

    print("Right pages by A3 position:")
    odd_right = [right_pages[i] for i in range(0, len(right_pages), 2)]
    even_right = [right_pages[i] for i in range(1, len(right_pages), 2)]

    print(f"  Odd A3 positions (1,3,5...): {odd_right}")
    print(f"  Even A3 positions (2,4,6...): {even_right}")

    # Find the formula
    print("\nFormula discovery:")
    total_pages = 32
    middle = total_pages // 2  # 16

    print(f"Total pages: {total_pages}, Middle: {middle}")

    # Pattern seems to be:
    # For odd A3 positions: left decreases from middle, right increases from middle+1
    # For even A3 positions: left increases from middle+2, right decreases from middle-1

    return True

def discover_formula():
    """Try to discover the mathematical formula"""

    total_pages = 32
    middle = total_pages // 2  # 16

    print("Formula Discovery:")
    print("=" * 30)

    # Generate based on observed pattern
    generated = []

    for a3_page in range(1, 17):  # 16 A3 pages
        if a3_page % 2 == 1:  # Odd A3 page (1, 3, 5, ...)
            # For odd positions: left starts at middle and decreases by 2 each time
            # right starts at middle+1 and increases by 2 each time
            pos = (a3_page - 1) // 2  # 0, 1, 2, 3...
            left = middle - (pos * 2)
            right = (middle + 1) + (pos * 2)
        else:  # Even A3 page (2, 4, 6, ...)
            # For even positions: left starts at middle+2 and increases by 2 each time
            # right starts at middle-1 and decreases by 2 each time
            pos = (a3_page - 2) // 2  # 0, 1, 2, 3...
            left = (middle + 2) + (pos * 2)
            right = (middle - 1) - (pos * 2)

        generated.append((a3_page, [left, right]))
        print(f"A3 Page {a3_page:2d}: [{left:2d}, {right:2d}]")

    return generated

def verify_formula():
    """Verify the discovered formula"""

    # Original data
    original = [
        (1, [16, 17]), (2, [18, 15]), (3, [14, 19]), (4, [20, 13]),
        (5, [12, 21]), (6, [22, 11]), (7, [10, 23]), (8, [24, 9]),
        (9, [8, 25]), (10, [26, 7]), (11, [6, 27]), (12, [28, 5]),
        (13, [4, 29]), (14, [30, 3]), (15, [2, 31]), (16, [32, 1])
    ]

    generated = discover_formula()

    print("\nVerification:")
    print("=" * 40)
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
    return matches == len(original)

if __name__ == "__main__":
    analyze_actual_pattern()
    print("\n" + "="*60 + "\n")
    success = verify_formula()
    if success:
        print("✓ Formula discovered successfully!")
    else:
        print("✗ Need to refine formula...")