import streamlit as st
import random
import time
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

def get_ai_move(board, difficulty="Середній"):
    empty_indices = [i for i, val in enumerate(board) if val == ""]
    if not empty_indices:
        return -1
        
    if difficulty == "Легкий":
        return random.choice(empty_indices)
        
    elif difficulty == "Середній":
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
    st.session_state.ttt_turn = "X"
    st.session_state.ttt_moves = 0
    st.session_state.ttt_start_time = time.time()
    st.session_state.ttt_elapsed_time = 0.0

def run():
    # Inject CSS to center the board and scoreboard and make buttons squares
    st.markdown("""
    <style>
    /* Center and restrict the game container */
    .main .block-container {
        max-width: 620px !important;
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
        max-width: 600px !important;
        margin: 0 auto !important;
        gap: 8px !important;
    }
    
    /* Format scoreboard columns margins */
    div[data-testid="column"] {
        padding: 5px !important;
    }
    
    /* Make only grid buttons (which are inside columns) rectangular */
    div[data-testid="column"] div[data-testid="stButton"] button {
        width: 180px !important;
        height: 100px !important;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 2.5rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        border-radius: 12px !important;
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
    
    /* Style the surrender button in column 3 to be pink */
    div[data-testid="column"]:nth-of-type(3) button {
        background-color: #f43f5e !important;
        color: #ffffff !important;
        border: none !important;
    }
    div[data-testid="column"]:nth-of-type(3) button:hover {
        background-color: #e11d48 !important;
        box-shadow: 0 4px 10px rgba(244, 63, 94, 0.3) !important;
    }
    
    /* Custom status bar styling */
    .ttt-status-bar {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        padding: 8px 12px;
        border-radius: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
        box-shadow: 0 4px 6px var(--shadow-color);
    }
    .ttt-badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.82rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    .ttt-badge.pink {
        background-color: #f43f5e;
        color: #ffffff !important;
    }
    .ttt-badge.dark {
        background-color: var(--border-color);
        color: var(--text-color) !important;
    }
    .ttt-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-color);
        font-family: 'Space Grotesk', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<h2 style="text-align:center; font-family:\'Space Grotesk\', sans-serif; color:var(--text-color); margin-bottom:15px;">Хрестики-нолики (З вибором складності)</h2>', unsafe_allow_html=True)
    
    # Load profile data
    username = st.session_state.get("current_user", "Гість")
    profile = get_player_profile(username)
    
    # Make sure we have the correct nested dict
    if "tic_tac_toe" not in profile:
        profile["tic_tac_toe"] = {"wins": 0, "losses": 0, "ties": 0, "streak": 0}
        
    ttt_stats = profile["tic_tac_toe"]
    streak = ttt_stats.get("streak", 0)
    
    # Initialize session state for Tic-Tac-Toe
    if "ttt_board" not in st.session_state:
        reset_game()
        
    board = st.session_state.ttt_board
    winner = st.session_state.ttt_winner
    
    # Controls row
    col_diff, col_restart, col_surrender, col_reset = st.columns([1.6, 1.0, 1.0, 1.0])
    
    with col_diff:
        difficulty = st.selectbox(
            "Складність:",
            ["Легкий", "Середній", "Нереальний (Ідеальний)"],
            index=1,
            label_visibility="collapsed",
            key="ttt_difficulty"
        )
        
    with col_restart:
        if st.button("Почати заново", key="btn_restart", use_container_width=True):
            reset_game()
            st.rerun()
            
    with col_surrender:
        # Player surrenders -> loses game
        is_surrender_disabled = (winner is not None)
        if st.button("Здатися 🏳️", key="btn_surrender", use_container_width=True, disabled=is_surrender_disabled):
            st.session_state.ttt_winner = "O"
            st.session_state.ttt_elapsed_time = time.time() - st.session_state.ttt_start_time
            ttt_stats["losses"] += 1
            ttt_stats["streak"] = streak + 1
            profile["tic_tac_toe"] = ttt_stats
            update_player_profile(username, profile)
            st.rerun()
            
    with col_reset:
        if st.button("Скинути рахунок", key="btn_reset", use_container_width=True):
            profile["tic_tac_toe"] = {"wins": 0, "losses": 0, "ties": 0, "streak": 0}
            update_player_profile(username, profile)
            reset_game()
            st.rerun()
            
    # Calculate elapsed time
    if winner is None:
        elapsed = time.time() - st.session_state.ttt_start_time
    else:
        elapsed = st.session_state.ttt_elapsed_time

    # Render custom status bar matching screenshot
    if winner is None:
        turn_text = f"ХІД: {st.session_state.ttt_turn} | {difficulty}"
    else:
        turn_text = "ГРА ЗАВЕРШЕНА"
        
    status_bar_html = f"""
    <div class="ttt-status-bar">
        <span class="ttt-badge pink">{turn_text}</span>
        <span class="ttt-badge dark">Рахунок: <span style="color:#f43f5e;">{ttt_stats['wins']}</span> - <span style="color:#3b82f6;">{ttt_stats['losses']}</span> - <span style="color:#94a3b8;">{ttt_stats['ties']}</span></span>
        <span class="ttt-label">Хід: {st.session_state.ttt_moves}</span>
        <span class="ttt-label">Час: {elapsed:.1f}s</span>
    </div>
    """
    st.markdown(status_bar_html, unsafe_allow_html=True)
    
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
                
            is_disabled = (winner is not None) or (cell_value != "") or (st.session_state.ttt_turn == "O")
            
            if cols[col].button(btn_label, key=f"cell_{idx}", disabled=is_disabled):
                # Player moves
                board[idx] = "X"
                st.session_state.ttt_moves += 1
                st.session_state.ttt_elapsed_time = time.time() - st.session_state.ttt_start_time
                winner = check_winner(board)
                
                if winner:
                    st.session_state.ttt_winner = winner
                    if winner == "X":
                        ttt_stats["wins"] += 1
                        ttt_stats["streak"] = 0
                    elif winner == "Tie":
                        ttt_stats["ties"] += 1
                        ttt_stats["streak"] = streak + 1
                    
                    profile["tic_tac_toe"] = ttt_stats
                    update_player_profile(username, profile)
                else:
                    st.session_state.ttt_turn = "O"
                st.rerun()
 
    # AI Turn logic
    if st.session_state.ttt_turn == "O" and winner is None:
        ai_idx = get_ai_move(board, difficulty)
        if ai_idx != -1:
            board[ai_idx] = "O"
            st.session_state.ttt_moves += 1
            st.session_state.ttt_elapsed_time = time.time() - st.session_state.ttt_start_time
            winner = check_winner(board)
            
            if winner:
                st.session_state.ttt_winner = winner
                if winner == "O":
                    ttt_stats["losses"] += 1
                    ttt_stats["streak"] = streak + 1
                elif winner == "Tie":
                    ttt_stats["ties"] += 1
                    ttt_stats["streak"] = streak + 1
                
                profile["tic_tac_toe"] = ttt_stats
                update_player_profile(username, profile)
            
        st.session_state.ttt_turn = "X"
        st.rerun()
        
    st.write("")
    
    # Bottom status messages matching screenshot, but in Ukrainian
    if winner is None:
        st.markdown(f'<div style="text-align:center; color:#22c55e; font-weight:bold; font-size:1.1rem;">Гра почалася. Складність: {difficulty}. Першим ходить: X</div>', unsafe_allow_html=True)
    elif winner == "X":
        st.markdown(f'<div style="text-align:center; color:#22c55e; font-weight:bold; font-size:1.1rem;">Вітаємо! Ви перемогли ШІ на складності {difficulty}!</div>', unsafe_allow_html=True)
        st.balloons()
    elif winner == "O":
        st.markdown(f'<div style="text-align:center; color:#f43f5e; font-weight:bold; font-size:1.1rem;">ШІ переміг на складності {difficulty}. Спробуйте ще раз!</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align:center; color:#3b82f6; font-weight:bold; font-size:1.1rem;">Нічия на складності {difficulty}! Хороша гра.</div>', unsafe_allow_html=True)
        
    st.markdown(f'<div style="text-align:center; color:#3b82f6; font-size:0.95rem; margin-top:5px;">Серія без перемог над ботом: {streak}</div>', unsafe_allow_html=True)
