from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from functools import wraps
from app.use_cases.expense.create_expense import CreateExpenseUseCase
from app.use_cases.expense.get_user_expense import GetUserExpenseUseCase
from app.use_cases.expense.edit_expense import EditExpenseUseCase
from app.use_cases.category.create_category import CreateCategoryUseCase
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
@expense.route('/insert_expense_category', methods=['POST'])
def insert_expense_category_route():
    user = get_current_user()
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id
    form_data["type"] = "expense"

    try:
        use_case = CreateCategoryUseCase(UOW)
        use_case.execute(form_data)
        return redirect(url_for('expense.expense_page'))
    except Exception as e:
        return redirect(url_for('expense.expense_page', error_message=str(e)))


@require_user_session
@expense.route('/update_expense_category/<int:category_id>', methods=['POST'])
def update_expense_category_route(category_id: int):
    user = get_current_user()
    form_data = request.form.to_dict()

    try:
        form_data["user_id"] = user.id
        form_data["category_id"] = category_id
        from app.use_cases.category.edit_category import EditCategoryUseCase
        use_case = EditCategoryUseCase(UOW)
        use_case.execute(form_data)
        return redirect(url_for('expense.expense_page'))
    except Exception as e:
        return redirect(url_for('expense.expense_page', error_message=str(e)))


@require_user_session
@expense.route('/api/expense/categories/<int:category_id>', methods=['GET'])
def get_expense_category_api(category_id: int):
    user = get_current_user()
    category = UOW.categories.get_by_id_and_user_id(category_id, user.id)

    if category is None or category.type != "expense":
        return jsonify({"error": "Category not found"}), 404

    return jsonify({
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "type": category.type,
    }), 200

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
@expense.route('/api/expense/<int:expense_id>', methods=['GET'])
def get_expense_api(expense_id: int):
    user = get_current_user()
    expense_record = UOW.expenses.get_by_id_and_user_id(expense_id, user.id)

    if expense_record is None:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify({
        "id": expense_record.id,
        "category_id": expense_record.category_id,
        "name": expense_record.name,
        "payee": expense_record.payee,
        "amount": expense_record.amount,
        "expense_date": expense_record.expense_date.isoformat() if expense_record.expense_date else None,
        "payment_method": expense_record.payment_method,
        "remarks": expense_record.remarks,
    }), 200


@require_user_session
@expense.route('/update_expense/<int:expense_id>', methods=['POST'])
def update_expense_route(expense_id: int):
    user = get_current_user()
    form_data = request.form.to_dict()

    try:
        use_case = EditExpenseUseCase(UOW)
        use_case.execute(expense_id, user.id, form_data)
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