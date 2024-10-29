import tkinter as tk
from tkinter import messagebox
import random

#Main Program window
root = tk.Tk()
root.title("Exercise 1 | Arithmetic Quiz")
root.configure(bg="lightcyan")
root.geometry("600x400")
root.resizable(False, False)

#Displays the main menu
def displayMenu():
    clearScreen()
    header_label.config(text="Arithmetic Math Quiz Simulator", font=("Helvetica", 24, "bold"), fg="white", bg="darkblue")
    subtext_label.config(text="Please select a difficulty", font=("Helvetica", 14), fg="black", bg="lightgrey")
    tk.Button(root, text="Easy", command=lambda: set_difficulty('Easy'), font=("Helvetica", 12), bg="lightgrey").pack(pady=5)
    tk.Button(root, text="Moderate", command=lambda: set_difficulty('Moderate'), font=("Helvetica", 12), bg="lightgrey").pack(pady=5)
    tk.Button(root, text="Advanced", command=lambda: set_difficulty('Advanced'), font=("Helvetica", 12), bg="lightgrey").pack(pady=5)

#Sets the difficulty level
def set_difficulty(level):
    global difficulty
    difficulty = level
    clearScreen()
    startQuiz()

#Gnerates random integers based on the difficulty level
def randomInt():
    if difficulty == 'Easy':
        return random.randint(1, 9), random.randint(1, 9)
    elif difficulty == 'Moderate':
        return random.randint(10, 99), random.randint(10, 99)
    elif difficulty == 'Advanced':
        return random.randint(1000, 9999), random.randint(1000, 9999)

#Randomly decide the operation (either addition or subtraction)
def decideOperation():
    return random.choice(['+', '-'])

#Displays the math problem
def displayProblem():
    global num1, num2, operation, attempts
    num1, num2 = randomInt()
    operation = decideOperation()
    problem_label.config(text=f"{num1} {operation} {num2} = ?", font=("Helvetica", 16), bg="lightgrey")
    answer_entry.delete(0, tk.END)
    attempts = 0
    subtext_label.config(text=f"Question {question_count + 1}", font=("Helvetica", 14), fg="black", bg="lightgrey")

#Checks if the user's inputted answer is correct
def isCorrect(user_answer):
    correct_answer = eval(f"{num1} {operation} {num2}")
    return user_answer == correct_answer

#Provides feedback to the user and updates the score accordingly
def checkAnswer():
    global score, attempts
    try:
        user_answer = int(answer_entry.get())
        if isCorrect(user_answer):
            if attempts == 0:
                score += 1
            else:
                score += 0.5
            feedback_label.config(text="Correct!", fg="green", bg="lightgrey")
            nextQuestion()
        else:
            attempts += 1
            if attempts < 2:
                feedback_label.config(text="Incorrect, try again!", fg="orange", bg="lightgrey")
            else:
                feedback_label.config(text=f"Incorrect, the correct answer was {eval(f'{num1} {operation} {num2}')}", fg="red", bg="lightgrey")
                nextQuestion()
    except ValueError:
        feedback_label.config(text="Please enter a valid number.", fg="red", bg="lightgrey")

#Moves to the next question or display results if quiz is over
def nextQuestion():
    global question_count
    question_count += 1
    if question_count < 10:
        displayProblem()
    else:
        displayResults()

#Displays the final results and grade
def displayResults():
    #Hide the question prompt, input box, and submit button
    problem_label.pack_forget()
    answer_entry.pack_forget()
    submit_button.pack_forget()
    
    grade = ""
    if score > 9:
        grade = "A+"
    elif score > 8:
        grade = "A"
    elif score > 7:
        grade = "B"
    elif score > 6:
        grade = "C"
    else:
        grade = "D"
    
    feedback_label.config(text=f"Your final score is {score}/10\nGrade: {grade}", fg="blue", bg="lightgrey")
    subtext_label.config(text="Would you like to play again?", font=("Helvetica", 14), fg="black", bg="lightgrey")
    
    button_frame = tk.Frame(root, bg="lightgrey")
    button_frame.pack(pady=5)
    
    tk.Button(button_frame, text="Yes", command=resetQuiz, font=("Helvetica", 12), bg="lightgrey").pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="No", command=root.destroy, font=("Helvetica", 12), bg="lightgrey").pack(side=tk.LEFT, padx=10)

#Resets the quiz
def resetQuiz():
    global score, question_count
    score = 0
    question_count = 0
    clearScreen()
    displayMenu()

#Starts the quiz
def startQuiz():
    global problem_label, answer_entry, submit_button, feedback_label
    header_label.config(text="Arithmetic Math Quiz Simulator", font=("Helvetica", 24, "bold"), fg="white", bg="darkblue")
    subtext_label.config(text=f"Question {question_count + 1}", font=("Helvetica", 14), fg="black", bg="lightgrey")
    problem_label = tk.Label(root, text="", font=("Helvetica", 16), bg="lightgrey")
    problem_label.pack(pady=20)
    answer_entry = tk.Entry(root, font=("Helvetica", 16))
    answer_entry.pack(pady=10)
    submit_button = tk.Button(root, text="Submit", command=checkAnswer, font=("Helvetica", 12), bg="lightgrey")
    submit_button.pack(pady=20)
    feedback_label = tk.Label(root, text="", font=("Helvetica", 12), bg="lightgrey")
    feedback_label.pack(pady=10)
    displayProblem()

#Clear the screen when the program needs to reset
def clearScreen():
    for widget in root.winfo_children():
        if widget not in (header_label, subtext_label):
            widget.destroy()

#Header and subtext labels
header_label = tk.Label(root, text="Arithmetic Math Quiz Simulator", font=("Helvetica", 24, "bold"), fg="white", bg="darkblue")
header_label.pack(pady=10)
subtext_label = tk.Label(root, text="", font=("Helvetica", 14), fg="black", bg="lightgrey")
subtext_label.pack(pady=5)

#Setsup the global variables
score = 0
question_count = 0
difficulty = 'Easy'
attempts = 0

#Displays the main menu
displayMenu()

#Start the main loop
root.mainloop()
