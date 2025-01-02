input_value = '''
You are provided with a scanned image of a receipt. Your task is to accurately extract the relevant details from the receipt and return them in a structured JSON format. Ensure to handle special characters, line breaks, and other potential issues to provide accurate and clean data

Return the extracted information in the following JSON format:


{
  "store": {
    "store_name": "Store Name",
    "address": "Store Address"
  },
  "transaction": {
  
    "id": "Transaction ID",
    "date": "YYYY-MM-DD",
    "time": "HH:MM"
  },
  "items": [
    {
      "name": "Item Name",
      "total_price": "Total Price",
      "category": "Category (Food & Beverages, Health & Personal Care, Clothing & Apparel, Electronics & Gadgets, Home & Furniture, Utilities & Bills, Transportation, Entertainment, Office Supplies, Pets & Animal Care, Miscellaneous, or Other)"
    }
  ],
  "summary": {
    "discount": "Discount Amount",
    "grand_total": "Grand Total Amount",
    "tax": "Tax Amount"
  }
}
'''
