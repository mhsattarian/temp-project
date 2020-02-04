import tkinter as tk

window = tk.Tk()
window.title("Biometrics User Authentication")

window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1, 2], minsize=200, weight=1)

btn_decrease = tk.Button(master=window, text="Enroll")
btn_decrease.grid(row=0, column=0, sticky="nsew")

btn_increase = tk.Button(master=window, text="Find")
btn_increase.grid(row=0, column=1, sticky="nsew")

user_id_entry = tk.Entry(master=window, width=10)
user_id_entry.grid(row=0, column=2)

window.mainloop()