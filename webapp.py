import streamlit as st
from database import get_user, update_clicks, buy_multiplier
from auth import verify_webapp_signature
import os

st.set_page_config(
    page_title="Telegram Clicker",
    layout="centered",
    menu_items=None
)

# Режим отладки
DEBUG = os.environ.get("DEBUG", False)

try:
    # Логируем все параметры URL
    st.write("Все параметры URL:", st.query_params.to_dict())
    
    # Проверка подписи только в продакшене
    if not DEBUG:
        init_data = st.query_params.get("tgWebAppData", None)
        st.write("Полученные данные initData:", init_data)
        
        if not init_data:
            st.error("Отсутствует tgWebAppData!")
            st.stop()
            
        if not verify_webapp_signature(st.secrets["BOT_TOKEN"], init_data):
            st.error("Неверная подпись Telegram!")
            st.stop()

    # Получение user_id
    user_id = st.query_params.get("user_id", None)
    st.write("User ID из URL:", user_id)
    
    if not user_id:
        st.error("User ID не найден")
        st.stop()

    user = get_user(int(user_id))
    st.write("Данные пользователя из БД:", user.__dict__)

except Exception as e:
    st.error(f"Критическая ошибка: {str(e)}")
    st.stop()

# Интерфейс приложения
col1, col2 = st.columns(2)
with col1:
    if st.button("🖱️ КЛИКНУТЬ"):
        new_clicks = user.clicks + user.multiplier
        update_clicks(user.user_id, new_clicks)
        st.rerun()

with col2:
    st.metric("💎 Множитель", f"x{user.multiplier}")
    st.metric("🖱️ Клики", user.clicks)

if st.button(f"🚀 Улучшить множитель (50x{user.multiplier})"):
    if buy_multiplier(user.user_id):
        st.success("Успешно!")
        st.rerun()
    else:
        st.error("Недостаточно кликов!")