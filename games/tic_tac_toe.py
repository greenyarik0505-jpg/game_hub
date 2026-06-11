import streamlit as st
import random
from games.utils import get_player_profile, update_player_profile

METADATA = {
    "id": "tic_tac_toe",
    "title": "🎮 Tic-Tac-Toe",
    "author": "Команда Hub",
    "category": "Board",
    "description": "Класична гра 'Хрестики-Нулики' проти розумного та непередбачуваного ШІ.",
    "image": "assets/tic_tac_toe.jpg",
    "tags": ["ШІ", "Настільна", "Ретро"]
}

def check_winner(board):
    # Check rows, columns, and diagonals
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != "":
            return board[line[0]]
    if "" not in board:
        return "Tie"
    return None

def evaluate_board(board):
    winner = check_winner(board)
    if winner == "O":
        return 10
    elif winner == "X":
        return -10
    return 0

def minimax(board, depth, is_maximizing):
    score = evaluate_board(board)
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if "" not in board:
        return 0
        
    if is_maximizing:
        best = -1000
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                best = max(best, minimax(board, depth + 1, False))
                board[i] = ""
        return best
    else:
        best = 1000
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best = min(best, minimax(board, depth + 1, True))
                board[i] = ""
        return best

def find_best_move(board):
    best_val = -1000
    best_move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            move_val = minimax(board, 0, False)
            board[i] = ""
            if move_val > best_val:
                best_val = move_val
                best_move = i
    return best_move

def get_ai_move(board, difficulty="Розумний 🧠"):
    empty_indices = [i for i, val in enumerate(board) if val == ""]
    if not empty_indices:
        return -1
        
    if difficulty == "Легкий 👤":
        return random.choice(empty_indices)
        
    elif difficulty == "Розумний 🧠":
        # 1. Check if AI can win in the next move
        for idx in empty_indices:
            temp_board = list(board)
            temp_board[idx] = "O"
            if check_winner(temp_board) == "O":
                return idx
                
        # 2. Check if Player can win and block them
        for idx in empty_indices:
            temp_board = list(board)
            temp_board[idx] = "X"
            if check_winner(temp_board) == "X":
                return idx
                
        # 3. Take center if available
        if 4 in empty_indices:
            return 4
            
        # 4. Take corners if available
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if c in empty_indices]
        if available_corners:
            return random.choice(available_corners)
            
        # 5. Take random
        return random.choice(empty_indices)
        
    else:
        # Impossible mode using minimax algorithm
        return find_best_move(board)

def reset_game():
    st.session_state.ttt_board = [""] * 9
    st.session_state.ttt_winner = None
    st.session_state.ttt_turn = "Player"

def run():
    # Inject CSS to center the board and scoreboard and make buttons squares
    st.markdown("""
    <style>
    /* Center and restrict the game container */
    .main .block-container {
        max-width: 480px !important;
        margin: 0 auto !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
    }
    
    /* Keep the top bar stretched to full viewport width */
    .game-top-bar {
        width: 100vw !important;
        margin-left: calc(-50vw + 50%) !important;
        margin-right: calc(-50vw + 50%) !important;
        left: 0 !important;
        box-sizing: border-box !important;
    }
    
    /* Align the 3x3 columns tightly and center them */
    div[data-testid="stHorizontalBlock"] {
        max-width: 460px !important;
        margin: 0 auto !important;
        gap: 8px !important;
    }
    
    /* Format scoreboard columns margins */
    div[data-testid="column"] {
        padding: 5px !important;
    }
    
    /* Make only grid buttons (which are inside columns) perfect squares */
    div[data-testid="column"] div[data-testid="stButton"] button {
        width: 140px !important;
        height: 140px !important;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 3rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        border-radius: 16px !important;
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-color) !important;
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1) !important;
        box-shadow: 0 4px 6px var(--shadow-color) !important;
    }
    
    div[data-testid="column"] div[data-testid="stButton"] button:hover {
        background: var(--bg-color) !important;
        border-color: var(--primary-color) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 6px 15px var(--shadow-color) !important;
    }
    
    div[data-testid="column"] div[data-testid="stButton"] button:disabled {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        opacity: 1.0 !important;
        border-color: var(--border-color) !important;
        cursor: not-allowed !important;
    }
    
    div[data-testid="column"] div[data-testid="stButton"] button:active {
        transform: scale(0.98) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_hdr_l, col_hdr_r = st.columns([1.5, 1.0])
    with col_hdr_l:
        st.title("🎮 Tic-Tac-Toe")
        st.write("Зіграйте проти ШІ! Чи зможете ви перемогти?")
    with col_hdr_r:
        difficulty = st.selectbox(
            "Складність ШІ:",
            ["Легкий 👤", "Розумний 🧠", "Неможливий 🤖"],
            index=1,
            key="ttt_difficulty"
        )
    
    # Load profile data
    username = st.session_state.get("current_user", "Гість")
    profile = get_player_profile(username)
    
    # Make sure we have the correct nested dict
    if "tic_tac_toe" not in profile:
        profile["tic_tac_toe"] = {"wins": 0, "losses": 0, "ties": 0}
        
    ttt_stats = profile["tic_tac_toe"]
    
    # Initialize session state for Tic-Tac-Toe
    if "ttt_board" not in st.session_state:
        reset_game()
        
    board = st.session_state.ttt_board
    winner = st.session_state.ttt_winner
    
    # Display scores from profile
    col1, col2, col3 = st.columns(3)
    col1.metric("Ви перемог (❌)", ttt_stats["wins"])
    col2.metric("ШІ (⭕)", ttt_stats["losses"])
    col3.metric("Нічиї", ttt_stats["ties"])
    
    st.write("---")
    
    # Render the game grid
    for row in range(3):
        cols = st.columns([1, 1, 1])
        for col in range(3):
            idx = row * 3 + col
            cell_value = board[idx]
            
            btn_label = " "
            if cell_value == "X":
                btn_label = "❌"
            elif cell_value == "O":
                btn_label = "⭕"
                
            is_disabled = (winner is not None) or (cell_value != "") or (st.session_state.ttt_turn == "AI")
            
            if cols[col].button(btn_label, key=f"cell_{idx}", use_container_width=True, disabled=is_disabled):
                # Player moves
                board[idx] = "X"
                winner = check_winner(board)
                
                if winner:
                    st.session_state.ttt_winner = winner
                    if winner == "X":
                        ttt_stats["wins"] += 1
                    elif winner == "Tie":
                        ttt_stats["ties"] += 1
                    
                    profile["tic_tac_toe"] = ttt_stats
                    update_player_profile(username, profile)
                else:
                    st.session_state.ttt_turn = "AI"
                st.rerun()
 
    # AI Turn logic
    if st.session_state.ttt_turn == "AI" and winner is None:
        ai_idx = get_ai_move(board, difficulty)
        if ai_idx != -1:
            board[ai_idx] = "O"
            winner = check_winner(board)
            
            if winner:
                st.session_state.ttt_winner = winner
                if winner == "O":
                    ttt_stats["losses"] += 1
                elif winner == "Tie":
                    ttt_stats["ties"] += 1
                
                profile["tic_tac_toe"] = ttt_stats
                update_player_profile(username, profile)
            
        st.session_state.ttt_turn = "Player"
        st.rerun()
        
    # Game Over status
    if winner:
        st.write("---")
        if winner == "X":
            st.success("🎉 Ви перемогли! Вітаємо!")
            st.balloons()
        elif winner == "O":
            st.error("💀 ШІ переміг. Спробуйте ще раз!")
        else:
            st.info("🤝 Нічия!")
            
        if st.button("Грати знову", type="primary", use_container_width=True):
            reset_game()
            st.rerun()
            
    # Reset Score button
    if st.button("Скинути статистику", use_container_width=True):
        profile["tic_tac_toe"] = {"wins": 0, "losses": 0, "ties": 0}
        update_player_profile(username, profile)
        reset_game()
        st.rerun()
