# Receipt Scanner Application

A **Streamlit-based** application that can scan receipts using image upload or manual entry. The application uses Google's Gemini AI for image processing and MongoDB for data storage.

## Prerequisites

Before you begin, ensure you have the following installed on your computer:
- [Python](https://www.python.org/downloads/) (3.8 or newer)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- [Git](https://git-scm.com/downloads)
- **Google Gemini API Key** (Instructions below)

## Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Select **"Create API key in new project"**
5. Give your project a name (e.g., "Receipt Scanner")
6. Click **"Create"**
7. Copy your API key (it will look like "AIza...")
8. Store this key securely, as you won't be able to see it again (but you can create a new one if needed)

**Important Notes:**
- Keep your API key secret
- Don’t commit it to version control
- The free tier includes:
  - 60 requests per minute
  - Maximum 32k context tokens
  - No credit card required

## Step-by-Step Setup Guide

### 1. Clone the Repository
```bash
git clone [your-repository-url]
cd receipt-scanner
```

### 2. Set Up Visual Studio Code
1. Open **Visual Studio Code**.
2. Install the Python extension:
   - Click on **Extensions** (or press `Ctrl+Shift+X`).
   - Search for **"Python"**.
   - Install the **Microsoft Python extension**.

### 3. Create and Activate Virtual Environment
Open the VS Code terminal (`Ctrl+` or `View → Terminal`) and run the following:

For **Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

For **macOS/Linux**:
```bash
python -m venv venv
source venv/bin/activate
```

### 4. Install Required Packages
With the virtual environment activated, run:
```bash
pip install streamlit pandas pillow python-dotenv google-generativeai pymongo matplotlib
```

### 5. Set Up MongoDB
1. After installing MongoDB Community Server:
   - **Windows**: MongoDB should start automatically as a service.
   - **macOS**: Run `brew services start mongodb-community`.
   - **Linux**: Run `sudo systemctl start mongod`.
2. Verify MongoDB is running:
   - Open **MongoDB Compass** (installed with MongoDB).
   - Connect to `mongodb://localhost:27017`.

### 6. Configure Environment Variables
1. Create a `.env` file in the project root.
2. Add your **Gemini API key** (obtained from Google AI Studio) in the `.env` file:
```bash
GEMINI_KEY="your-api-key-here"
```
3. **Important**: Ensure the `.env` file is listed in your `.gitignore` file to prevent accidentally sharing your API key.

### 7. Run the Application
In the VS Code terminal (with the virtual environment activated), run:
```bash
streamlit run Home.py
```
The application should open in your default web browser.

## Using the Application

### Image Upload
1. Click on **"🖼️ Image Upload"** tab.
2. Upload a receipt image.
3. Click **"Analyse Receipt"**.
4. View the extracted information.

### Manual Entry
1. Click on **"📝 Manual Entry"** tab.
2. Fill in the store details.
3. Add transaction information.
4. Add items (use **"Add Another Item"** button for multiple items).
5. Fill in summary details.
6. Click **"Submit"**.

### View Receipt History
1. Click on **"Receipt History"** in the sidebar.
2. View:
   - Graphical representation of spending.
   - Detailed receipt history.

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**
   - Make sure the virtual environment is activated.
   - Run `pip install [package-name]` for the missing module.

2. **MongoDB Connection Error**
   - Verify MongoDB is running:
     - **Windows**: Check Services (`Win+R` → `services.msc`).
     - **macOS/Linux**: Run `ps aux | grep mongod`.
   - Try connecting with MongoDB Compass.

3. **Streamlit Import Error**
   - Ensure you're in the correct directory.
   - Verify all project files are present.
   - Check file names match exactly.

4. **Image Processing Error**
   - Verify your Gemini API key in the `.env` file.
   - Ensure the image is clear and readable.
   - Check the internet connection.

### Additional API-Related Issues:

1. **"Invalid API Key" Error**
   - Verify the API key is correctly copied to your `.env` file.
   - Check for any extra spaces or characters.
   - Try generating a new API key if issues persist.

2. **"Quota Exceeded" Error**
   - You’ve reached the API usage limit.
   - Wait for the quota to reset (usually at the start of the next minute).
   - Consider upgrading to a paid tier for higher limits.

## Project Structure
```
receipt_scanner/
├── .env
├── Home.py
├── Input.py
├── ImageUpload.py
├── ManualEntry.py
├── DatabaseLogic.py
├── DisplayDetails.py
└── pages/
    └── ReceiptHistory.py
```