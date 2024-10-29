import random
from tkinter import *

#Main Program Window
root = Tk()
root.title("Exercise 2 | Alexa Tell me a Joke")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#1e1e1e")
root.option_add("*Font", "Arial 16")

#Reads the jokes from the text file
def read_jokefile(filename):
    with open(filename, 'r') as file:
        return [line.strip().split('?') for line in file]

#Displays a suggestion if the input is incorrect
def display_suggestion():
    suggestion_label.config(text="Alexa can't answer that. Maybe try typing 'Alexa tell me a joke'?")
    root.after(2000, clear_suggestion)

#Clears the suggestion text
def clear_suggestion():
    suggestion_label.config(text="")

#Processes the user's input
def process_input(event=None):
    user_input = input_entry.get().strip().lower()
    if "alexa tell me a joke" in user_input:
        display_joke()
    else:
        display_suggestion()
    input_entry.delete(0, END)

#Displays the intiial joke
def display_joke():
    global setup, punchline
    setup, punchline = random.choice(jokes)
    input_entry.pack_forget()
    suggestion_label.pack_forget()
    quit_button.pack_forget()
    joke_label.config(text=setup + "?")
    punchline_button.pack()

#Displays the punchline of the joke
def display_joke_punchline():
    joke_label.config(text=punchline)
    punchline_button.pack_forget()
    for widget in root.pack_slaves():
        if isinstance(widget, Button) and widget.cget("text") in ["Tell Another Joke", "Ask a Different Prompt"]:
            widget.pack_forget()
    Button(root, text="Tell Another Joke", command=display_joke, bg="#90ee90", fg="black").pack(side=LEFT, padx=20, pady=10)
    Button(root, text="Ask a Different Prompt", command=reset_to_prompt, bg="#ffcccb", fg="black").pack(side=RIGHT, padx=20, pady=10)

#Resets the interface to the initial state
def reset_to_prompt():
    joke_label.config(text="")
    for widget in root.pack_slaves():
        widget.pack_forget()
    header.pack(pady=10)
    subheader.pack(pady=5)
    input_entry.pack(pady=5)
    suggestion_label.pack(pady=5)
    quit_button.pack(pady=10)
    joke_label.pack(pady=5)
    punchline_button.pack_forget()

#Header and subheader labels
header = Label(root, text="Chat with Alexa v0.01", fg="#00ff00", bg="#333333", font=("Arial", 24, "bold"), padx=10, pady=10)
header.pack(pady=10)
subheader = Label(root, text="Note: Alexa can only tell jokes as of this version", fg="#00ff00", bg="#333333", font=("Arial", 14), padx=10, pady=5)
subheader.pack(pady=5)

#Loads the jokes from the file
jokes = read_jokefile(r"C:\\Users\\carlo\\Documents\\the\\Advanced Programming\\assessment\\randomJokes.txt")

#Input entry setup
input_entry = Entry(root, width=40)
input_entry.pack(pady=5)
input_entry.bind("<Return>", process_input)

#Suggestion label setup
suggestion_label = Label(root, text="", fg="red", bg="#1e1e1e")
suggestion_label.pack(pady=5)

#Joke label setup
joke_label = Label(root, text="", fg="#00ff00", bg="#1e1e1e")
joke_label.pack(pady=20)

#Punchline button setup
punchline_button = Button(root, text="Tell me", command=display_joke_punchline, bg="#90ee90", fg="black")
punchline_button.pack_forget()

#Quit button setup
quit_button = Button(root, text="Exit", command=root.quit, bg="#ffcccb", fg="black")
quit_button.pack(pady=10)

#Start the main loop
root.mainloop()
