import streamlit as st
import random
import time
from games.utils import get_player_profile, update_player_profile

METADATA = {
    "id": "memory_match",
    "title": "🧠 Cosmic Memory Match",
    "author": "Команда Hub",
    "category": "Arcade",
    "description": "Класична гра на тренування пам'яті. Знайдіть пари космічних об'єктів за найменшу кількість ходів!",
    "image": "assets/memory_match.png",
    "tags": ["Пам'ять", "Космос", "Навчальна"]
}

EMOJIS = ['🚀', '👽', '👾', '🪐', '🛸', '🛰️', '📡', '☄️']

def init_game():
    # Double the list to make pairs
    cards = EMOJIS * 2
    random.shuffle(cards)
    st.session_state.mm_cards = cards
    st.session_state.mm_revealed = [False] * 16
    st.session_state.mm_selected = []
    st.session_state.mm_moves = 0
    st.session_state.mm_start_time = time.time()
    st.session_state.mm_game_won = False
    st.session_state.mm_elapsed_time = 0.0

def run():
    # Custom CSS for memory game buttons to make them square and style card backs
    st.markdown("""
    <style>
    /* Center and restrict the game container */
    .main .block-container {
        max-width: 520px !important;
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
    
    /* Card buttons grid sizing */
    div[data-testid="stHorizontalBlock"] {
        max-width: 500px !important;
        margin: 0 auto !important;
        gap: 10px !important;
    }
    
    /* Style cards */
    div[data-testid="column"] div[data-testid="stButton"] button {
        width: 110px !important;
        height: 110px !important;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 2.2rem !important;
        font-family: 'Outfit', sans-serif !important;
        border-radius: 14px !important;
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1) !important;
        background-color: rgba(22, 28, 45, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Active/hover hover card effects */
    div[data-testid="column"] div[data-testid="stButton"] button:hover {
        border-color: rgba(6, 182, 212, 0.4) !important;
        transform: scale(1.03) !important;
        box-shadow: 0 8px 16px rgba(6, 182, 212, 0.1) !important;
    }
    
    /* Distinct styling for revealed card backs and faces */
    /* Handled dynamically via labels */
    </style>
    """, unsafe_allow_html=True)

    st.title("🧠 Cosmic Memory Match")
    st.write("Знайдіть всі 8 пар однакових космічних об'єктів!")
    
    # Load profile data
    username = st.session_state.get("current_user", "Гість")
    profile = get_player_profile(username)
    
    if "memory_match" not in profile:
        profile["memory_match"] = {
            "best_moves": 999,
            "best_time": 9999.0,
            "games_played": 0
        }
    stats = profile["memory_match"]

    # Initialize game
    if "mm_cards" not in st.session_state:
        init_game()

    # Display game stats during play
    col_st1, col_st2, col_st3 = st.columns(3)
    col_st1.metric("Кількість ходів", st.session_state.mm_moves)
    
    # Calculate current elapsed time
    if not st.session_state.mm_game_won:
        elapsed = time.time() - st.session_state.mm_start_time
    else:
        elapsed = st.session_state.mm_elapsed_time
        
    col_st2.metric("Час гри", f"{elapsed:.1f} сек")
    
    best_moves_val = stats["best_moves"]
    if best_moves_val == 999:
        best_moves_val = "—"
    col_st3.metric("Рекорд класу (ходові)", best_moves_val)

    st.write("---")

    # Render 4x4 Grid
    cards = st.session_state.mm_cards
    revealed = st.session_state.mm_revealed
    selected = st.session_state.mm_selected

    for row in range(4):
        cols = st.columns(4)
        for col in range(4):
            idx = row * 4 + col
            
            # Decide what emoji/label to display on the button
            is_open = revealed[idx] or (idx in selected)
            
            # Card label
            btn_label = cards[idx] if is_open else "❓"
            
            # Styling for open/closed state
            is_disabled = is_open or st.session_state.mm_game_won
            
            # Unique button key
            if cols[col].button(btn_label, key=f"mm_card_{idx}", use_container_width=True, disabled=is_disabled):
                # Handle click
                # If 2 cards are already temporarily open, close them on this next click
                if len(selected) == 2:
                    selected.clear()
                    
                selected.append(idx)
                
                # Check for match when 2 cards selected
                if len(selected) == 2:
                    st.session_state.mm_moves += 1
                    idx1, idx2 = selected[0], selected[1]
                    if cards[idx1] == cards[idx2]:
                        # Match!
                        revealed[idx1] = True
                        revealed[idx2] = True
                        selected.clear()
                        
                        # Check win condition
                        if all(revealed):
                            st.session_state.mm_game_won = True
                            st.session_state.mm_elapsed_time = time.time() - st.session_state.mm_start_time
                            
                            # Save to profile!
                            stats["games_played"] += 1
                            if st.session_state.mm_moves < stats["best_moves"]:
                                stats["best_moves"] = st.session_state.mm_moves
                            if st.session_state.mm_elapsed_time < stats["best_time"]:
                                stats["best_time"] = round(st.session_state.mm_elapsed_time, 1)
                                
                            profile["memory_match"] = stats
                            update_player_profile(username, profile)
                
                st.rerun()

    # Win Banner
    if st.session_state.mm_game_won:
        st.write("---")
        st.success(f"🎉 Вітаємо, {username}! Ви пройшли гру за **{st.session_state.mm_moves} ходів** та **{st.session_state.mm_elapsed_time:.1f} секунд**!")
        
        # Display record alerts
        if st.session_state.mm_moves <= stats["best_moves"] or st.session_state.mm_elapsed_time <= stats["best_time"]:
            st.balloons()
            st.toast("🏆 Новий ОСОБИСТИЙ РЕКОРД встановлено!", icon="🔥")
            
        if st.button("Зіграти знову", type="primary", use_container_width=True):
            init_game()
            st.rerun()
            
    # Reset Button
    if st.button("Перезапустити гру", use_container_width=True):
        init_game()
        st.rerun()
