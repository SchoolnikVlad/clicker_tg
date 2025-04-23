import streamlit as st
from database import get_user, update_clicks, buy_multiplier
import datetime

st.set_page_config(page_title="Telegram Clicker", layout="centered")

# Стили для игры
st.markdown("""
<style>
@keyframes click {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}
.button {
    animation: click 0.3s ease;
    background: #4CAF50;
    color: white;
    border: none;
    padding: 20px;
    border-radius: 10px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

user_id = st.query_params().get("user_id", [None])[0]

if user_id:
    user = get_user(int(user_id))
    st.title(f"🕹️ Telegram Clicker")
    
    # Основной интерфейс
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖱️ КЛИКНУТЬ", key="click", use_container_width=True):
            new_clicks = user.clicks + user.multiplier
            update_clicks(user.user_id, new_clicks)
            st.experimental_rerun()
        
    with col2:
        st.metric("💎 Множитель", f"x{user.multiplier}")
        st.metric("🖱️ Клики", user.clicks)
    
    # Покупка улучшений
    if st.button(f"🚀 Улучшить множитель (50x{user.multiplier})", use_container_width=True):
        if buy_multiplier(user.user_id):
            st.success("Улучшение куплено!")
            st.experimental_rerun()
        else:
            st.error("Недостаточно кликов!")
else:
    st.error("🚫 Доступ только через Telegram бота.")