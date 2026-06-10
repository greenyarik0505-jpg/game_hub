import json
import os
import streamlit as st
from datetime import datetime

PROFILES_FILE = "profiles.json"

def load_profiles():
    """Loads all player profiles from profiles.json."""
    if os.path.exists(PROFILES_FILE):
        try:
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            # If JSON is corrupted, start fresh
            pass
    return {}

def save_profiles(profiles):
    """Saves the profiles dict to profiles.json."""
    try:
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Помилка при збереженні профілів: {e}")

def get_default_profile():
    """Returns the default profile structure for a new player."""
    return {
        "created_at": datetime.now().isoformat(),
        "tic_tac_toe": {
            "wins": 0,
            "losses": 0,
            "ties": 0
        },
        "clicker": {
            "coins": 0.0,
            "click_power": 1.0,
            "click_upgrade_cost": 10.0,
            "miners": 0,
            "miner_cost": 50.0
        },
        "memory_match": {
            "best_moves": 999,
            "best_time": 9999.0,
            "games_played": 0
        }
    }

def get_player_profile(username):
    """Retrieves or creates a player's profile data."""
    if not username:
        username = "Гість"
    profiles = load_profiles()
    if username not in profiles:
        profiles[username] = get_default_profile()
        save_profiles(profiles)
    return profiles[username]

def update_player_profile(username, profile_data):
    """Updates and saves a player's profile data."""
    if not username:
        username = "Гість"
    profiles = load_profiles()
    profiles[username] = profile_data
    save_profiles(profiles)
    
    # Sync with session state if this is the active user
    if "current_user" in st.session_state and st.session_state.current_user == username:
        st.session_state.user_profile = profile_data
