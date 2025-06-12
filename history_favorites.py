import streamlit as st

MAX_HISTORY = 5

def save_search(city):
    history = st.session_state.get("search_history", [])
    if city not in history:
        history.insert(0, city)
        if len(history) > MAX_HISTORY:
            history.pop()
        st.session_state["search_history"] = history

def get_search_history():
    return st.session_state.get("search_history", [])

def add_favorite(city):
    favorites = st.session_state.get("favorites", set())
    favorites.add(city)
    st.session_state["favorites"] = favorites

def remove_favorite(city):
    favorites = st.session_state.get("favorites", set())
    favorites.discard(city)
    st.session_state["favorites"] = favorites

def get_favorites():
    return st.session_state.get("favorites", set())
