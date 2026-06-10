import streamlit as st
import json
import importlib
import os
import base64
import re

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
    # Remove newlines and collapse multiple spaces into one space
    # This prevents the markdown parser from treating indented HTML as code blocks
    cleaned = html_str.replace("\n", " ")
    cleaned = re.sub(r'\s+', ' ', cleaned)
    st.markdown(cleaned, unsafe_allow_html=True)

# Render background floating ambient orbs globally
render_html("""
<div class="bg-orb orb-1"></div>
<div class="bg-orb orb-2"></div>
<div class="bg-orb orb-3"></div>
""")

# Load games configuration
def load_games_config():
    try:
        with open("games.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading games.json: {e}")
        return []

games = load_games_config()

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
    if os.path.exists(path):
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
    if image_path:
        img_data = get_base64_image(image_path)
        if img_data:
            return f'<img src="{img_data}" class="game-cover-image" alt="{game["title"]}">'
            
    # Fallback if image not found
    game_id = game["id"]
    FALLBACKS = {
        "tic_tac_toe": {
            "gradient": "linear-gradient(135deg, #8a2be2 0%, #4facfe 100%)",
            "emoji": "❌⭕"
        },
        "clicker": {
            "gradient": "linear-gradient(135deg, #ff007f 0%, #ffaa00 100%)",
            "emoji": "🪙"
        },
        "template": {
            "gradient": "linear-gradient(135deg, #27c93f 0%, #00f2fe 100%)",
            "emoji": "💻"
        }
    }
    fallback = FALLBACKS.get(game_id, {
        "gradient": "linear-gradient(135deg, #150e3a 0%, #291242 100%)",
        "emoji": "🎮"
    })
    
    return f"""
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: {fallback['gradient']};">
        <div class="game-cover-fallback">{fallback['emoji']}</div>
    </div>
    """

# Process incoming ratings if any
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
    logo_html = get_logo_html()
    render_html(f"""
    <div class="hub-container">
        <div class="hub-header">
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                {logo_html}
            </div>
            <p class="hub-subtitle">Найкращі ретро-ігри та аркади, створені нашими талановитими студентами</p>
            <div class="neon-line"></div>
        </div>
    </div>
    """)
    
    # Inject style to box the search and category filters together
    render_html("""
    <style>
    div[data-testid="stHorizontalBlock"] {
        background: rgba(22, 28, 45, 0.3) !important;
        padding: 20px 25px !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(25px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
        margin-bottom: 40px !important;
    }
    </style>
    """)
    
    # Render search and filter controls
    col_search, col_cats = st.columns([1, 1])
    
    with col_search:
        search_query = st.text_input(
            "Пошук",
            placeholder="🔍 Знайди гру за назвою, автором чи тегом...",
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
                
    # Filter the games list
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
        match_category = (selected_cat == "All" or game["category"] == selected_cat)
        
        if match_search and match_category:
            filtered_games.append(game)
            
    # Load all ratings to show on cards
    ratings_db = load_ratings()
            
    # Render Games Grid
    if filtered_games:
        grid_html = '<div class="game-grid">'
        for game in filtered_games:
            cover_html = get_game_cover_html(game)
            
            # Calculate rating
            game_ratings = ratings_db.get(game["id"], [])
            if game_ratings:
                avg_val = sum(game_ratings) / len(game_ratings)
                rating_badge = f'<span class="rating-display">⭐ {avg_val:.1f} ({len(game_ratings)})</span>'
            else:
                rating_badge = '<span class="rating-display" style="color:#6e6a85">⭐ 0.0 (0)</span>'
            
            tags_html = ""
            for tag in game.get("tags", []):
                tags_html += f'<span class="game-tag">{tag}</span>'
                
            grid_html += f"""
            <a href="/?page={game['id']}" target="_self" class="game-card card-{game['id']}">
                <div class="game-cover-container">
                    {cover_html}
                    <span class="game-category-badge">{game['category']}</span>
                </div>
                <div class="game-content">
                    <div>
                        <div class="game-meta">
                            <span class="game-author">👤 {game['author']}</span>
                            {rating_badge}
                        </div>
                        <h3 class="game-card-title">{game['title']}</h3>
                        <p class="game-card-desc">{game['description']}</p>
                    </div>
                    <div>
                        <div class="game-tags">
                            {tags_html}
                        </div>
                        <div class="play-action">
                            <span>🎮 Грати</span>
                        </div>
                    </div>
                </div>
            </a>
            """
        grid_html += '</div>'
        render_html(grid_html)
    else:
        st.warning("Ігор за вашим запитом не знайдено. Спробуйте змінити фільтри пошуку!")

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
            
        # 1. Render premium 3-column top bar with rating voting links
        render_html(f"""
        <div class="game-top-bar">
            <div class="top-bar-left">
                <a href="/?page=menu" target="_self" class="back-btn">
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
                    <span>Оцінити гру:</span>
                    <div class="stars-row">
                        <a href="/?page={active_page}&rate=1" target="_self" class="star-link">⭐</a>
                        <a href="/?page={active_page}&rate=2" target="_self" class="star-link">⭐</a>
                        <a href="/?page={active_page}&rate=3" target="_self" class="star-link">⭐</a>
                        <a href="/?page={active_page}&rate=4" target="_self" class="star-link">⭐</a>
                        <a href="/?page={active_page}&rate=5" target="_self" class="star-link">⭐</a>
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
        
        # 2. Directly run student's game
        try:
            module_name = game_metadata["module"]
            game_module = importlib.import_module(module_name)
            game_module.run()
            
        except Exception as e:
            # Handle student compilation/runtime crash dynamically
            import traceback
            tb_str = traceback.format_exc()
            
            render_html(f"""
            <div class="terminal-container">
                <div class="terminal-header">
                    <span class="terminal-dot red"></span>
                    <span class="terminal-dot yellow"></span>
                    <span class="terminal-dot green"></span>
                    <span class="terminal-title">SYSTEM ERROR CONSOLE - GAME: {game_metadata['title'].upper()}</span>
                </div>
                <div class="terminal-body">
                    <div class="terminal-line error-msg">❌ CRITICAL RUNTIME EXCEPTION DETECTED</div>
                    <div class="terminal-line">----------------------------------------------------------------------</div>
                    <div class="terminal-line"><b>Message:</b> {str(e)}</div>
                    <div class="terminal-line">----------------------------------------------------------------------</div>
                    <div class="terminal-line"><b>Python Stack Traceback:</b></div>
                    <pre class="terminal-code">{tb_str}</pre>
                    <div class="terminal-line">----------------------------------------------------------------------</div>
                    <div class="terminal-line tip">💡 <b>Порада щодо усунення помилки:</b> Перевірте файл <code>games/{game_metadata['id']}.py</code>. 
                    Переконайтеся, що всі змінні в <code>st.session_state</code> ініційовані перед використанням, 
                    а також перевірте правильність відступів та імпортів бібліотек.</div>
                </div>
            </div>
            """)
    else:
        st.error(f"Гру з ID '{active_page}' не знайдено.")
        st.markdown('<a href="/?page=menu" target="_self" class="back-btn">⬅ Повернутися до меню</a>', unsafe_allow_html=True)
