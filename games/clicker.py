import streamlit as st
import time
from games.utils import get_player_profile, update_player_profile

METADATA = {
    "id": "clicker",
    "title": "🪙 Crypto Miner Clicker",
    "author": "Команда Hub",
    "category": "Arcade",
    "description": "Клікай по крипто-монеті, купуй відеокарти для автомайнінгу та стань крипто-магнатом класу!",
    "image": "assets/clicker.jpg",
    "tags": ["Клікер", "Автомайнінг", "Магнат"]
}

def run():
    st.title("🪙 Crypto Miner Clicker")
    st.write("Клікай, покращуй Pickaxe та купуй автоматичні GPU майнери!")

    # Load profile data
    username = st.session_state.get("current_user", "Гість")
    profile = get_player_profile(username)
    
    if "clicker" not in profile:
        profile["clicker"] = {
            "coins": 0.0,
            "click_power": 1.0,
            "click_upgrade_cost": 10.0,
            "miners": 0,
            "miner_cost": 50.0
        }
    stats = profile["clicker"]

    # Sync player profile data to session state if not initialized
    if "clicker_coins" not in st.session_state:
        st.session_state.clicker_coins = float(stats.get("coins", 0.0))
        st.session_state.clicker_power = float(stats.get("click_power", 1.0))
        st.session_state.clicker_upgrade_cost = float(stats.get("click_upgrade_cost", 10.0))
        st.session_state.clicker_miners = int(stats.get("miners", 0))
        st.session_state.clicker_miner_cost = float(stats.get("miner_cost", 50.0))

    # Helper function to save current session progress back to JSON
    def save_progress():
        profile["clicker"] = {
            "coins": st.session_state.clicker_coins,
            "click_power": st.session_state.clicker_power,
            "click_upgrade_cost": st.session_state.clicker_upgrade_cost,
            "miners": st.session_state.clicker_miners,
            "miner_cost": st.session_state.clicker_miner_cost
        }
        update_player_profile(username, profile)

    # Automated miner earnings
    if "last_tick" not in st.session_state:
        st.session_state.last_tick = time.time()
        
    current_time = time.time()
    elapsed = current_time - st.session_state.last_tick
    st.session_state.last_tick = current_time
    
    miner_power = 0.5  # Coins per second per miner
    
    if st.session_state.clicker_miners > 0:
        earnings = elapsed * st.session_state.clicker_miners * miner_power
        st.session_state.clicker_coins += earnings
        # Save on ticks to preserve progress
        save_progress()

    # Display Stats
    st.metric(label="Баланс", value=f"🪙 {st.session_state.clicker_coins:.2f} Coins")
    
    col1, col2 = st.columns(2)
    col1.metric("Сила кліку", f"+{st.session_state.clicker_power:.1f} за клік")
    col2.metric("Швидкість автомайнінгу", f"+{st.session_state.clicker_miners * miner_power:.1f} / сек")

    st.write("---")

    # Mining Action (Large click button)
    if st.button("⛏️ ЗДОБУТИ КРИПТО-МОНЕТУ ⛏️", type="primary", use_container_width=True):
        st.session_state.clicker_coins += st.session_state.clicker_power
        save_progress()
        st.rerun()

    st.write("### Магазин Покращень")
    
    col_up1, col_up2 = st.columns(2)
    
    # Click Upgrade
    with col_up1:
        st.write("🚀 **Супер-Кірка (Pickaxe)**")
        st.write(f"Збільшує силу кліку на +1.\n\n**Вартість:** {st.session_state.clicker_upgrade_cost:.1f} coins")
        can_buy_click = st.session_state.clicker_coins >= st.session_state.clicker_upgrade_cost
        if st.button("Покращити Кірку", disabled=not can_buy_click, use_container_width=True):
            st.session_state.clicker_coins -= st.session_state.clicker_upgrade_cost
            st.session_state.clicker_power += 1.0
            st.session_state.clicker_upgrade_cost = int(st.session_state.clicker_upgrade_cost * 1.5)
            save_progress()
            st.rerun()
            
    # Auto Miner Upgrade
    with col_up2:
        st.write("🤖 **Майнінг-Ферма GPU**")
        st.write(f"Майнить +0.5 монет щосекунди автоматично.\n\n**Вартість:** {st.session_state.clicker_miner_cost:.1f} coins")
        can_buy_miner = st.session_state.clicker_coins >= st.session_state.clicker_miner_cost
        if st.button("Придбати GPU", disabled=not can_buy_miner, use_container_width=True):
            st.session_state.clicker_coins -= st.session_state.clicker_miner_cost
            st.session_state.clicker_miners += 1
            st.session_state.clicker_miner_cost = int(st.session_state.clicker_miner_cost * 1.4)
            save_progress()
            st.rerun()

    st.write("---")
    
    # Reset Button
    if st.button("Скинути ігровий процес", use_container_width=True):
        st.session_state.clicker_coins = 0.0
        st.session_state.clicker_power = 1.0
        st.session_state.clicker_upgrade_cost = 10.0
        st.session_state.clicker_miners = 0
        st.session_state.clicker_miner_cost = 50.0
        st.session_state.last_tick = time.time()
        save_progress()
        st.rerun()
