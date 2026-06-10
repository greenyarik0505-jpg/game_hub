import streamlit as st
import json
import importlib
import importlib.util
import types
import os
import base64
import re
import sys
from games.utils import load_profiles, get_player_profile, update_player_profile
import ast

# Set page configurations
st.set_page_config(
    page_title="Streamlit Game Hub",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Helper function to inject custom CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inject custom styling
local_css("style.css")

# Helper function to clean and render HTML safely in Streamlit
def render_html(html_str):
    cleaned = html_str.replace("\n", " ")
    cleaned = re.sub(r'\s+', ' ', cleaned)
    st.markdown(cleaned, unsafe_allow_html=True)

# Render background floating ambient orbs globally
render_html("""
<div class="bg-orb orb-1"></div>
<div class="bg-orb orb-2"></div>
<div class="bg-orb orb-3"></div>
""")

# Dynamic Game Scanner (No games.json needed)
def scan_games():
    games_list = []
    games_dir = "games"
    if not os.path.exists(games_dir):
        return games_list
    
    for filename in sorted(os.listdir(games_dir)):
        if filename.endswith(".py") and not filename.startswith("__") and filename != "utils.py":
            module_id = filename[:-3]
            module_name = f"games.{module_id}"
            file_path = os.path.join(games_dir, filename)
            
            try:
                # 1. Parse file using AST to extract METADATA and check for run() function without executing top-level code!
                metadata = {}
                has_run = False
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=file_path)
                    for node in tree.body:
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name) and target.id == "METADATA":
                                    metadata = ast.literal_eval(node.value)
                        elif isinstance(node, ast.FunctionDef) and node.name == "run":
                            has_run = True
                except Exception as e:
                    # Let syntax/parse errors bubble up to broken status representation
                    raise e
                
                game_data = {
                    "id": metadata.get("id", module_id),
                    "title": metadata.get("title", module_id.replace("_", " ").title()),
                    "author": metadata.get("author", "Невідомий"),
                    "category": metadata.get("category", "Arcade"),
                    "description": metadata.get("description", "Опис гри відсутній."),
                    "image": metadata.get("image", None),
                    "tags": metadata.get("tags", []),
                    "module": module_name,
                    "status": "active",
                    "has_run": has_run
                }
                games_list.append(game_data)
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                # Broken game node representation
                games_list.append({
                    "id": module_id,
                    "title": module_id.replace("_", " ").title(),
                    "author": "Невідомий",
                    "category": "Broken",
                    "description": "Ця гра зламалася при компіляції або запуску. Натисніть, щоб відкрити термінал розробника.",
                    "image": None,
                    "tags": ["Broken", "Error"],
                    "module": module_name,
                    "status": "broken",
                    "error_trace": error_trace,
                    "has_run": False
                })
    return games_list

# Load the dynamic games list
games = scan_games()

# Helper for Ratings read/write
def load_ratings():
    ratings_file = "ratings.json"
    if os.path.exists(ratings_file):
        try:
            with open(ratings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_rating(game_id, rating_val):
    ratings_file = "ratings.json"
    ratings = load_ratings()
    if game_id not in ratings:
        ratings[game_id] = []
    if 1 <= rating_val <= 5:
        ratings[game_id].append(rating_val)
    try:
        with open(ratings_file, "w", encoding="utf-8") as f:
            json.dump(ratings, f, indent=2)
    except Exception as e:
        st.error(f"Error saving rating: {e}")

# Helper to get base64 encoded image
def get_base64_image(path):
    if path and os.path.exists(path):
        try:
            with open(path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                mime_type = "image/png" if path.endswith(".png") else "image/jpeg"
                return f"data:{mime_type};base64,{encoded}"
        except:
            pass
    return None

# Get Logo HTML
def get_logo_html():
    logo_data = get_base64_image("assets/logo.png")
    if logo_data:
        return f'<img src="{logo_data}" class="hub-logo" alt="Game Hub Logo">'
    return '<h1 class="hub-title">STREAMLIT GAME HUB</h1>'

def get_game_cover_html(game):
    image_path = game.get("image", "")
    img_data = get_base64_image(image_path)
    if img_data:
        return f'<img src="{img_data}" class="game-cover-image" alt="{game["title"]}">'
            
    # Fallback if image not found
    game_id = game["id"]
    FALLBACKS = {
        "tic_tac_toe": {
            "gradient": "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
            "emoji": "❌⭕"
        },
        "clicker": {
            "gradient": "linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)",
            "emoji": "🪙"
        },
        "memory_match": {
            "gradient": "linear-gradient(135deg, #6366f1 0%, #ec4899 100%)",
            "emoji": "🧠"
        },
        "template": {
            "gradient": "linear-gradient(135deg, #10b981 0%, #06b6d4 100%)",
            "emoji": "💻"
        }
    }
    fallback = FALLBACKS.get(game_id, {
        "gradient": "linear-gradient(135deg, #ef4444 0%, #f59e0b 100%)" if game.get("status") == "broken" else "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
        "emoji": "⚠️" if game.get("status") == "broken" else "🎮"
    })
    
    return f"""
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: {fallback['gradient']};">
        <div class="game-cover-fallback">{fallback['emoji']}</div>
    </div>
    """

# Generate a unique deterministic gradient avatar from username
def get_avatar_html(username, size=50):
    gradients = [
        "linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)",
        "linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)",
        "linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)",
        "linear-gradient(135deg, #f59e0b 0%, #ec4899 100%)",
        "linear-gradient(135deg, #10b981 0%, #06b6d4 100%)",
        "linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%)"
    ]
    emojis = ["🎮", "👾", "🚀", "🛡️", "🐱", "⚡", "🧠", "🔥", "🏆", "🌟", "🧙", "🐱‍💻", "🦉", "🦁", "🐼", "🤖"]
    
    user_hash = sum(ord(c) for c in username)
    gradient = gradients[user_hash % len(gradients)]
    emoji = emojis[user_hash % len(emojis)]
    
    return f"""
    <div class="user-avatar" style="
        width: {size}px; 
        height: {size}px; 
        border-radius: 50%; 
        background: {gradient}; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        font-size: {int(size * 0.5)}px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        border: 2px solid rgba(255,255,255,0.15);
    ">
        {emoji}
    </div>
    """

# Initialize Player Profile
query_params = st.query_params
if "current_user" not in st.session_state:
    if "user" in query_params:
        st.session_state.current_user = query_params["user"]
    else:
        st.session_state.current_user = "Гість"

active_user = st.session_state.current_user
user_profile = get_player_profile(active_user)
st.session_state.user_profile = user_profile

# Process ratings query parameters
query_params = st.query_params
active_page = query_params.get("page", "menu")

if active_page != "menu" and "rate" in query_params:
    try:
        rate_val = int(query_params["rate"])
        save_rating(active_page, rate_val)
        del st.query_params["rate"]
        st.toast(f"Дякуємо за вашу оцінку {rate_val} ⭐!", icon="💖")
        st.rerun()
    except Exception as e:
        pass

if active_page == "menu":
    # --- RENDER MAIN MENU LAUNCHER ---
    
    # 1. Header & Profile Selector Area
    avatar_html = get_avatar_html(active_user, size=46)
    
    # Check if we should show the sign-in form
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
        
    # Render layout columns for header top bar
    col_hdr_left, col_hdr_right = st.columns([2, 1])
    
    with col_hdr_right:
        # Create a premium glassmorphic Profile Card
        render_html(f"""
        <div class="profile-card">
            <div style="display: flex; align-items: center; gap: 12px;">
                {avatar_html}
                <div>
                    <div style="font-size: 0.8rem; color: #64748b; font-weight: 500;">ГРАВЕЦЬ</div>
                    <div style="font-size: 1.1rem; color: #fff; font-weight: 700; font-family: 'Space Grotesk', sans-serif;">{active_user}</div>
                </div>
            </div>
        </div>
        """)
        
        # Action Buttons
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            if active_user == "Гість":
                if st.button("🗝️ Ввійти", key="btn_show_login", use_container_width=True):
                    st.session_state.show_login = not st.session_state.show_login
                    st.rerun()
            else:
                if st.button("🚪 Вийти", key="btn_logout", use_container_width=True):
                    st.session_state.current_user = "Гість"
                    st.query_params["user"] = "Гість"
                    # Reset game states so new login doesn't inherit clicked values
                    for k in list(st.session_state.keys()):
                        if k not in ["current_user", "show_login"]:
                            del st.session_state[k]
                    st.rerun()
        with sub_col2:
            # Simple link to school web or stats
            st.button("⚙️ Налаштування", key="btn_settings", disabled=True, use_container_width=True)

        if st.session_state.show_login:
            # Login Form
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            new_user = st.text_input("Введіть ваше ім'я / нікнейм:", placeholder="Нікнейм...")
            if st.button("Приєднатися", type="primary", use_container_width=True):
                cleaned_name = new_user.strip()
                if cleaned_name and cleaned_name.lower() != "гість":
                    st.session_state.current_user = cleaned_name
                    st.query_params["user"] = cleaned_name
                    st.session_state.show_login = False
                    # Force reload stats from utils
                    get_player_profile(cleaned_name)
                    # Clear session variables
                    for k in list(st.session_state.keys()):
                        if k not in ["current_user", "show_login"]:
                            del st.session_state[k]
                    st.rerun()
                elif cleaned_name.lower() == "гість":
                    st.warning("Ім'я 'Гість' зарезервоване. Будь ласка, оберіть інше ім'я.")
            st.markdown('</div>', unsafe_allow_html=True)
            
    with col_hdr_left:
        logo_html = get_logo_html()
        render_html(f"""
        <div class="hub-title-container">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 5px;">
                {logo_html}
            </div>
            <p class="hub-subtitle" style="text-align: left; margin: 0;">Інтерактивна консоль учнівських ігор. Домен готовий до запуску!</p>
        </div>
        """)
        
    render_html('<div class="neon-line" style="width: 100%; margin-top: 15px; margin-bottom: 30px;"></div>')

    # Layout: left is game cards grid, right is leaderboard!
    col_main_grid, col_leaderboard = st.columns([2.2, 1.2])

    with col_main_grid:
        st.markdown('<h2 style="font-family:\'Space Grotesk\', sans-serif; font-size:1.6rem; color:#fff; margin-bottom: 20px;">🎮 Доступні ігри</h2>', unsafe_allow_html=True)
        
        # Inject style to box search/category nicely
        render_html("""
        <style>
        .filter-panel {
            background: rgba(22, 28, 45, 0.25) !important;
            padding: 15px 20px !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.03) !important;
            margin-bottom: 25px !important;
        }
        </style>
        """)
        
        st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
        col_search, col_cats = st.columns([1.1, 1.3])
        
        with col_search:
            search_query = st.text_input(
                "Пошук",
                placeholder="🔍 Знайди за назвою чи тегом...",
                label_visibility="collapsed"
            )
            
        with col_cats:
            categories = ["All", "Arcade", "Board", "Strategy"]
            if "selected_category" not in st.session_state:
                st.session_state.selected_category = "All"
                
            cols = st.columns(len(categories))
            for idx, cat in enumerate(categories):
                is_active = (st.session_state.selected_category == cat)
                btn_type = "primary" if is_active else "secondary"
                if cols[idx].button(cat, key=f"btn_{cat}", type=btn_type, use_container_width=True):
                    st.session_state.selected_category = cat
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
                    
        # Filter games
        filtered_games = []
        search_lower = search_query.lower()
        selected_cat = st.session_state.selected_category
        
        for game in games:
            match_search = (
                search_lower in game["title"].lower() or
                search_lower in game["author"].lower() or
                search_lower in game["description"].lower() or
                any(search_lower in tag.lower() for tag in game.get("tags", []))
            )
            # Handle categories (Broken category matches All only or explicitly if filtered)
            match_category = (selected_cat == "All" or game["category"] == selected_cat)
            
            if match_search and match_category:
                filtered_games.append(game)
                
        # Load ratings
        ratings_db = load_ratings()
                
        # Render Games Grid
        if filtered_games:
            grid_html = '<div class="game-grid" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;">'
            for game in filtered_games:
                cover_html = get_game_cover_html(game)
                
                # Rating Badge
                game_ratings = ratings_db.get(game["id"], [])
                if game_ratings:
                    avg_val = sum(game_ratings) / len(game_ratings)
                    rating_badge = f'<span class="rating-display">⭐ {avg_val:.1f} ({len(game_ratings)})</span>'
                else:
                    rating_badge = '<span class="rating-display" style="color:#6e6a85">⭐ 0.0 (0)</span>'
                
                tags_html = ""
                for tag in game.get("tags", []):
                    tags_html += f'<span class="game-tag">{tag}</span>'
                
                # Dynamic Card Classes for styling
                card_class = f"game-card card-{game['id']}"
                if game.get("status") == "broken":
                    card_class += " broken-card"
                    
                play_text = "🔧 Логи" if game.get("status") == "broken" else "🎮 Грати"
                
                grid_html += f"""
                <a href="/?page={game['id']}&user={active_user}" target="_self" class="{card_class}" style="height: 380px;">
                    <div class="game-cover-container" style="height: 150px;">
                        {cover_html}
                        <span class="game-category-badge">{game['category']}</span>
                    </div>
                    <div class="game-content" style="padding: 15px;">
                        <div>
                            <div class="game-meta">
                                <span class="game-author">👤 {game['author']}</span>
                                {rating_badge}
                            </div>
                            <h3 class="game-card-title" style="font-size:1.2rem;">{game['title']}</h3>
                            <p class="game-card-desc" style="font-size:0.82rem; -webkit-line-clamp: 2;">{game['description']}</p>
                        </div>
                        <div>
                            <div class="game-tags" style="margin-bottom: 10px;">
                                {tags_html}
                            </div>
                            <div class="play-action" style="padding: 8px 15px; font-size:0.85rem;">
                                <span>{play_text}</span>
                            </div>
                        </div>
                    </div>
                </a>
                """
            grid_html += '</div>'
            render_html(grid_html)
        else:
            st.warning("Ігор не знайдено.")

    with col_leaderboard:
        st.markdown('<h2 style="font-family:\'Space Grotesk\', sans-serif; font-size:1.6rem; color:#fff; margin-bottom: 20px;">🏆 Таблиця лідерів класу</h2>', unsafe_allow_html=True)
        
        # Load all profiles
        all_profiles = load_profiles()
        
        # Tabs for different leaderboards
        tab_clicker, tab_ttt, tab_memory = st.tabs(["🪙 Клікер", "❌ Tic-Tac-Toe", "🧠 Memory Match"])
        
        with tab_clicker:
            # Sort by Clicker Coins
            clicker_ranks = []
            for user, data in all_profiles.items():
                coins = data.get("clicker", {}).get("coins", 0.0)
                clicker_ranks.append((user, coins))
            
            clicker_ranks = sorted(clicker_ranks, key=lambda x: x[1], reverse=True)[:10]
            
            if clicker_ranks:
                rows_html = ""
                for idx, (user, val) in enumerate(clicker_ranks):
                    badge = "👑" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}"
                    rows_html += f"""
                    <tr>
                        <td style="padding: 10px; font-weight:bold; color:#f59e0b;">{badge}</td>
                        <td style="padding: 10px;">{user}</td>
                        <td style="padding: 10px; text-align:right; font-family:'Space Grotesk'; font-weight:600; color:#06b6d4;">🪙 {val:.2f}</td>
                    </tr>
                    """
                
                render_html(f"""
                <table style="width:100%; border-collapse:collapse; background:rgba(22, 28, 45, 0.2); border-radius:12px; overflow:hidden; border: 1px solid rgba(255,255,255,0.03);">
                    <tr style="background:rgba(22, 28, 45, 0.4); border-bottom:1px solid rgba(255,255,255,0.05); text-align:left;">
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem;">РАНГ</th>
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem;">УЧЕНЬ</th>
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem; text-align:right;">БАЛАНС</th>
                    </tr>
                    {rows_html}
                </table>
                """)
            else:
                st.write("Статистика відсутня.")
                
        with tab_ttt:
            # Sort by Tic-Tac-Toe Wins
            ttt_ranks = []
            for user, data in all_profiles.items():
                wins = data.get("tic_tac_toe", {}).get("wins", 0)
                losses = data.get("tic_tac_toe", {}).get("losses", 0)
                ttt_ranks.append((user, wins, losses))
                
            ttt_ranks = sorted(ttt_ranks, key=lambda x: x[1], reverse=True)[:10]
            
            if ttt_ranks:
                rows_html = ""
                for idx, (user, wins, losses) in enumerate(ttt_ranks):
                    badge = "👑" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}"
                    rows_html += f"""
                    <tr>
                        <td style="padding: 10px; font-weight:bold; color:#f59e0b;">{badge}</td>
                        <td style="padding: 10px;">{user}</td>
                        <td style="padding: 10px; text-align:center; font-family:'Space Grotesk'; font-weight:600; color:#10b981;">{wins}</td>
                        <td style="padding: 10px; text-align:right; font-family:'Space Grotesk'; color:#64748b;">{losses}</td>
                    </tr>
                    """
                
                render_html(f"""
                <table style="width:100%; border-collapse:collapse; background:rgba(22, 28, 45, 0.2); border-radius:12px; overflow:hidden; border: 1px solid rgba(255,255,255,0.03);">
                    <tr style="background:rgba(22, 28, 45, 0.4); border-bottom:1px solid rgba(255,255,255,0.05); text-align:left;">
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem;">РАНГ</th>
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem;">УЧЕНЬ</th>
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem; text-align:center;">WINS</th>
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem; text-align:right;">LOSSES</th>
                    </tr>
                    {rows_html}
                </table>
                """)
            else:
                st.write("Статистика відсутня.")
                
        with tab_memory:
            # Sort by Memory Match Best Moves (Ascending, ignore default 999)
            mem_ranks = []
            for user, data in all_profiles.items():
                best_moves = data.get("memory_match", {}).get("best_moves", 999)
                best_time = data.get("memory_match", {}).get("best_time", 9999.0)
                if best_moves < 999:
                    mem_ranks.append((user, best_moves, best_time))
                    
            mem_ranks = sorted(mem_ranks, key=lambda x: x[1])[:10]
            
            if mem_ranks:
                rows_html = ""
                for idx, (user, moves, duration) in enumerate(mem_ranks):
                    badge = "👑" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}"
                    rows_html += f"""
                    <tr>
                        <td style="padding: 10px; font-weight:bold; color:#f59e0b;">{badge}</td>
                        <td style="padding: 10px;">{user}</td>
                        <td style="padding: 10px; text-align:center; font-family:'Space Grotesk'; font-weight:600; color:#ec4899;">{moves}</td>
                        <td style="padding: 10px; text-align:right; font-family:'Space Grotesk'; color:#3b82f6;">{duration:.1f}s</td>
                    </tr>
                    """
                
                render_html(f"""
                <table style="width:100%; border-collapse:collapse; background:rgba(22, 28, 45, 0.2); border-radius:12px; overflow:hidden; border: 1px solid rgba(255,255,255,0.03);">
                    <tr style="background:rgba(22, 28, 45, 0.4); border-bottom:1px solid rgba(255,255,255,0.05); text-align:left;">
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem;">РАНГ</th>
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem;">УЧЕНЬ</th>
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem; text-align:center;">MOVES</th>
                        <th style="padding: 12px 10px; color:#64748b; font-size:0.8rem; text-align:right;">TIME</th>
                    </tr>
                    {rows_html}
                </table>
                """)
            else:
                st.write("Статистика відсутня. Будьте першим, хто пройде Memory Match!")

else:
    # --- RENDER ACTIVE GAME ---
    game_metadata = next((g for g in games if g["id"] == active_page), None)
    
    if game_metadata:
        # Load ratings for top bar display
        ratings_db = load_ratings()
        game_ratings = ratings_db.get(active_page, [])
        if game_ratings:
            avg_val = sum(game_ratings) / len(game_ratings)
            current_rating_html = f'<span class="rating-display">⭐ {avg_val:.1f} ({len(game_ratings)})</span>'
        else:
            current_rating_html = '<span class="rating-display" style="color:#6e6a85">⭐ 0.0</span>'
            
        # Render premium 3-column top bar with rating voting links
        render_html(f"""
        <div class="game-top-bar">
            <div class="top-bar-left">
                <a href="/?page=menu&user={active_user}" target="_self" class="back-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                    Назад до меню
                </a>
            </div>
            <div class="top-bar-center">
                <div class="active-game-title">{game_metadata["title"]}</div>
                <div class="active-game-author">Розробник: {game_metadata["author"]}</div>
            </div>
            <div class="top-bar-right">
                <div class="rating-stars">
                    <span>Оцінити:</span>
                    <div class="stars-row">
                        <a href="/?page={active_page}&rate=1&user={active_user}" target="_self" class="star-link">⭐</a>
                        <a href="/?page={active_page}&rate=2&user={active_user}" target="_self" class="star-link">⭐</a>
                        <a href="/?page={active_page}&rate=3&user={active_user}" target="_self" class="star-link">⭐</a>
                        <a href="/?page={active_page}&rate=4&user={active_user}" target="_self" class="star-link">⭐</a>
                        <a href="/?page={active_page}&rate=5&user={active_user}" target="_self" class="star-link">⭐</a>
                    </div>
                    <span class="rating-val">{current_rating_html}</span>
                </div>
            </div>
        </div>
        """)
        
        # Inject style block to force 100% fullscreen canvas, removing side columns
        render_html("""
        <style>
        .main .block-container {
            max-width: 100vw !important;
            padding-left: 40px !important;
            padding-right: 40px !important;
            padding-top: 20px !important;
            padding-bottom: 40px !important;
            margin: 0 !important;
            animation: slideUp 0.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        }
        [data-testid="stSidebar"] {
            display: none !important;
        }
        </style>
        """)
        
        # Check if the game is flagged as broken, and render terminal console if so
        if game_metadata.get("status") == "broken":
            tb_str = game_metadata.get("error_trace", "Unknown traceback info.")
            render_html(f"""
            <div class="terminal-container">
                <div class="terminal-header">
                    <span class="terminal-dot red"></span>
                    <span class="terminal-dot yellow"></span>
                    <span class="terminal-dot green"></span>
                    <span class="terminal-title">SYSTEM ERROR CONSOLE - GAME: {game_metadata['title'].upper()}</span>
                </div>
                <div class="terminal-body">
                    <div class="terminal-line error-msg">❌ CRITICAL COMPILE/IMPORT EXCEPTION DETECTED</div>
                    <div class="terminal-line">----------------------------------------------------------------------</div>
                    <div class="terminal-line"><b>Message:</b> Failed to import or run game module {game_metadata['module']}</div>
                    <div class="terminal-line">----------------------------------------------------------------------</div>
                    <div class="terminal-line"><b>Python Stack Traceback:</b></div>
                    <pre class="terminal-code">{tb_str}</pre>
                    <div class="terminal-line">----------------------------------------------------------------------</div>
                    <div class="terminal-line tip">💡 <b>Порада щодо усунення помилки:</b> Перевірте файл <code>games/{game_metadata['id']}.py</code>. 
                    Переконайтеся, що всі бібліотеки встановлені, немає синтаксичних помилок і функція <code>run()</code> визначена правильно.</div>
                </div>
            </div>
            """)
        else:
            # Run the active student game
            try:
                module_name = game_metadata["module"]
                file_path = os.path.join("games", game_metadata["id"] + ".py")
                
                # 1. Mock set_page_config globally to prevent StreamlitAPIException
                original_set_page_config = st.set_page_config
                st.set_page_config = lambda *args, **kwargs: None
                
                try:
                    # 2. Setup module namespace without executing yet
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if spec is None:
                        raise ImportError(f"Could not load spec for {file_path}")
                    
                    if module_name in sys.modules:
                        game_module = sys.modules[module_name]
                    else:
                        game_module = importlib.util.module_from_spec(spec)
                        sys.modules[module_name] = game_module
                    
                    # 3. Choose execution path based on AST has_run detection
                    if game_metadata.get("has_run", False):
                        # Well-behaved code path (uses run() function)
                        game_module = importlib.reload(game_module)
                        game_module.run()
                    else:
                        # Raw top-level code execution pathway (runs as __main__)
                        with open(file_path, "r", encoding="utf-8") as f:
                            code_content = f.read()
                        
                        game_module.__dict__["__name__"] = "__main__"
                        exec(code_content, game_module.__dict__)
                finally:
                    # 4. Restore original page config
                    st.set_page_config = original_set_page_config
                
                # 5. Inject a CSS override to ensure any full-viewport custom iframes start below our top-bar
                st.markdown("""
                <style>
                iframe {
                    position: fixed !important;
                    top: 70px !important;
                    height: calc(100vh - 70px) !important;
                    z-index: 999999 !important;
                }
                .game-top-bar {
                    position: fixed !important;
                    top: 0 !important;
                    left: 0 !important;
                    width: 100vw !important;
                    z-index: 99999999 !important;
                    box-sizing: border-box !important;
                }
                .main .block-container {
                    padding-top: 80px !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                # Runtime crash inside running game
                import traceback
                tb_str = traceback.format_exc()
                
                render_html(f"""
                <div class="terminal-container">
                    <div class="terminal-header">
                        <span class="terminal-dot red"></span>
                        <span class="terminal-dot yellow"></span>
                        <span class="terminal-dot green"></span>
                        <span class="terminal-title">SYSTEM RUNTIME ERROR - GAME: {game_metadata['title'].upper()}</span>
                    </div>
                    <div class="terminal-body">
                        <div class="terminal-line error-msg">❌ CRITICAL RUNTIME EXCEPTION DETECTED DURING GAMEPLAY</div>
                        <div class="terminal-line">----------------------------------------------------------------------</div>
                        <div class="terminal-line"><b>Exception Message:</b> {str(e)}</div>
                        <div class="terminal-line">----------------------------------------------------------------------</div>
                        <div class="terminal-line"><b>Python Stack Traceback:</b></div>
                        <pre class="terminal-code">{tb_str}</pre>
                        <div class="terminal-line">----------------------------------------------------------------------</div>
                        <div class="terminal-line tip">💡 <b>Порада розробнику:</b> Стан сесії гри міг отримати некоректне значення. 
                        Переконайтеся, що всі ключі в <code>st.session_state</code> ініціалізовані і не викликають помилок ZeroDivision чи IndexError.</div>
                    </div>
                </div>
                """)
    else:
        st.error(f"Гру з ID '{active_page}' не знайдено.")
        st.markdown(f'<a href="/?page=menu&user={active_user}" target="_self" class="back-btn">⬅ Повернутися до меню</a>', unsafe_allow_html=True)
