import streamlit as st

pages = [
         st.Page(page='overview.py', url_path='overview.py', title='Overview'),
         st.Page(page='geographic.py', url_path='geographic.py', title='Geographic'),
         st.Page(page='risk_profiles.py', url_path='risk_profiles.py', title='Risk Profiles'),
         st.Page(page='recommendations.py', url_path='recommendations.py', title='Recommendations'),
         ]

pg = st.navigation(pages)
pg.run()


