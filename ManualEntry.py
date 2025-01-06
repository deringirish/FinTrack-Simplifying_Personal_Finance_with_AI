import streamlit as st
from datetime import datetime
import DisplayDetails
import DataBaseLogic

json_data = {
    "store": {
        "store_name": None,
        "address": None
    },
    "transaction": {
        "id": None,
        "date": None,
        "time": None
    },
    "items": [],
    "summary": {
        "discount": 0.0,
        "grand_total": 0.0,
        "tax": 0.0
    }
}

def manual_entry():
    st.subheader("Manual Entry of Receipt Details...")

    with st.form("json_form", clear_on_submit=False):
        st.subheader("Store Details")
        store_name = st.text_input(
            "Store Name", key="store_name", value=st.session_state.get("store_name", ""))
        address = st.text_input("Address", key="address",value=st.session_state.get("address", ""))

        st.subheader("Transaction Details")
        transaction_id = st.text_input("Transaction ID", key="transaction_id", value=st.session_state.get("transaction_id", ""))
        date = st.date_input("Date (YYYY-MM-DD)", key="date",value=st.session_state.get("date", None))

        time = st.number_input("Time (HH.MM)", min_value=0.0, max_value=24.0, format="%.2f", step=0.01, key="time",value=st.session_state.get("time", None))

        st.subheader("Items")
        if "component_count" not in st.session_state:
            st.session_state.component_count = len(st.session_state.get("items", [])) + 1

        items = []
        for i in range(st.session_state.component_count):
            with st.expander(f"Item {i + 1}", expanded=True):
                cols = st.columns([3, 3, 3])
                with cols[0]:
                    item_name = st.text_input(f"Item Name {i + 1}", key=f"text_field1_{i}", value=st.session_state.get(f"text_field1_{i}", ""))
                with cols[1]:
                    total_price = st.number_input(f"Total Price {i + 1}", min_value=0.0, format="%.2f", step=0.1, key=f"text_field2_{i}", value=st.session_state.get(f"text_field2_{i}", None))
                with cols[2]:
                    category = st.selectbox(
                        f"Category {i + 1}",
                        [
                            "None", "Food & Beverages", "Health & Personal Care",
                            "Clothing & Apparel", "Electronics & Gadgets",
                            "Home & Furniture", "Utilities & Bills", "Transportation",
                            "Entertainment", "Office Supplies", "Pets & Animal Care",
                            "Miscellaneous", "Other"
                        ],
                        key=f"dropdown_{i}",
                        index=["None", "Food & Beverages", "Health & Personal Care", "Clothing & Apparel", "Electronics & Gadgets",
                               "Home & Furniture", "Utilities & Bills", "Transportation", "Entertainment", "Office Supplies",
                               "Pets & Animal Care", "Miscellaneous", "Other"].index(st.session_state.get(f"dropdown_{i}", "None"))
                    )

        if st.form_submit_button("Add Another Item"):
            st.session_state.component_count += 1

        st.subheader("Summary Details")
        discount = st.number_input(
            "Discount", min_value=0.0, format="%.2f", step=0.1, key="discount", value=st.session_state.get("discount", None))
        grand_total = st.number_input(
            "Grand Total", min_value=0.0, format="%.2f", step=0.1, key="grand_total", value=st.session_state.get("grand_total", None))
        tax = st.number_input("Tax", min_value=0.0,
                              format="%.2f", step=0.1, key="tax", value=st.session_state.get("tax",None))

        if st.form_submit_button("Reset Form"):
            for key in list(st.session_state.keys()):
                if key.startswith("text_field1_") or key.startswith("text_field2_") or key.startswith("dropdown_"):
                    del st.session_state[key]
            st.session_state.component_count = 1

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.markdown("---")
            json_data["store"]["store_name"] = store_name if store_name else None
            json_data["store"]["address"] = address if address else None
            json_data["transaction"]["id"] = transaction_id if transaction_id else None
            json_data["transaction"]["date"] = date.strftime(
                "%Y-%m-%d") if date else None
            json_data["transaction"]["time"] = time
            items = []
            for i in range(st.session_state.component_count):
                item_name = st.session_state.get(f"text_field1_{i}")
                total_price = st.session_state.get(f"text_field2_{i}")
                category = st.session_state.get(f"dropdown_{i}")
                if item_name and total_price and category:
                    items.append({
                        "name": item_name,
                        "total_price": total_price,
                        "category": category if category != "None" else None
                    })
            json_data["items"] = items
            json_data["summary"]["discount"] = discount
            json_data["summary"]["grand_total"] = grand_total
            json_data["summary"]["tax"] = tax

            updated_json_data = DisplayDetails.print_response_from_manual_entry(json_data)
            print(updated_json_data)
            DataBaseLogic.upload_to_database(updated_json_data)

