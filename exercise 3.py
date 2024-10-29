import tkinter as tk
from tkinter import messagebox, simpledialog

#Main Program Window
root = tk.Tk()
root.title("Exercise 3 | Student Manager")
root.geometry("800x700")
root.resizable(False, False)
root.configure(bg="#800000") 
root.option_add("*Font", "Arial 14")

#Creates the Student Class
class Student:
    def __init__(self, number, name, coursework1, coursework2, coursework3, exam_mark):
        #Initializes student attributes
        self.number = number
        self.name = name
        self.coursework_mark = coursework1 + coursework2 + coursework3
        self.exam_mark = exam_mark
        self.total_score = self.coursework_mark + exam_mark
        self.percentage = (self.total_score / 160) * 100
        self.grade = self.calculate_grade()

    #Calculates the grade based on percentage
    def calculate_grade(self):
        if self.percentage >= 70:
            return 'A'
        elif self.percentage >= 60:
            return 'B'
        elif self.percentage >= 50:
            return 'C'
        elif self.percentage >= 40:
            return 'D'
        else:
            return 'F'

#Loads students information from the designated file
def load_students_from_file(filename):
    students = []
    with open(filename, 'r') as file:
        for line in file:
            number, name, coursework1, coursework2, coursework3, exam_mark = line.strip().split(',')
            students.append(Student(number, name, int(coursework1), int(coursework2), int(coursework3), int(exam_mark)))
    return students

#Save students infromation to the designated file
def save_students_to_file(filename, students):
    with open(filename, 'w') as file:
        for student in students:
            file.write(f"{student.number},{student.name},{student.coursework_mark // 3},{student.coursework_mark // 3},{student.coursework_mark // 3},{student.exam_mark}\n")

#Loads the file path that is used for student data
file_path = (r"assets\\studentMarks.txt")
students = load_students_from_file(file_path)

#Creates a custom gui input dialog
def custom_askstring(title, prompt):
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.configure(bg="#800000")
    dialog.geometry("500x200")
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(dialog, text=prompt, font=("Helvetica", 18, "bold"), bg="#be0032", fg="white").pack(pady=10)
    entry = tk.Entry(dialog, width=20)
    entry.pack(pady=10)

    button_frame = tk.Frame(dialog, bg="#800000")
    button_frame.pack(pady=20)

    def on_ok():
        dialog.result = entry.get()
        dialog.destroy()

    def on_cancel():
        dialog.result = None
        dialog.destroy()

    tk.Button(button_frame, text="OK", command=on_ok, bg="#cb4154", fg="white", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Cancel", command=on_cancel, bg="#cb4154", fg="white", width=10).pack(side=tk.LEFT, padx=10)

    dialog.wait_window(dialog)
    return dialog.result

#Views all the student records
def view_all_records():
    output_box.delete(1.0, tk.END)
    for student in students:
        output_box.insert(tk.END, f"Number: {student.number}\nName: {student.name}\n"
                                  f"Coursework Mark: {student.coursework_mark}\nExam Mark: {student.exam_mark}\n"
                                  f"Overall Percentage: {student.percentage:.2f}%\nGrade: {student.grade}\n\n")
    output_box.insert(tk.END, f"Total Students: {len(students)}\n"
                              f"Average Percentage: {sum(s.percentage for s in students) / len(students):.2f}%\n")

#Views an individual student record
def view_individual_record():
    identifier = custom_askstring("Input", "Enter student number or name:")
    if identifier is None:
        return
    output_box.delete(1.0, tk.END)
    for student in students:
        if student.number == identifier or student.name.lower() == identifier.lower():
            output_box.insert(tk.END, f"Number: {student.number}\nName: {student.name}\n"
                                      f"Coursework Mark: {student.coursework_mark}\nExam Mark: {student.exam_mark}\n"
                                      f"Overall Percentage: {student.percentage:.2f}%\nGrade: {student.grade}\n")
            return
    messagebox.showerror("Error", "Student not found")

#Shows the student with the highest score
def show_highest_score():
    highest = max(students, key=lambda s: s.total_score)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Student with Highest Score:\nNumber: {highest.number}\nName: {highest.name}\n"
                              f"Total Score: {highest.total_score}\n")

#Shows the student with the lowest score
def show_lowest_score():
    lowest = min(students, key=lambda s: s.total_score)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Student with Lowest Score:\nNumber: {lowest.number}\nName: {lowest.name}\n"
                              f"Total Score: {lowest.total_score}\n")

#Adds a student record
def add_student_record():
    number = custom_askstring("Input", "Enter student number:")
    if number is None:
        return
    name = custom_askstring("Input", "Enter student name:")
    if name is None:
        return
    coursework1 = custom_askstring("Input", "Enter coursework mark 1 (out of 20):")
    if coursework1 is None:
        return
    coursework2 = custom_askstring("Input", "Enter coursework mark 2 (out of 20):")
    if coursework2 is None:
        return
    coursework3 = custom_askstring("Input", "Enter coursework mark 3 (out of 20):")
    if coursework3 is None:
        return
    exam_mark = custom_askstring("Input", "Enter exam mark (out of 100):")
    if exam_mark is None:
        return

    students.append(Student(number, name, int(coursework1), int(coursework2), int(coursework3), int(exam_mark)))
    save_students_to_file(file_path, students)
    messagebox.showinfo("Success", "Student record added successfully")

#Deletes a student record
def delete_student_record():
    identifier = custom_askstring("Input", "Enter student number or name:")
    if identifier is None:
        return
    global students
    students = [student for student in students if student.number != identifier and student.name.lower() != identifier.lower()]
    save_students_to_file(file_path, students)
    messagebox.showinfo("Success", "Student record deleted successfully")

#Updates a student record
def update_student_record():
    identifier = custom_askstring("Input", "Enter student number or name:")
    if identifier is None:
        return
    for student in students:
        if student.number == identifier or student.name.lower() == identifier.lower():
            name = custom_askstring("Input", "Enter new student name:")
            if name is None:
                return
            coursework1 = custom_askstring("Input", "Enter new coursework mark 1 (out of 20):")
            if coursework1 is None:
                return
            coursework2 = custom_askstring("Input", "Enter new coursework mark 2 (out of 20):")
            if coursework2 is None:
                return
            coursework3 = custom_askstring("Input", "Enter new coursework mark 3 (out of 20):")
            if coursework3 is None:
                return
            exam_mark = custom_askstring("Input", "Enter new exam mark (out of 100):")
            if exam_mark is None:
                return
            student.name = name
            student.coursework_mark = int(coursework1) + int(coursework2) + int(coursework3)
            student.exam_mark = int(exam_mark)
            student.total_score = student.coursework_mark + student.exam_mark
            student.percentage = (student.total_score / 160) * 100
            student.grade = student.calculate_grade()
            save_students_to_file(file_path, students)
            messagebox.showinfo("Success", "Student record updated successfully")
            return
    messagebox.showerror("Error", "Student not found")

#Sorts student records by number, name, or total score
def sort_student_records():
    dialog = tk.Toplevel(root)
    dialog.title("Sort Students")
    dialog.configure(bg="#800000")
    dialog.geometry("450x150")
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(dialog, text="Sort by:", font=("Helvetica", 20, "bold"), bg="#be0032", fg="white").pack(pady=10)

    button_frame = tk.Frame(dialog, bg="#800000")
    button_frame.pack(pady=20)

    def sort_by_number():
        students.sort(key=lambda s: s.number)
        dialog.destroy()
        view_all_records()

    def sort_by_name():
        students.sort(key=lambda s: s.name)
        dialog.destroy()
        view_all_records()

    def sort_by_total_score():
        students.sort(key=lambda s: s.total_score, reverse=True)
        dialog.destroy()
        view_all_records()

    tk.Button(button_frame, text="Number", command=sort_by_number, bg="#cb4154", fg="white", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Name", command=sort_by_name, bg="#cb4154", fg="white", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Total Score", command=sort_by_total_score, bg="#cb4154", fg="white", width=10).pack(side=tk.LEFT, padx=10)

    dialog.wait_window(dialog)

#Creates the header label
header = tk.Label(root, text="Student Manager", font=("Helvetica", 25, "bold"), bg="#be0032", fg="white")
header.pack(pady=20)

#Frames for the buttons
frame1 = tk.Frame(root, bg="#800000")
frame1.pack(pady=10)

#Buttons which are primarily used to view student record information
view_all_button = tk.Button(frame1, text="View All Student Records", command=view_all_records, width=25, bg="#cb4154", fg="white")
view_all_button.grid(row=0, column=0, padx=5, pady=5)

view_individual_button = tk.Button(frame1, text="View Individual Student Record", command=view_individual_record, width=25, bg="#cb4154", fg="white")
view_individual_button.grid(row=0, column=1, padx=5, pady=5)

highest_score_button = tk.Button(frame1, text="View Student with Highest Score", command=show_highest_score, width=25, bg="#cb4154", fg="white")
highest_score_button.grid(row=1, column=0, padx=5, pady=5)

lowest_score_button = tk.Button(frame1, text="View Student with Lowest Score", command=show_lowest_score, width=25, bg="#cb4154", fg="white")
lowest_score_button.grid(row=1, column=1, padx=5, pady=5)

#Main Text Box for outpit
output_box = tk.Text(root, height=15, width=80)
output_box.pack(pady=10)

#Adds a new frame and additional buttons for the extension problem, used primarily to add or edit to the student records, or to help sort the information by category
frame2 = tk.Frame(root, bg="#800000")
frame2.pack(pady=10)

add_student_button = tk.Button(frame2, text="Add Student Record", command=add_student_record, width=25, bg="#cb4154", fg="white")
add_student_button.grid(row=0, column=0, padx=5, pady=5)

delete_student_button = tk.Button(frame2, text="Delete Student Record", command=delete_student_record, width=25, bg="#cb4154", fg="white")
delete_student_button.grid(row=0, column=1, padx=5, pady=5)

update_student_button = tk.Button(frame2, text="Update Student Record", command=update_student_record, width=25, bg="#cb4154", fg="white")
update_student_button.grid(row=1, column=0, padx=5, pady=5)

sort_student_button = tk.Button(frame2, text="Sort Student Records", command=sort_student_records, width=25, bg="#cb4154", fg="white")
sort_student_button.grid(row=1, column=1, padx=5, pady=5)

#Starts the main event loop
root.mainloop()
