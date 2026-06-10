import streamlit as st

def run():
    st.title("Buggy Test Game")
    st.write("This game is about to trigger a runtime crash to showcase our custom terminal console...")
    
    # Intentionally trigger an error
    x = 1 / 0  # ZeroDivisionError!
