import streamlit as st

st.title("🚀 Моя Вільна Гра")
st.write("Це гра, написана взагалі без інструкцій, без функції run() та без METADATA!")

val = st.slider("Виберіть рівень складності:", min_value=1, max_value=10, value=5)
st.success(f"Ви обрали рівень {val}! Гра працює в інтерактивному режимі!")
