import streamlit as st
from database import get_user, update_clicks, buy_multiplier
from auth import verify_webapp_signature

st.set_page_config(
    page_title="Telegram Clicker",
    layout="centered",
    menu_items=None
)

# Проверка подписи Telegram
try:
    init_data = st.query_params.get("tgWebAppData", None)
    if not init_data or not verify_webapp_signature(st.secrets["BOT_TOKEN"], init_data):
        st.error("Доступ запрещен!")
        st.stop()
except:
    st.error("Ошибка проверки авторизации")
    st.stop()

# Получение user_id
user_id = st.query_params.get("user_id", None)
if not user_id:
    st.error("user_id не найден")
    st.stop()

try:
    user_id = int(user_id)
    user = get_user(user_id)
except:
    st.error("Ошибка авторизации")
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