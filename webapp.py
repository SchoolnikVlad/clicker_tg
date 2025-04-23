import streamlit as st
from database import get_user, update_clicks, buy_multiplier
import datetime

st.set_page_config(
    page_title="Telegram Clicker",
    layout="centered",
    menu_items=None
)

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

# Получаем user_id из URL
query_params = st.query_params
user_ids = query_params.get_all("user_id")  # Получаем список значений для параметра "user_id"
user_id = user_ids[0] if user_ids else None  # Берем первое значение, если параметр есть

if user_id:
    try:
        user_id = int(user_id)  # Преобразуем в число
        user = get_user(user_id)
        
        # Основной интерфейс
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🖱️ КЛИКНУТЬ", key="click", use_container_width=True):
                new_clicks = user.clicks + user.multiplier
                update_clicks(user.user_id, new_clicks)
                st.rerun()
        
        with col2:
            st.metric("💎 Множитель", f"x{user.multiplier}")
            st.metric("🖱️ Клики", user.clicks)
        
        # Покупка улучшений
        if st.button(f"🚀 Улучшить множитель (50x{user.multiplier})", use_container_width=True):
            if buy_multiplier(user.user_id):
                st.success("Улучшение куплено!")
                st.rerun()
            else:
                st.error("Недостаточно кликов!")
                
    except Exception as e:
        st.error("Ошибка авторизации. Пожалуйста, зайдите через бота.")
else:
    st.error("🚫 Доступ только через Telegram бота.")