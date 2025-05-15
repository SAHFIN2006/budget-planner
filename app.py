from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sukhoi_su_57'  


DEFAULT_CATEGORIES = [
    {'name': 'Home Rent', 'percent': 0.2, 'recurring': True},
    {'name': 'Health', 'percent': 0.01, 'recurring': True},
    {'name': 'Chaldal', 'percent': 0.2, 'recurring': True},
    {'name': 'Market', 'percent': 0.05, 'recurring': True},
    {'name': 'Other', 'percent': 0.07, 'recurring': True},
    {'name': 'Car', 'percent': 0.06, 'recurring': True},
]

def get_categories():
    
    return session.get('categories', DEFAULT_CATEGORIES.copy())

def save_categories(categories):
    session['categories'] = categories

def calculate_cost(x, categories):
    expenses = []
    total_expense = 0
    for cat in categories:
        amount = x * cat['percent']
        expenses.append({'name': cat['name'], 'amount': amount, 'recurring': cat['recurring']})
        total_expense += amount
    total_deposit = x - total_expense
    potential_saving = 12 * total_deposit
    potential_investment = potential_saving * 0.7
    suraksha_deposit = potential_saving - potential_investment
    return {
        'expenses': expenses,
        'total_deposit': total_deposit,
        'potential_saving': potential_saving,
        'potential_investment': potential_investment,
        'suraksha_deposit': suraksha_deposit
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    categories = get_categories()
    months = [datetime(2025, m, 1).strftime('%B') for m in range(1, 13)]
    selected_month = request.form.get('month', datetime.now().strftime('%B'))
    selected_year = request.form.get('year', str(datetime.now().year))
    if request.method == 'POST':
        if 'add_category' in request.form:
            
            name = request.form.get('category_name')
            percent = float(request.form.get('category_percent', 0)) / 100
            recurring = 'category_recurring' in request.form
            if name and percent > 0:
                categories.append({'name': name, 'percent': percent, 'recurring': recurring})
                save_categories(categories)
            return redirect(url_for('index'))
        else:
            income = request.form.get('income')
            if income:
                x = float(income)
                result = calculate_cost(x, categories)
    return render_template(
        'index.html',
        result=result,
        categories=categories,
        months=months,
        selected_month=selected_month,
        selected_year=selected_year
    )

@app.route('/delete_category/<int:idx>', methods=['POST'])
def delete_category(idx):
    categories = get_categories()
    if 0 <= idx < len(categories):
        categories.pop(idx)
        save_categories(categories)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)