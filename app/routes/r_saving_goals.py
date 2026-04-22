from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.routes.functions import redirect_on_action, require_user_session, get_current_user
from app.service import UOW
from app.use_cases.saving_goals.get_user_saving_goals import GetUserSavingGoalsUseCase
from app.use_cases.saving_goals.get_saving_goal_details import GetSavingGoalDetailsUseCase
from app.use_cases.saving_goals.add_saving_goal_payment import AddSavingGoalPaymentUseCase
# TODO: Add other use cases as they are created
# from app.use_cases.saving_goals.create_saving_goal import CreateSavingGoalUseCase
# from app.use_cases.saving_goals.edit_saving_goal import EditSavingGoalUseCase
# from app.use_cases.saving_goals.delete_saving_goal import DeleteSavingGoalUseCase

saving_goals = Blueprint(
    'saving_goals',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@saving_goals.route('/saving_goals', methods=['GET'])
@require_user_session
def saving_goals_page():
    user = get_current_user()
    error_message = request.args.get("error_message")
    use_case = GetUserSavingGoalsUseCase(UOW)
    all_saving_goals = use_case.execute(user.id)

    return render_template("auth/pages/saving_goals/index.html",
                         user=user,
                         all_saving_goals=all_saving_goals,
                         error_message=error_message)

@saving_goals.route('/add_saving_goal_payment/<int:goal_id>', methods=['POST'])
@require_user_session
@redirect_on_action('saving_goals.saving_goals_page')
def add_saving_goal_payment_route(goal_id: int):
    user = get_current_user()
    
    # Get form data
    amount = request.form.get('amount')
    expense_date = request.form.get('expense_date')
    payment_method = request.form.get('payment_method', 'cash')
    remarks = request.form.get('remarks', '')
    
    # Prepare data for use case
    saving_payment_data = {
        'user_id': user.id,
        'goal_id': goal_id,
        'txt_type': 'deposit'
    }
    
    expense_data = {
        'user_id': user.id,
        'amount': amount,
        'expense_date': expense_date,
        'payment_method': payment_method,
        'remarks': remarks
    }
    
    use_case = AddSavingGoalPaymentUseCase(UOW)
    use_case.execute(saving_payment_data, expense_data)

@saving_goals.route('/saving_goal_details/<int:goal_id>')
@require_user_session
def saving_goal_details_page(goal_id: int):
    user = get_current_user()
    error_message = request.args.get("error_message")

    use_case = GetSavingGoalDetailsUseCase(UOW)
    try:
        data = use_case.execute(goal_id, user.id)
    except Exception:
        return redirect(url_for('saving_goals.saving_goals_page', error_message="Saving goal not found"))
    
    return render_template("auth/pages/saving_goals/details.html",
                         user=user,
                         goal=data['goal'],
                         payments=data['payments'],
                         error_message=error_message)