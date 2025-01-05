import streamlit as st
import DataBaseLogic



st.header("ReceiptHistory")
graphical_representation, receipt_history = st.tabs(["🧾 Graphical Represenation", "📈 Receipt History"])

with receipt_history:
  DataBaseLogic.display_all_data()

with graphical_representation:
  DataBaseLogic.show_graph()