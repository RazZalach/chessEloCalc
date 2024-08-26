import tkinter as tk
from tkinter import ttk
from student_manager import add_student,get_leader, update_elo, load_students, update_elo_manually, delete_student

def refresh_table(tree, df=None):
    for row in tree.get_children():
        tree.delete(row)

    if df is None:
        df = load_students()
    for index, row in df.iterrows():
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=(row.ID, row.Name, row.ELO, row.Date, row.Rank, row.Wins, row.Losses, row.Draws), tags=(tag,))
    for col in tree['columns']:
        tree.column(col, anchor='center')

def sort_by_rank():
    df = load_students()
    df_sorted = df.sort_values(by='Rank', ascending=False)
    refresh_table(tree, df_sorted)

def add_student_gui():
    def submit():
        name = name_entry.get()
        add_student(name)
        refresh_table(tree)
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("הוסף תלמיד")
    popup.configure(bg='#e3e3e3')

    name_label = tk.Label(popup, text="שם התלמיד:", bg='#e3e3e3', font=('Arial', 12))
    name_label.pack(pady=5)

    name_entry = tk.Entry(popup, font=('Arial', 12))
    name_entry.pack(pady=5)

    submit_button = tk.Button(popup, text="הוסף", command=submit, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
    submit_button.pack(pady=10)

def add_game_gui():
    def submit():
        player1_id = int(player1_id_entry.get())
        player2_id = int(player2_id_entry.get())
        result = result_entry.get()

        if result.lower() == 'תיקו':
            result = 0.5
        else:
            result = float(result)

        update_elo(player1_id, player2_id, result)
        refresh_table(tree)
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("הוסף משחק")
    popup.configure(bg='#e3e3e3')

    player1_id_label = tk.Label(popup, text="ID 1:", bg='#e3e3e3', font=('Arial', 12))
    player1_id_label.pack(pady=5)

    player1_id_entry = tk.Entry(popup, font=('Arial', 12))
    player1_id_entry.pack(pady=5)

    player2_id_label = tk.Label(popup, text="ID 2:", bg='#e3e3e3', font=('Arial', 12))
    player2_id_label.pack(pady=5)

    player2_id_entry = tk.Entry(popup, font=('Arial', 12))
    player2_id_entry.pack(pady=5)

    result_label = tk.Label(popup, text="תוצאה (1 לניצחון שחקן 1, 0.5 לתיקו, 0 לניצחון שחקן 2):", bg='#e3e3e3', font=('Arial', 12))
    result_label.pack(pady=5)

    result_entry = tk.Entry(popup, font=('Arial', 12))
    result_entry.pack(pady=5)

    submit_button = tk.Button(popup, text="הוסף", command=submit, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
    submit_button.pack(pady=10)

def update_elo_gui():
    def submit():
        student_id = int(student_id_entry.get())
        new_elo = int(new_elo_entry.get())
        update_elo_manually(student_id, new_elo)
        refresh_table(tree)
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("עדכן דירוג ELO ידני")
    popup.configure(bg='#e3e3e3')

    student_id_label = tk.Label(popup, text="מזהה תלמיד:", bg='#e3e3e3', font=('Arial', 12))
    student_id_label.pack(pady=5)

    student_id_entry = tk.Entry(popup, font=('Arial', 12))
    student_id_entry.pack(pady=5)

    new_elo_label = tk.Label(popup, text="דירוג ELO חדש:", bg='#e3e3e3', font=('Arial', 12))
    new_elo_label.pack(pady=5)

    new_elo_entry = tk.Entry(popup, font=('Arial', 12))
    new_elo_entry.pack(pady=5)

    submit_button = tk.Button(popup, text="עדכן", command=submit, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
    submit_button.pack(pady=10)

def delete_student_gui():
    def submit():
        student_id = int(student_id_entry.get())
        try:
            delete_student(student_id)
            refresh_table(tree)
        except ValueError as e:
            error_label.config(text=str(e))
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("מחק תלמיד")
    popup.configure(bg='#e3e3e3')

    student_id_label = tk.Label(popup, text="מזהה תלמיד:", bg='#e3e3e3', font=('Arial', 12))
    student_id_label.pack(pady=5)

    student_id_entry = tk.Entry(popup, font=('Arial', 12))
    student_id_entry.pack(pady=5)

    submit_button = tk.Button(popup, text="מחק", command=submit, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
    submit_button.pack(pady=10)

    error_label = tk.Label(popup, text="", fg="red", bg='#e3e3e3', font=('Arial', 12))
    error_label.pack(pady=5)

def display_leader():
    leader = get_leader()
    popup = tk.Toplevel()
    popup.title("המנצח")
    popup.configure(bg='#e3e3e3')

    leader_info = (
        f"שחקן: {leader['Name']}\n"
        f"ELO: {leader['ELO']}\n"
        f"ניצחונות: {leader['Wins']}\n"
        f"הפסדים: {leader['Losses']}\n"
        f"תיקו: {leader['Draws']}\n"
        f"מס מזהה: {leader['ID']}"
    )

    leader_label = tk.Label(popup, text=leader_info, bg='#e3e3e3', font=('Arial', 12))
    leader_label.pack(pady=10)

root = tk.Tk()
root.title('ניהול דירוג Elo')

style = ttk.Style()
style.configure('Treeview',
                background='#ffffff',
                
                fieldbackground='#ffffff')
style.configure('Treeview.Heading',
                background='#4CAF50',
                
                font=('Arial', 12, 'bold'))
style.configure('TButton',
                background='#4CAF50',
                
                font=('Arial', 12, 'bold'))
style.configure('TButton:hover',
                background='#45a049')

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

columns = ('ID', 'Name', 'ELO', 'Date', 'Rank', 'Wins', 'Losses', 'Draws')
tree = ttk.Treeview(frame, columns=columns, show='headings', style='Treeview')
tree.tag_configure('oddrow', background='#f9f9f9')
tree.tag_configure('evenrow', background='#ffffff')
for col in columns:
    tree.heading(col, text=col, anchor='center')
    tree.column(col, width=100, anchor='center')
tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

button_frame = ttk.Frame(frame)
button_frame.grid(row=1, column=0, pady=10, sticky=tk.S)

add_student_button = ttk.Button(button_frame, text='הוסף תלמיד', command=add_student_gui, style='TButton')
add_student_button.grid(row=0, column=0, padx=5)

add_game_button = ttk.Button(button_frame, text='הוסף משחק', command=add_game_gui, style='TButton')
add_game_button.grid(row=0, column=1, padx=5)

update_elo_button = ttk.Button(button_frame, text='עדכן דירוג ידני', command=update_elo_gui, style='TButton')
update_elo_button.grid(row=0, column=2, padx=5)

sort_by_rank_button = ttk.Button(button_frame, text='מיין לפי דירוג', command=sort_by_rank, style='TButton')
sort_by_rank_button.grid(row=0, column=3, padx=5)

delete_student_button = ttk.Button(button_frame, text='מחק תלמיד', command=delete_student_gui, style='TButton')
delete_student_button.grid(row=0, column=4, padx=5)

display_leader_button = ttk.Button(button_frame, text='הראה מנצח', command=display_leader, style='TButton')
display_leader_button.grid(row=0, column=5, padx=5)

refresh_table(tree)
root.mainloop()
