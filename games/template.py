import streamlit as st
from games.utils import get_player_profile, update_player_profile

# ШАБЛОН ДЛЯ СТУДЕНТСЬКИХ ІГОР З ІНТЕГРАЦІЄЮ ПРОФІЛІВ
# Перейменуйте цей файл (наприклад, `my_cool_game.py`) та почніть створювати свою гру!

METADATA = {
    "id": "template",
    "title": "💻 Шаблон розробника",
    "author": "Вчитель / Команда Hub",
    "category": "Strategy",
    "description": "Інструкція та шаблон коду для розробки студентських ігор з підтримкою збереження прогресу.",
    "image": "assets/template.jpg",
    "tags": ["Документація", "Шаблон", "Приклад"]
}

def run():
    # 1. Заголовок гри
    st.title("💻 Шаблон розробника ігор")
    st.write("Це інтерактивний приклад того, як створювати ігри з підтримкою профілів.")
    
    # 2. Робота зі спільними профілями користувачів
    username = st.session_state.get("current_user", "Гість")
    profile = get_player_profile(username)
    
    # Ініціалізація вашої власної структури у профілі, якщо її ще немає
    if "template_stats" not in profile:
        profile["template_stats"] = {
            "clicks": 0,
            "stars_collected": 0
        }
    stats = profile["template_stats"]

    # 3. Робота зі станом сесії (st.session_state)
    # Зберігайте тимчасові дані, які скидаються при виході з гри, тут
    if "space_stars" not in st.session_state:
        st.session_state.space_stars = 0
    if "space_game_over" not in st.session_state:
        st.session_state.space_game_over = False

    st.write("---")
    
    # Показуємо збережені у файлі глобальні дані користувача
    st.write(f"👤 Поточний гравець: **{username}**")
    
    col_metrics1, col_metrics2 = st.columns(2)
    col_metrics1.metric(label="Зібрано зірок (Тимчасово)", value=st.session_state.space_stars)
    col_metrics2.metric(label="Усього кліків (Збережено у профілі)", value=stats["clicks"])
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    
    if not st.session_state.space_game_over:
        if col1.button("🪐 Зібрати зірку (+10)", use_container_width=True):
            st.session_state.space_stars += 10
            # Збільшуємо кліки та зберігаємо у файл!
            stats["clicks"] += 1
            profile["template_stats"] = stats
            update_player_profile(username, profile)
            
            # Перевірка умови закінчення гри
            if st.session_state.space_stars >= 100:
                st.session_state.space_game_over = True
            st.rerun()
            
        if col2.button("💥 Врізатися в астероїд (Game Over)", use_container_width=True):
            # Кліки теж рахуються
            stats["clicks"] += 1
            profile["template_stats"] = stats
            update_player_profile(username, profile)
            
            st.session_state.space_game_over = True
            st.rerun()
    else:
        if st.session_state.space_stars >= 100:
            st.success("🎉 Вітаємо! Ви досягли мети і перемогли!")
            # Додамо зірочку в постійний профіль при перемозі
            stats["stars_collected"] += 1
            profile["template_stats"] = stats
            update_player_profile(username, profile)
        else:
            st.error("💀 Гра закінчена! Ви врізалися в астероїд.")
            
        if st.button("Грати знову", type="primary", use_container_width=True):
            st.session_state.space_stars = 0
            st.session_state.space_game_over = False
            st.rerun()
            
    st.write("---")
    st.write("### 📖 Як це працює для розробників:")
    st.code("""
# Імпортуйте утиліти профілів:
from games.utils import get_player_profile, update_player_profile

def run():
    # Отримайте нікнейм поточного користувача
    username = st.session_state.get("current_user", "Гість")
    
    # Завантажте його профайл
    profile = get_player_profile(username)
    
    # Створіть свій словник даних всередині профілю
    if "my_game_stats" not in profile:
        profile["my_game_stats"] = { "high_score": 0 }
        
    # Модифікуйте та збережіть:
    profile["my_game_stats"]["high_score"] = 42
    update_player_profile(username, profile)
    """, language="python")
