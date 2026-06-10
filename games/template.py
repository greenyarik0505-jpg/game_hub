import streamlit as st

# ШАБЛОН ДЛЯ СТУДЕНТСЬКИХ ІГОР
# Перейменуйте цей файл (наприклад, `my_cool_game.py`) та почніть створювати свою гру!

def run():
    # 1. Заголовок гри
    st.title("🚀 Моя крута космічна гра")
    st.write("Короткий опис гри: керуйте кораблем та збирайте зірки.")
    
    # 2. Робота зі станом (session state)
    # ВАЖЛИВО: Щоб уникнути конфліктів з іншими іграми, використовуйте префікс для змінних!
    # Наприклад, замість "score" використовуйте "space_score"
    if "space_score" not in st.session_state:
        st.session_state.space_score = 0
    if "space_game_over" not in st.session_state:
        st.session_state.space_game_over = False

    # 3. Ігрова логіка
    st.write("---")
    st.metric(label="Набрано балів", value=st.session_state.space_score)
    
    col1, col2 = st.columns(2)
    
    if not st.session_state.space_game_over:
        if col1.button("🪐 Зібрати зірку (+10)", use_container_width=True):
            st.session_state.space_score += 10
            # Перевірка умови закінчення гри
            if st.session_state.space_score >= 100:
                st.session_state.space_game_over = True
            st.rerun()
            
        if col2.button("💥 Врізатися в астероїд (Game Over)", use_container_width=True):
            st.session_state.space_game_over = True
            st.rerun()
    else:
        if st.session_state.space_score >= 100:
            st.success("🎉 Вітаємо! Ви досягли мети і перемогли!")
        else:
            st.error("💀 Гра закінчена! Ви врізалися в астероїд.")
            
        if st.button("Грати знову", type="primary", use_container_width=True):
            st.session_state.space_score = 0
            st.session_state.space_game_over = False
            st.rerun()
            
    st.write("---")
    st.info("💡 Порада для розробника: використовуйте `st.columns` для кнопок і `st.session_state` для збереження стану між перезапусками коду.")
