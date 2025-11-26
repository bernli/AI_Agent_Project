"""Test script to verify CSV loading workflow."""

import sys
import os

# Add insight_loop to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'insight_loop'))

from tools import save_csv_string_to_file, load_csv_data

# Test CSV content
csv_content = """Name,Age,City,Salary
Anna,25,Berlin,50000
Bob,30,München,60000
Charlie,35,Hamburg,70000
Diana,28,Frankfurt,55000"""

print("=" * 60)
print("TEST 1: Save CSV string to file")
print("=" * 60)

result1 = save_csv_string_to_file(csv_content)
print(f"Status: {result1['status']}")
print(f"Message: {result1.get('message', 'N/A')}")
print(f"File Path: {result1.get('file_path', 'N/A')}")

if result1['status'] == 'success':
    file_path = result1['file_path']

    print("\n" + "=" * 60)
    print("TEST 2: Load CSV from saved file")
    print("=" * 60)

    result2 = load_csv_data(file_path)
    print(f"Status: {result2['status']}")

    if result2['status'] == 'success':
        print(f"\nSource: {result2['source']}")
        print(f"Shape: {result2['schema']['shape']}")
        print(f"Columns: {result2['schema']['columns']}")
        print(f"\nSample rows:")
        for i, row in enumerate(result2['sample_rows'][:3], 1):
            print(f"  {i}. {row}")

        print("\n✅ ALL TESTS PASSED!")
    else:
        print(f"❌ Load failed: {result2.get('error_message', 'Unknown error')}")
else:
    print(f"❌ Save failed: {result1.get('error_message', 'Unknown error')}")

print("\n" + "=" * 60)
