import streamlit as st

def run():
    st.title("🪙 Crypto Miner Clicker")
    st.write("Click, upgrade, and automate your virtual mining empire!")

    # Initialize game state
    if "coins" not in st.session_state:
        st.session_state.coins = 0.0
    if "click_power" not in st.session_state:
        st.session_state.click_power = 1.0
    if "click_upgrade_cost" not in st.session_state:
        st.session_state.click_upgrade_cost = 10.0
    if "miners" not in st.session_state:
        st.session_state.miners = 0
    if "miner_cost" not in st.session_state:
        st.session_state.miner_cost = 50.0
    if "miner_power" not in st.session_state:
        st.session_state.miner_power = 0.5  # Coins per second

    # Automated miner earnings (adds coins on rerun based on some simulated cycles, but in simple Streamlit we can update on click/rerun)
    # To keep it simple, we check if we need to collect auto coins
    import time
    if "last_tick" not in st.session_state:
        st.session_state.last_tick = time.time()
        
    current_time = time.time()
    elapsed = current_time - st.session_state.last_tick
    st.session_state.last_tick = current_time
    
    if st.session_state.miners > 0:
        earnings = elapsed * st.session_state.miners * st.session_state.miner_power
        st.session_state.coins += earnings

    # Display Stats
    st.metric(label="Total Balance", value=f"🪙 {st.session_state.coins:.2f} Coins")
    
    col1, col2 = st.columns(2)
    col1.metric("Clicking Power", f"+{st.session_state.click_power:.1f} per click")
    col2.metric("Auto Mining Speed", f"+{st.session_state.miners * st.session_state.miner_power:.1f} / sec")

    st.write("---")

    # Mining Action
    # Large click button
    if st.button("⛏️ MINE COIN ⛏️", type="primary", use_container_width=True):
        st.session_state.coins += st.session_state.click_power
        st.rerun()

    st.write("### Upgrades Shop")
    
    col_up1, col_up2 = st.columns(2)
    
    # Click Upgrade
    with col_up1:
        st.write("🚀 **Super Pickaxe**")
        st.write(f"Increases click power by +1.\n\n**Cost:** {st.session_state.click_upgrade_cost:.1f} coins")
        can_buy_click = st.session_state.coins >= st.session_state.click_upgrade_cost
        if st.button("Upgrade Pickaxe", disabled=not can_buy_click, use_container_width=True):
            st.session_state.coins -= st.session_state.click_upgrade_cost
            st.session_state.click_power += 1.0
            st.session_state.click_upgrade_cost = int(st.session_state.click_upgrade_cost * 1.5)
            st.rerun()
            
    # Auto Miner Upgrade
    with col_up2:
        st.write("🤖 **Automated GPU Miner**")
        st.write(f"Mines +0.5 coins automatically.\n\n**Cost:** {st.session_state.miner_cost:.1f} coins")
        can_buy_miner = st.session_state.coins >= st.session_state.miner_cost
        if st.button("Hire Miner GPU", disabled=not can_buy_miner, use_container_width=True):
            st.session_state.coins -= st.session_state.miner_cost
            st.session_state.miners += 1
            st.session_state.miner_cost = int(st.session_state.miner_cost * 1.4)
            st.rerun()

    st.write("---")
    
    # Reset Button
    if st.button("Reset Mining Progress", use_container_width=True):
        st.session_state.coins = 0.0
        st.session_state.click_power = 1.0
        st.session_state.click_upgrade_cost = 10.0
        st.session_state.miners = 0
        st.session_state.miner_cost = 50.0
        st.session_state.last_tick = time.time()
        st.rerun()
