# gradebook.py
# Author: lakshay
# Date: November 13, 2025
# Title: Gradebook Analyzer

import csv
from statistics import median
from typing import Dict, List, Tuple

# --- Global Constants ---
PASS_THRESHOLD = 40

def print_welcome_menu() -> str:
    """Prints the welcome message and basic usage menu."""
    print("=" * 40)
    print(" WELCOME TO THE GRADEBOOK ANALYZER ")
    print("=" * 40)
    print("\nHow would you like to input student data?")
    print("  1. Manual Entry (Enter names and marks one by one)")
    print("  2. Import from CSV file (e.g., 'data.csv')")
    print("  3. Exit Program")
    return input("Enter your choice (1, 2, or 3): ").strip()

# --- Task 2: Data Entry or CSV Import ---

def manual_data_entry() -> Dict[str, int]:
    """Allows manual entry of student names and marks."""
    marks = {}
    print("\n--- Manual Data Entry ---")
    while True:
        name = input("Enter student name (or type 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        try:
            mark = int(input(f"Enter mark for {name} (0-100): ").strip())
            if 0 <= mark <= 100:
                marks[name] = mark
            else:
                print(" Mark must be between 0 and 100. Please re-enter.")
        except ValueError:
            print(" Invalid input. Please enter a valid number for the mark.")
    return marks

def import_csv_data() -> Dict[str, int]:
    """Loads student names and marks from a CSV file."""
    marks = {}
    file_name = input("Enter the CSV file name (e.g., students.csv): ").strip()
    print(f"\n--- Importing data from '{file_name}' ---")
    try:
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header_skipped = False
            for row in reader:
                if not header_skipped:
                    # Assuming the first row is a header
                    header_skipped = True
                    continue

                if len(row) >= 2:
                    name = row[0].strip()
                    try:
                        mark = int(row[1].strip())
                        if 0 <= mark <= 100:
                            marks[name] = mark
                        else:
                            print(f" Warning: Skipping {name}. Mark {mark} is out of range.")
                    except ValueError:
                        print(f"Error: Skipping row for {name}. Invalid mark value: {row[1]}")
                elif row:
                     print(f" Warning: Skipping incomplete row: {row}")

        if not marks:
            print(" File read successfully, but no valid student data was found (or file was empty).")
        else:
            print(f" Successfully imported data for {len(marks)} students.")

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f" An error occurred during CSV import: {e}")

    return marks

# --- Task 3: Statistical Analysis Functions ---

def calculate_average(marks_dict: Dict[str, int]) -> float:
    """Calculates the average score."""
    if not marks_dict:
        return 0.0
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict: Dict[str, int]) -> float:
    """Calculates the median score."""
    if not marks_dict:
        return 0.0
    # The statistics module's median function handles both even and odd lists
    return median(list(marks_dict.values()))

def find_max_score(marks_dict: Dict[str, int]) -> Tuple[str, int]:
    """Finds the maximum score and the student who achieved it."""
    if not marks_dict:
        return ("N/A", 0)
    max_mark = max(marks_dict.values())
    # Find the first student who achieved the max score
    top_student = next(name for name, mark in marks_dict.items() if mark == max_mark)
    return (top_student, max_mark)

def find_min_score(marks_dict: Dict[str, int]) -> Tuple[str, int]:
    """Finds the minimum score and the student who achieved it."""
    if not marks_dict:
        return ("N/A", 0)
    min_mark = min(marks_dict.values())
    # Find the first student who achieved the min score
    bottom_student = next(name for name, mark in marks_dict.items() if mark == min_mark)
    return (bottom_student, min_mark)

def display_statistics(marks_dict: Dict[str, int]):
    """Prints the statistical analysis summary."""
    if not marks_dict:
        print("\n--- Statistical Analysis ---")
        print("No data available for analysis.")
        return

    avg = calculate_average(marks_dict)
    med = calculate_median(marks_dict)
    max_name, max_score = find_max_score(marks_dict)
    min_name, min_score = find_min_score(marks_dict)

    print("\n" + "=" * 40)
    print("Statistical Analysis Summary")
    print("=" * 40)
    print(f"Total Students:    {len(marks_dict)}")
    print(f"Class Average:     {avg:.2f}")
    print(f"Class Median:      {med:.2f}")
    print(f"Highest Score:     {max_score} (Achieved by: {max_name})")
    print(f"Lowest Score:      {min_score} (Achieved by: {min_name})")
    print("-" * 40)

# --- Task 4: Grade Assignment and Distribution ---

def assign_grade(score: int) -> str:
    """Assigns a letter grade based on the score."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def generate_grades_and_distribution(marks_dict: Dict[str, int]) -> Tuple[Dict[str, str], Dict[str, int]]:
    """Generates the gradebook dictionary and counts grade distribution."""
    grades_dict: Dict[str, str] = {}
    distribution: Dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for name, mark in marks_dict.items():
        grade = assign_grade(mark)
        grades_dict[name] = grade
        distribution[grade] += 1

    return grades_dict, distribution

def display_grade_distribution(distribution: Dict[str, int]):
    """Prints the grade distribution count."""
    print("\n" + "=" * 40)
    print(" Grade Distribution Summary")
    print("=" * 40)
    for grade, count in distribution.items():
        print(f"Grade {grade} (Students: {count})")
    print("-" * 40)

# --- Task 5: Pass/Fail Filter with List Comprehension ---

def filter_pass_fail(marks_dict: Dict[str, int]) -> Tuple[List[str], List[str]]:
    """
    Uses list comprehension to filter students into passed and failed lists.
    Pass threshold is defined by PASS_THRESHOLD.
    """
    # List comprehension for passed students (score >= 40)
    passed_students = [
        name for name, score in marks_dict.items() if score >= PASS_THRESHOLD
    ]

    # List comprehension for failed students (score < 40)
    failed_students = [
        name for name, score in marks_dict.items() if score < PASS_THRESHOLD
    ]

    return passed_students, failed_students

def display_pass_fail(passed: List[str], failed: List[str]):
    """Prints the pass/fail summary."""
    print("\n" + "=" * 40)
    print(f" Pass/Fail Analysis (Pass Score: {PASS_THRESHOLD}+)")
    print("=" * 40)

    print(f"PASSED Students ({len(passed)}):")
    # Join names for a clean output
    print(f"  {', '.join(passed)}")

    print(f"\nFAILED Students ({len(failed)}):")
    print(f"  {', '.join(failed)}")
    print("-" * 40)

# --- Task 6: Results Table and User Loop ---

def print_results_table(marks_dict: Dict[str, int], grades_dict: Dict[str, str]):
    """Prints the final results in a formatted table."""
    if not marks_dict:
        print("\nNo results to display.")
        return

    print("\n" + "=" * 50)
    print(" Final Gradebook Results Table")
    print("=" * 50)

    # Set column widths for alignment
    NAME_WIDTH = 20
    MARKS_WIDTH = 10
    GRADE_WIDTH = 10

    # Header
    print(
        f"{'Name':<{NAME_WIDTH}} "
        f"{'Marks':<{MARKS_WIDTH}} "
        f"{'Grade':<{GRADE_WIDTH}}"
    )
    print("-" * (NAME_WIDTH + MARKS_WIDTH + GRADE_WIDTH + 4))

    # Data Rows
    for name, mark in marks_dict.items():
        grade = grades_dict.get(name, "N/A")
        # Using f-strings with alignment for clean formatting
        print(
            f"{name:<{NAME_WIDTH}} "
            f"{mark:<{MARKS_WIDTH}} "
            f"{grade:<{GRADE_WIDTH}}"
        )
    print("=" * 50)

def main_program_loop():
    """Main loop for the Gradebook Analyzer application."""
    running = True
    while running:
        choice = print_welcome_menu()

        marks: Dict[str, int] = {}

        # --- Task 2 Execution ---
        if choice == '1':
            marks = manual_data_entry()
        elif choice == '2':
            # Create a simple dummy CSV for testing if it doesn't exist
            # Assuming a file named 'test_grades.csv' with columns: Name, Mark
            # You should create this file for proper testing:
            # Name,Mark
            # Alice,78
            # Bob,92
            # Charlie,65
            # Diana,83
            # Evan,55
            # Fiona,95
            # George,39
            # Helen,72
            # For demonstration, you might enter 'test_grades.csv'
            marks = import_csv_data()
        elif choice == '3':
            print("\n Thank you for using the Gradebook Analyzer. Goodbye!")
            running = False
            continue
        else:
            print(" Invalid choice. Please select 1, 2, or 3.")
            continue

        if marks:
            # --- Task 3, 4, 5, 6 Execution ---
            display_statistics(marks)

            grades, distribution = generate_grades_and_distribution(marks)
            display_grade_distribution(distribution)

            passed, failed = filter_pass_fail(marks)
            display_pass_fail(passed, failed)

            print_results_table(marks, grades)

            # Task 6: Loop Menu
            while True:
                next_action = input("\nEnter 'R' to run a new analysis or 'X' to exit: ").strip().upper()
                if next_action == 'R':
                    break # Break inner loop to restart main loop
                elif next_action == 'X':
                    print("\n Thank you for using the Gradebook Analyzer. Goodbye!")
                    running = False
                    break # Break both loops
                else:
                    print(" Invalid input. Please enter 'R' or 'X'.")
        
        elif running:
            # If marks is empty but the user didn't explicitly exit (choice 1 or 2 failed)
            print("\nNo data was loaded. Returning to main menu.")


if __name__ == "__main__":
    main_program_loop()
