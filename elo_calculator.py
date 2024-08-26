def calculate_elo(current_elo, opponent_elo, result, K=30):
    if result == 0.5:
        return current_elo  # אם התוצאה תיקו, לא משנה את הדירוג
    
    expected_score = 1 / (1 + 10 ** ((opponent_elo - current_elo) / 400))
    return current_elo + K * (result - expected_score)
