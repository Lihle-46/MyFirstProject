from flask import Flask, render_template, request
import os
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'

# Global DataFrame to store the uploaded data
global_df = None

def process_excel(file_path):
    df = pd.read_excel(file_path)
    # Calculate stats
    highest_income_month = df.loc[df['Income'].idxmax(), 'Month']
    lowest_income_month = df.loc[df['Income'].idxmin(), 'Month']
    highest_expense_month = df.loc[df['Expense'].idxmax(), 'Month']
    lowest_expense_month = df.loc[df['Expense'].idxmin(), 'Month']
    average_income = df['Income'].mean()
    average_expense = df['Expense'].mean()
    stats = {
        'highest_income_month': highest_income_month,
        'lowest_income_month': lowest_income_month,
        'highest_expense_month': highest_expense_month,
        'lowest_expense_month': lowest_expense_month,
        'average_income': f"{average_income:.2f}",
        'average_expense': f"{average_expense:.2f}"
    }
    # Generate graphs with analysis
    graph_dir = os.path.join('static', 'graphs')
    os.makedirs(graph_dir, exist_ok=True)
    # Line graph with analysis
    plt.figure(figsize=(10,5))
    plt.plot(df['Month'], df['Income'], marker='o', label='Income')
    plt.plot(df['Month'], df['Expense'], marker='o', label='Expense')
    plt.title('Income and Expense Over Months')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.legend()
    # Annotate highest/lowest points using month names
    max_income_idx = df['Income'].idxmax()
    min_income_idx = df['Income'].idxmin()
    max_expense_idx = df['Expense'].idxmax()
    min_expense_idx = df['Expense'].idxmin()
    plt.annotate('Highest Income', (df['Month'][max_income_idx], df['Income'][max_income_idx]),
                 textcoords="offset points", xytext=(0,10), ha='center', color='green', fontsize=9, arrowprops=dict(arrowstyle='->', color='green'))
    plt.annotate('Lowest Income', (df['Month'][min_income_idx], df['Income'][min_income_idx]),
                 textcoords="offset points", xytext=(0,-15), ha='center', color='red', fontsize=9, arrowprops=dict(arrowstyle='->', color='red'))
    plt.annotate('Highest Expense', (df['Month'][max_expense_idx], df['Expense'][max_expense_idx]),
                 textcoords="offset points", xytext=(0,10), ha='center', color='purple', fontsize=9, arrowprops=dict(arrowstyle='->', color='purple'))
    plt.annotate('Lowest Expense', (df['Month'][min_expense_idx], df['Expense'][min_expense_idx]),
                 textcoords="offset points", xytext=(0,-15), ha='center', color='orange', fontsize=9, arrowprops=dict(arrowstyle='->', color='orange'))
    line_path = os.path.join(graph_dir, 'line.png')
    plt.tight_layout()
    plt.savefig(line_path)
    plt.close()
    # Bar graph with analysis
    plt.figure(figsize=(10,5))
    width = 0.35
    x = range(len(df['Month']))
    plt.bar(x, df['Income'], width=width, label='Income')
    plt.bar([i+width for i in x], df['Expense'], width=width, label='Expense')
    plt.xticks([i+width/2 for i in x], df['Month'], rotation=45)
    plt.title('Income vs Expense by Month')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.legend()
    # Annotate bars using month names
    plt.text(max_income_idx, df['Income'][max_income_idx]+200, 'Highest Income', ha='center', color='green', fontsize=8)
    plt.text(min_income_idx, df['Income'][min_income_idx]-400, 'Lowest Income', ha='center', color='red', fontsize=8)
    plt.text(max_expense_idx+width, df['Expense'][max_expense_idx]+200, 'Highest Expense', ha='center', color='purple', fontsize=8)
    plt.text(min_expense_idx+width, df['Expense'][min_expense_idx]-400, 'Lowest Expense', ha='center', color='orange', fontsize=8)
    bar_path = os.path.join(graph_dir, 'bar.png')
    plt.tight_layout()
    plt.savefig(bar_path)
    plt.close()
    # Pie chart (Income distribution)
    plt.figure(figsize=(5,5))
    plt.pie(df['Income'], labels=df['Month'], autopct='%1.1f%%')
    plt.title('Income Distribution by Month')
    pie_path = os.path.join(graph_dir, 'pie.png')
    plt.savefig(pie_path)
    plt.close()
    # Histogram (Expense)
    plt.figure(figsize=(6,4))
    plt.hist(df['Expense'], bins=6, color='orange', edgecolor='black')
    plt.title('Expense Histogram')
    plt.xlabel('Expense')
    plt.ylabel('Frequency')
    hist_path = os.path.join(graph_dir, 'hist.png')
    plt.tight_layout()
    plt.savefig(hist_path)
    plt.close()
    # Return correct static paths for HTML
    graph_paths = {
        'line': f'graphs/line.png',
        'bar': f'graphs/bar.png',
        'pie': f'graphs/pie.png',
        'hist': f'graphs/hist.png'
    }
    return df, stats, graph_paths

@app.route("/", methods=["GET", "POST"])
def index():
    global global_df
    selected_graph = 'line'
    if request.method == "POST":
        try:
            selected_graph = request.form.get('selected_graph', 'line')
            if "file" not in request.files:
                return "No file uploaded", 400
            file = request.files["file"]
            if file.filename == "":
                return "No file selected", 400
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                df, stats, graph_paths = process_excel(file_path)
                global_df = df  # Store for later use
                if 'Month' not in df.columns:
                    return "Excel file must contain a 'Month' column.", 400
                try:
                    import datetime
                    current_year = datetime.datetime.now().year
                    months = pd.to_datetime(df['Month'] + ' ' + str(current_year), format='%B %Y').dt.strftime("%B %Y").tolist()
                except Exception as e:
                    return f"Error parsing 'Month' column: {e}", 400
                request.session = {
                    "stats": stats,
                    "graph_paths": graph_paths,
                    "months": months
                }
                # Only show the selected graph on results page
                return render_template("results.html", stats=stats, graph_paths=graph_paths, months=months, selected_graph=selected_graph)
        except Exception as e:
            return f"An error occurred: {e}", 500
    return render_template("index.html")

@app.route("/details/<month>")
def details(month):
    global global_df
    import datetime
    current_year = datetime.datetime.now().year
    # Convert month back to original name (e.g., 'January 2025' -> 'January')
    try:
        month_name = datetime.datetime.strptime(month, "%B %Y").strftime("%B")
        row = global_df[global_df['Month'].str.lower() == month_name.lower()]
        if not row.empty:
            data = {
                "Income": int(row.iloc[0]["Income"]),
                "Expense": int(row.iloc[0]["Expense"])
            }
        else:
            data = {"Income": "N/A", "Expense": "N/A"}
    except Exception as e:
        data = {"Income": "Error", "Expense": str(e)}
    return render_template("month_details.html", month=month, data=data)

if __name__ == "__main__":
    app.run(debug=True)
