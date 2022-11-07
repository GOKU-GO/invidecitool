import streamlit as st

import Stock
import Crypto_Dashboard

pages = {'Crypto_Dashboard': Crypto_Dashboard, 'Stock': Stock}

choice = st.sidebar.radio("Choice your page: ",tuple(pages.keys()))
page = pages[choice]
page.main()




