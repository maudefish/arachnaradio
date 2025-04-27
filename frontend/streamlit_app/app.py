import streamlit as st
import dashboard
import dev_dashboard

# ✅ Set page config FIRST
st.set_page_config(page_title="Arachnaradio Dashboard", layout="wide")

# Sidebar nav
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ("User Dashboard", "Developer Tools"))


if page == "User Dashboard":
    dashboard.render()
elif page == "Developer Tools":
    dev_dashboard.render()

    
st.sidebar.markdown("---")
st.sidebar.caption("Built with 🕷️ Arachnaradio")
