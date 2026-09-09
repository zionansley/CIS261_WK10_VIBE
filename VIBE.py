class Student:
    """Represents one student record with names, IDs, test scores, average, and grade."""

    def __init__(self, name, id, test1, test2, test3):
        self.name = name.strip()
        self.id = id.strip()
        self.test1 = test1
        self.test2 = test2
        self.test3 = test3
        self.average = self.calculate_average()
        self.grade = self.calculate_grade(self.average)

    def calculate_average(self):
        """Calculate the average of the three test scores."""
        return round((self.test1 + self.test2 + self.test3) / 3, 2)

    @staticmethod
    def calculate_grade(average):
        """Return the letter grade based on the average."""
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"

    def to_record(self):
        """Return a pipe-delimited record for saving."""
        return (
            f"{self.name}|{self.id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|"
            f"{self.average:.2f}|{self.grade}"
        )


def get_valid_score(prompt):
    """Validate test score input and ensure it is a number between 0 and 100."""
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 100:
                return score
            print("Please enter a test score between 0 and 100.")
        except ValueError:
            print("Invalid score. Please enter a numeric value.")


def combine_student_data(name, id, test1, test2, test3):
    """Create and return a Student object from user input."""
    student = Student(name, id, test1, test2, test3)
    return student


def add_student(students):
    """Prompt the user for student data, create a Student object, and add it to the list."""
    print("\nAdd New Student")
    name = input("Enter student name: ").strip()
    while not name:
        print("Student name cannot be empty.")
        name = input("Enter student name: ").strip()

    student_id = input("Enter student ID: ").strip()
    while not student_id:
        print("Student ID cannot be empty.")
        student_id = input("Enter student ID: ").strip()

    test1 = get_valid_score("Enter Test 1 score: ")
    test2 = get_valid_score("Enter Test 2 score: ")
    test3 = get_valid_score("Enter Test 3 score: ")

    student = Student(name, student_id, test1, test2, test3)
    students.append(student)
    save_students(students)
    print(f"Student {student.name} added successfully.")


def display_students(students):
    """Display all students in a formatted table."""
    if not students:
        print("No student records available.")
        return

    print("\nStudent Records")
    header = f"{'Name':<20} {'ID':<10} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>10} {'Grade':>6}"
    print(header)
    print("-" * len(header))

    for student in students:
        print(
            f"{student.name:<20} {student.id:<10} {student.test1:>8.2f} {student.test2:>8.2f} "
            f"{student.test3:>8.2f} {student.average:>10.2f} {student.grade:>6}"
        )


def display_class_statistics(students):
    """Display class statistical information: highest average, lowest average, and class average."""
    if not students:
        print("No student records available.")
        return

    highest = max(students, key=lambda s: s.average)
    lowest = min(students, key=lambda s: s.average)
    class_average = sum(student.average for student in students) / len(students)

    print("\nClass Statistics")
    print("-" * 30)
    print(f"Highest Average: {highest.name} ({highest.average:.2f})")
    print(f"Lowest Average:  {lowest.name} ({lowest.average:.2f})")
    print(f"Class Average:   {class_average:.2f}")


def search_student(students):
    """Search all records by student name, case-insensitive."""
    query = input("Enter student name to search: ").strip().lower()

    matches = [student for student in students if query in student.name.lower()]

    if not matches:
        print("No matching student found.")
        return

    print("\nSearch Results")
    print("-" * 30)
    for student in matches:
        print(f"Name: {student.name} | ID: {student.id} | Test 1: {student.test1:.2f} | Test 2: {student.test2:.2f} "
              f"| Test 3: {student.test3:.2f} | Average: {student.average:.2f} | Grade: {student.grade}")


def save_students(students):
    """Save all students to the pipe-delimited file student_grades.txt."""
    try:
        with open("student_grades.txt", "w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_record() + "\n")
        print("Student records saved to student_grades.txt")
    except OSError as exc:
        print(f"Error saving records: {exc}")


def load_students():
    """Load all students from student_grades.txt. If the file is missing, start with an empty list."""
    students = []
    try:
        with open("student_grades.txt", "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Skipping invalid record on line {line_number}.")
                    continue
                try:
                    name = parts[0]
                    id = parts[1]
                    test1 = float(parts[2])
                    test2 = float(parts[3])
                    test3 = float(parts[4])
                    average = float(parts[5])
                    grade = parts[6]

                    student = Student(name, id, test1, test2, test3)
                    student.average = average
                    student.grade = grade
                    students.append(student)
                except ValueError:
                    print(f"Skipping invalid numeric data on line {line_number}.")
    except FileNotFoundError:
        print("No saved student file found. Starting with an empty list.")
    except OSError as exc:
        print(f"Error loading records: {exc}")

    return students


def print_menu():
    """Display the menu."""
    print("\nStudent Grade Calculator")
    print("1. Add student")
    print("2. Display all students")
    print("3. Search student by name")
    print("4. Display class statistics")
    print("5. Save records")
    print("6. Load records")
    print("ESC. Exit")


def main():
    """Main program loop."""
    students = load_students()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip().upper()

        if choice == "ESC":
            save_students(students)
            print("Exiting Student Grade Calculator. Goodbye!")
            break
        elif choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            display_class_statistics(students)
        elif choice == "5":
            save_students(students)
        elif choice == "6":
            students = load_students()
        else:
            print("Invalid option. Please choose a valid menu item.")


if __name__ == "__main__":
    main()
