import pandas as pd
from elo_calculator import calculate_elo
from datetime import datetime

CSV_FILE = 'students.csv'

def load_students():
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['ID', 'Name', 'ELO', 'Date', 'Rank', 'Wins', 'Losses', 'Draws'])
    return df



def save_students(df):
    df.to_csv(CSV_FILE, index=False)

def add_student(name):
    df = load_students()
    new_id = df['ID'].max() + 1 if not df.empty else 1
    new_student = pd.DataFrame({
        'ID': [new_id], 
        'Name': [name], 
        'ELO': [1000],
        'Date': [datetime.now().strftime('%Y-%m-%d')],
        'Rank': [0],  # עמודת דירוג שתמלא לאחר חישוב
        'Wins': [0],  # עמודת ניצחונות
        'Losses': [0],  # עמודת הפסדים
        'Draws': [0]   # עמודת תיקו
    })
    df = pd.concat([df, new_student], ignore_index=True)
    
    save_students(df)



def update_elo(winner_id, loser_id, result):
    df = load_students()

    if winner_id not in df['ID'].values or loser_id not in df['ID'].values:
        raise ValueError("ID of the winner or loser not found")

    winner = df[df['ID'] == winner_id].iloc[0]
    loser = df[df['ID'] == loser_id].iloc[0]
    
    if result == 1:  # ניצחון למנצח
        new_winner_elo = calculate_elo(winner['ELO'], loser['ELO'], 1)
        new_loser_elo = calculate_elo(loser['ELO'], winner['ELO'], 0)
    elif result == 0:  # ניצחון למפסיד
        new_winner_elo = calculate_elo(winner['ELO'], loser['ELO'], 0)
        new_loser_elo = calculate_elo(loser['ELO'], winner['ELO'], 1)
    else:  # תיקו
        new_winner_elo = winner['ELO'] + 5
        new_loser_elo = loser['ELO'] + 5

    df.loc[df['ID'] == winner_id, 'ELO'] = new_winner_elo
    df.loc[df['ID'] == loser_id, 'ELO'] = new_loser_elo
    df.loc[df['ID'] == winner_id, 'Date'] = datetime.now().strftime('%Y-%m-%d')
    df.loc[df['ID'] == loser_id, 'Date'] = datetime.now().strftime('%Y-%m-%d')

    # עדכון דירוגים
    df['Rank'] = df['ELO'].rank(ascending=False)

    save_students(df)

def update_elo_manually(student_id, new_elo):
    df = load_students()

    if student_id not in df['ID'].values:
        raise ValueError("ID של התלמיד לא נמצא")

    df.loc[df['ID'] == student_id, 'ELO'] = new_elo
    df.loc[df['ID'] == student_id, 'Date'] = datetime.now().strftime('%Y-%m-%d')

    # עדכון דירוגים
    df['Rank'] = df['ELO'].rank(ascending=False)

    save_students(df)

def delete_student(student_id):
    df = load_students()

    if student_id not in df['ID'].values:
        raise ValueError("ID של התלמיד לא נמצא")

    df = df[df['ID'] != student_id]

    # עדכון דירוגים לאחר מחיקה
    df['Rank'] = df['ELO'].rank(ascending=False)

    save_students(df)

def get_leader():
    df = load_students()

    if df.empty:
        raise ValueError("לא נמצאו תלמידים")

    leader = df.loc[df['ELO'].idxmax()]
    return leader