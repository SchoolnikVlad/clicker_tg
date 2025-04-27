import streamlit as st
from database import get_user, update_clicks, buy_multiplier
from auth import verify_webapp_signature
import os

st.set_page_config(
    page_title="Telegram Clicker",
    layout="centered",
    menu_items=None
)

# Режим разработки: пропускаем проверку подписи локально
IS_LOCAL = os.environ.get("IS_LOCAL", False)

if not IS_LOCAL:
    # Проверка подписи Telegram
    try:
        init_data = st.query_params.get("tgWebAppData", None)
        if not init_data or not verify_webapp_signature(st.secrets["BOT_TOKEN"], init_data):
            st.error("Доступ запрещен!")
            st.stop()
    except Exception as e:
        st.error(f"Ошибка проверки авторизации: {str(e)}")
        st.stop()

# Получение user_id (для локального тестирования задайте вручную)
user_id = st.query_params.get("user_id", None)
if IS_LOCAL:
    user_id = 12345  # Тестовый user_id для локального запуска

if not user_id:
    st.error("user_id не найден")
    st.stop()

try:
    user_id = int(user_id)
    user = get_user(user_id)
except Exception as e:
    st.error(f"Ошибка авторизации: {str(e)}")
    st.stop()

# Интерфейс
col1, col2 = st.columns(2)
with col1:
    if st.button("🖱️ КЛИКНУТЬ", use_container_width=True):
        new_clicks = user.clicks + user.multiplier
        update_clicks(user.user_id, new_clicks)
        st.rerun()

with col2:
    st.metric("💎 Множитель", f"x{user.multiplier}")
    st.metric("🖱️ Клики", user.clicks)

if st.button(f"🚀 Улучшить множитель (50x{user.multiplier})", use_container_width=True):
    if buy_multiplier(user.user_id):
        st.success("Успешно!")
        st.rerun()
    else:
        st.error("Недостаточно кликов!")