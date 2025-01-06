from pymongo import MongoClient
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import DisplayDetails

client = None


def database_setup():
    global client
    try:
        client = MongoClient("mongodb://localhost:27017",
                             serverSelectionTimeoutMS=5000)
        db = client["receipt_scanner"]
        client.server_info()  # Check connection
        collection = db["receipts"]
        return collection
    except Exception as e:
        st.error(f"Failed to configure MongoDB: {e}")
        return None


def upload_to_database(json_data):
    """
    Upload data to MongoDB without providing an `_id`.
    MongoDB will generate a unique `_id` automatically.
    """
    collection = database_setup()
    if collection is not None:
        try:
            # Ensure `_id` is not in the data to let MongoDB auto-generate it
            if "_id" in json_data:
                del json_data["_id"]

            result = collection.insert_one(json_data)
            st.success(f"Data successfully saved to MongoDB with ID: {
                       result.inserted_id}")
        except Exception as e:
            st.error(f"Failed to save data to MongoDB: {e}")
    else:
        st.error("Failed to connect to MongoDB. Collection not found.")


def display_all_data():
    collection = database_setup()
    if collection is not None:
        try:
            documents = collection.find()
            data_list = [doc for doc in documents]
            for index, doc in enumerate(data_list):
                st.header(f"Data {index + 1}")
                DisplayDetails.print_response_from_image(doc)
        except Exception as e:
            st.error(f"Failed to retrieve data from MongoDB: {e}")
    else:
        st.error("Failed to connect to MongoDB. Collection not found.")


def show_graph():
    collection = database_setup()
    if collection is not None:
        try:
            data = list(collection.find())

            if not data:
                st.error("No data available in the collection.")
                return

            df = pd.DataFrame(data)

            if df.empty:
                st.error("No valid data to display.")
                return

            category_total = {}

            for index, row in df.iterrows():
                if "items" in row and row["items"]:
                    for item in row["items"]:
                        category = item.get("category")
                        price = item.get("total_price")

                        if category and isinstance(category, str) and price:
                            try:
                                price = float(price)
                                category_total[category] = category_total.get(
                                    category, 0) + price
                            except ValueError:
                                st.warning(
                                    f"Invalid price value for item: {item}"
                                )

            if not category_total:
                st.error("No valid category data to display.")
                return

            labels = list(category_total.keys())
            sizes = list(category_total.values())
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(labels, sizes, color='blue')
            ax.set_xlabel('Category')
            ax.set_ylabel('Total Price ($)')
            ax.set_title('Total Price by Category')
            plt.xticks(rotation=90)

            for i, v in enumerate(sizes):
                ax.text(i, v + 10, f'{v:.2f}', ha='center')

            st.pyplot(fig)

            summary_df = pd.DataFrame(
                list(category_total.items()), columns=["Category", "Total Price"]
            )
            st.table(summary_df)

        except Exception as e:
            st.error(f"An error occurred while generating the graph: {e}")
    else:
        st.error("Failed to connect to MongoDB. Collection not found.")
