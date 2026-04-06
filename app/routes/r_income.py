from flask import Blueprint, render_template, request, jsonify
from app.use_cases.category.create_category import CreateCategoryUseCase
from app.routes.functions import require_user_session, get_current_user, redirect_on_action
from app.use_cases.income.get_user_income import GetUserIncomeUseCase
from app.use_cases.income.create_income import CreateIncomeUseCase
from app.use_cases.income.edit_income import EditIncomeUseCase
from app.use_cases.income.delete_income import DeleteIncomeUseCase
from app.use_cases.category.delete_category import DeleteCategoryUseCase
from app.service import UOW

income = Blueprint(
    'income',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@income.route('/insert_income_category', methods=['POST'])
@require_user_session
@redirect_on_action('income.income_page')
def insert_income_category_route():
    user = get_current_user()
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id
    form_data["type"] = "income"  # Set type to income for this route

    use_case = CreateCategoryUseCase(UOW)
    use_case.execute(form_data)

@income.route('/update_income_category/<int:category_id>', methods=['POST'])
@require_user_session
@redirect_on_action('income.income_page')
def update_income_category_route(category_id: int):
    user = get_current_user()
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id
    form_data["category_id"] = category_id
    from app.use_cases.category.edit_category import EditCategoryUseCase
    use_case = EditCategoryUseCase(UOW)
    use_case.execute(form_data)


@income.route('/delete_income_category/<int:category_id>', methods=['POST'])
@require_user_session
@redirect_on_action('income.income_page')
def delete_income_category_route(category_id: int):
    user = get_current_user()

    use_case = DeleteCategoryUseCase(UOW)
    use_case.execute(category_id, user.id)

@income.route('/api/income/categories/<int:category_id>', methods=['GET'])
@require_user_session
def get_income_category_api(category_id: int):
    user = get_current_user()
    category = UOW.categories.get_by_id_and_user_id(category_id, user.id)

    if category is None or category.type != "income":
        return jsonify({"error": "Category not found"}), 404

    return jsonify({
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "type": category.type
    }), 200

@income.route('/insert_income', methods=['POST'])
@require_user_session
@redirect_on_action('income.income_page')
def insert_income_route():
    user = get_current_user()
    
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id

    use_case = CreateIncomeUseCase(UOW)
    use_case.execute(form_data)


@income.route('/api/income/<int:income_id>', methods=['GET'])
@require_user_session
def get_income_api(income_id: int):
    user = get_current_user()
    income_record = UOW.incomes.get_by_id_and_user_id(income_id, user.id)

    if income_record is None:
        return jsonify({"error": "Income not found"}), 404

    return jsonify({
        "id": income_record.id,
        "category_id": income_record.category_id,
        "name": income_record.name,
        "source": income_record.source,
        "amount": income_record.amount,
        "received_date": income_record.received_date.isoformat() if income_record.received_date else None,
        "payment_method": income_record.payment_method,
        "remarks": income_record.remarks,
    }), 200


@income.route('/update_income/<int:income_id>', methods=['POST'])
@require_user_session
@redirect_on_action('income.income_page')
def update_income_route(income_id: int):
    user = get_current_user()
    form_data = request.form.to_dict()

    use_case = EditIncomeUseCase(UOW)
    use_case.execute(income_id, user.id, form_data)


@income.route('/delete_income/<int:income_id>', methods=['POST'])
@require_user_session
@redirect_on_action('income.income_page')
def delete_income_route(income_id: int):
    user = get_current_user()

    use_case = DeleteIncomeUseCase(UOW)
    use_case.execute(income_id, user.id)
    
@income.route('/income', methods=['GET'])
@require_user_session
def income_page():
    user = get_current_user()
    error_message = request.args.get("error_message")
    use_case = GetUserIncomeUseCase(UOW)
    all_income = use_case.execute(user.id)
    
    # ADD THIS: Get user's income categories for the modal dropdown
    from app.use_cases.category.get_user_categories import GetUserCategoriesUseCase
    cat_use_case = GetUserCategoriesUseCase(UOW)
    user_categories = cat_use_case.execute(user.id, category_type="income")

    return render_template("auth/pages/income.html", 
                         user=user, 
                         all_income=all_income,
                         user_categories=user_categories,
                         error_message=error_message)# Pass to template