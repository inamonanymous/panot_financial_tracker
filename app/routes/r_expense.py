from flask import Blueprint, render_template, redirect, session, url_for, request
from functools import wraps
from app.use_cases.expense.create_expense import CreateExpenseUseCase
from app.use_cases.expense.get_user_expense import GetUserExpenseUseCase
from app.utils.exceptions.ServiceError import ServiceError
from app.routes.functions import require_user_session, get_current_user
#from app.use_cases.expense.get_user_expense import GetUserexpenseUseCase
#from app.use_cases.expense.create_expense import CreateexpenseUseCase
from app.service import UOW

expense = Blueprint(
    'expense',
    __name__,
    template_folder='templates',
    static_folder='statice'
)

@require_user_session
@expense.route('/insert_expense', methods=['POST'])
def insert_expense_route():
    user = get_current_user()
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id

    try:
        use_case = CreateExpenseUseCase(UOW)
        saved_expense = use_case.execute(form_data)
        return redirect(url_for('expense.expense_page'))
    except Exception as e:
        return redirect(url_for('expense.expense_page', error_message=str(e)))


@require_user_session
@expense.route('/expense', methods=['GET'])
def expense_page():
    user = get_current_user()
    error_message = request.args.get("error_message")
    use_case = GetUserExpenseUseCase(UOW)
    all_expense = use_case.execute(user.id)
    
    from app.use_cases.category.get_user_categories import GetUserCategoriesUseCase
    cat_use_case = GetUserCategoriesUseCase(UOW)
    user_categories = cat_use_case.execute(user.id, category_type="expense")

    return render_template("auth/pages/expense.html", 
                         user=user, 
                         expense=all_expense,
                         user_categories=user_categories,
                         error_message=error_message)# Pass to template