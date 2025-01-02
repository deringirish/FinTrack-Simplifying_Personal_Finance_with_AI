import streamlit as st
import pandas as pd
import json

# Function to print th4 
def print_response_from_image(json_data):
    try:
        st.header("The Response is")

        # Store Details
        st.subheader("Store Details")
        store_name = json_data.get("store", {}).get("store_name", "Not Found")
        address = json_data.get("store", {}).get("address", "Not Found")
        st.write(f"Store Name: {store_name}")
        st.write(f"Address: {address}")

        # Transaction Details
        st.subheader("Transaction Details")
        transaction_id = json_data.get(
            "transaction", {}).get("id", "Not Found")
        date = json_data.get("transaction", {}).get("date", "Not Found")
        time = json_data.get("transaction", {}).get("time", "Not Found")
        st.write(f"Transaction ID: {transaction_id}")
        st.write(f"Date: {date}")
        st.write(f"Time: {time}")

        # Description
        st.subheader("Description")
        items = json_data.get("items", [])
        total_price_sum = 0.0  # Variable to store sum of item prices

        if items:
            data = {
                'Item': [item.get("name", "Not Found") for item in items],
                'Category': [item.get("category", "Not Found") for item in items],
                'Price': [item.get("total_price", "0.00") for item in items]
            }
            # Calculate total price
            total_price_sum = sum(
                float(item.get("total_price", 0.00)) for item in items)
            df = pd.DataFrame(data)
            st.table(df)
        else:
            st.write("Items: Not Found")

        # Summary
        st.subheader("Summary")
        discount = json_data.get("summary", {}).get("discount", "Not Found")
        grand_total = json_data.get("summary", {}).get("grand_total", None)
        tax = json_data.get("summary", {}).get("tax", "Not Found")

        st.write(f"Discount: {discount}")

        if grand_total is not None:
            st.write(f"Grand Total: {grand_total}")
        else:
            # If grand_total is not provided, calculate it
            json_data["summary"]["grand_total"] = total_price_sum
            st.write(f"Grand Total (calculated): {total_price_sum:.2f}")

        st.write(f"Tax: {tax}")

        # Create and return a new JSON with updated values
        updated_json = json_data
        return updated_json

    except Exception as e:
        st.error(f"Error displaying the response: {e}")


def print_response_from_manual_entry(json_data):
    try:
        st.header("Transaction Details")

        # Store Details
        st.subheader("Store Details")
        store_name = json_data.get("store", {}).get(
            "store_name", "Not Found")
        address = json_data.get("store", {}).get(
            "address", "Not Found")
        st.write(f"Store Name: {store_name}")
        st.write(f"Address: {address}")

        # Transaction Details
        st.subheader("Transaction Information")
        transaction_id = json_data.get(
            "transaction", {}).get("id", "Not Found")
        date = json_data.get("transaction", {}).get(
            "date", "Not Found")
        time = json_data.get("transaction", {}).get(
            "time", "Not Found")
        st.write(f"Transaction ID: {transaction_id}")
        st.write(f"Date: {date}")
        st.write(f"Time: {time}")

        # Items Description
        st.subheader("Purchased Items")
        items = json_data.get("items", [])
        total_price_sum = 0.0  # Variable to store sum of item prices

        if items:
            # Filter out None values and invalid items
            valid_items = [
                item for item in items
                if item.get("name") is not None and
                item.get("total_price") is not None and
                item.get("category") is not None
            ]

            if valid_items:
                data = {
                    'Item': [item.get("name", "Not Found") for item in valid_items],
                    'Category': [item.get("category", "Not Found") for item in valid_items],
                    'Price': [item.get("total_price", 0.00) for item in valid_items]
                }
                # Calculate total price
                total_price_sum = sum(
                    float(item.get("total_price", 0.00)) for item in valid_items)
                df = pd.DataFrame(data)
                st.table(df)
            else:
                st.write("No valid items found in the transaction.")
        else:
            st.write("No items found in the transaction.")

        # Summary
        st.subheader("Transaction Summary")

        # Handle discount safely
        discount = json_data.get("summary", {}).get("discount")
        discount_display = f"{
            discount:.2f}" if discount is not None else "Not Found"
        st.write(f"Discount: {discount_display}")

        # Handle grand total safely
        grand_total = json_data.get("summary", {}).get("grand_total")
        if grand_total is not None:
            st.write(f"Grand Total: {grand_total:.2f}")
        else:
            # If grand_total is not provided, calculate it
            grand_total = total_price_sum
            json_data["summary"]["grand_total"] = grand_total
            st.write(f"Grand Total (calculated): {grand_total:.2f}")

        # Handle tax safely
        tax = json_data.get("summary", {}).get("tax")
        tax_display = f"{tax:.2f}" if tax is not None else "Not Found"
        st.write(f"Tax: {tax_display}")

        # Create and return a new JSON with updated values
        updated_json = json_data
        return updated_json

    except Exception as e:
        st.error(f"Error displaying the response: {e}")
        return json_data
