# Financial Data Visualization Flask App

A professional, user-friendly Flask web application for uploading Excel files, visualizing financial data (Income/Expense) with multiple graph types, and providing monthly details and summary statistics.

## Features

- **Excel Upload:** Upload your financial data in Excel format (must include columns: `Month`, `Income`, `Expense`).
- **Graph Selection:** Choose from Line, Bar, Pie, or Histogram graphs before uploading.
- **Data Visualization:** View interactive graphs with analysis annotations (highest/lowest income/expense).
- **Summary Statistics:** Instantly see average, highest, and lowest income/expense months.
- **Monthly Details:** Click any month to view its detailed income and expense breakdown.
- **Modern UI:** Beautiful, professional, and colorful (rainbow) interface for a great user experience.
- **Error Handling:** Friendly error messages for missing/invalid files or columns.

## Setup Instructions

1. **Clone or Download the Repository**

2. **Create and Activate a Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```powershell
   pip install Flask pandas openpyxl matplotlib
   ```

4. **Run the Application**
   ```powershell
   python app.py
   ```
   The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage

1. On the dashboard, select your preferred graph type.
2. Upload an Excel file with columns: `Month`, `Income`, `Expense`.
3. View the results page with your selected graph, summary statistics, and links to monthly details.
4. Click any month for a detailed breakdown.
5. Use navigation buttons to return to the dashboard or results.

## File Structure

- `app.py` — Main Flask application and logic
- `templates/` — HTML templates (`index.html`, `results.html`, `month_details.html`)
- `static/graphs/` — Generated graph images
- `upload/` — Uploaded Excel files

## Excel File Format Example

| Month    | Income | Expense |
|----------|--------|---------|
| January  | 5000   | 2000    |
| February | 5200   | 2100    |
| ...      | ...    | ...     |

## Customization
- Update the templates in `templates/` for UI changes.
- Modify `app.py` to add new features or change logic.

## License
This project is for educational and demonstration purposes.
