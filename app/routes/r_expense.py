from flask import Blueprint, render_template, request, jsonify
from app.use_cases.expense.create_expense import CreateExpenseUseCase
from app.use_cases.expense.get_user_expense import GetUserExpenseUseCase
from app.use_cases.expense.edit_expense import EditExpenseUseCase
from app.use_cases.expense.delete_expense import DeleteExpenseUseCase
from app.use_cases.category.create_category import CreateCategoryUseCase
from app.use_cases.category.delete_category import DeleteCategoryUseCase
from app.routes.functions import redirect_on_action, require_user_session, get_current_user
from app.service import UOW

expense = Blueprint(
    'expense',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@expense.route('/insert_expense_category', methods=['POST'])
@require_user_session
@redirect_on_action('expense.expense_page')
def insert_expense_category_route():
    user = get_current_user()
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id
    form_data["type"] = "expense"
    use_case = CreateCategoryUseCase(UOW)
    use_case.execute(form_data)


@expense.route('/update_expense_category/<int:category_id>', methods=['POST'])
@require_user_session
@redirect_on_action('expense.expense_page')
def update_expense_category_route(category_id: int):
    user = get_current_user()
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id
    form_data["category_id"] = category_id
    from app.use_cases.category.edit_category import EditCategoryUseCase
    use_case = EditCategoryUseCase(UOW)
    use_case.execute(form_data)

@expense.route('/delete_expense_category/<int:category_id>', methods=['POST'])
@require_user_session
@redirect_on_action('expense.expense_page')
def delete_expense_category_route(category_id: int):
    user = get_current_user()
    use_case = DeleteCategoryUseCase(UOW)
    use_case.execute(category_id, user.id)

@expense.route('/api/expense/categories/<int:category_id>', methods=['GET'])
@require_user_session
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

@expense.route('/insert_expense', methods=['POST'])
@require_user_session
@redirect_on_action('expense.expense_page')
def insert_expense_route():
    user = get_current_user()
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id

    use_case = CreateExpenseUseCase(UOW)
    use_case.execute(form_data)


@expense.route('/api/expense/<int:expense_id>', methods=['GET'])
@require_user_session
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


@expense.route('/update_expense/<int:expense_id>', methods=['POST'])
@require_user_session
@redirect_on_action('expense.expense_page')
def update_expense_route(expense_id: int):
    user = get_current_user()
    form_data = request.form.to_dict()
    use_case = EditExpenseUseCase(UOW)
    use_case.execute(expense_id, user.id, form_data)


@expense.route('/delete_expense/<int:expense_id>', methods=['POST'])
@require_user_session
@redirect_on_action('expense.expense_page')
def delete_expense_route(expense_id: int):
    user = get_current_user()
    use_case = DeleteExpenseUseCase(UOW)
    use_case.execute(expense_id, user.id)


@expense.route('/expense', methods=['GET'])
@require_user_session
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
                         error_message=error_message)