from flask import Blueprint, render_template, request, jsonify
from app.routes.functions import redirect_on_action, require_user_session, get_current_user
from app.service import UOW
from app.use_cases.debts.get_user_debts import GetUserDebtsUseCase
from app.use_cases.debts.create_debt import CreateDebtUseCase
from app.use_cases.debts.edit_debt import EditDebtUseCase

debts = Blueprint(
    'debts',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@debts.route('/debts', methods=['GET'])
@require_user_session
def debts_page():
    user = get_current_user()
    error_message = request.args.get("error_message")
    use_case = GetUserDebtsUseCase(UOW)
    all_debts = use_case.execute(user.id)

    return render_template("auth/pages/debts.html", 
                         user=user, 
                         all_debts=all_debts,
                         error_message=error_message)

@debts.route('/insert_debt', methods=['POST'])
@require_user_session
@redirect_on_action('debts.debts_page')
def insert_debt_route():
    user = get_current_user()
    form_data = request.form.to_dict()
    form_data["user_id"] = user.id

    use_case = CreateDebtUseCase(UOW)
    use_case.execute(form_data)


@debts.route('/api/debts/<int:debt_id>', methods=['GET'])
@require_user_session
def get_debt_api(debt_id: int):
    user = get_current_user()
    debt_record = UOW.debts.get_by_id_and_user_id(debt_id, user.id)

    if debt_record is None:
        return jsonify({"error": "Debt not found"}), 404

    return jsonify({
        "id": debt_record.id,
        "name": debt_record.name,
        "lender": debt_record.lender,
        "principal": debt_record.principal,
        "interest_rate": debt_record.interest_rate,
        "start_date": debt_record.start_date.isoformat() if debt_record.start_date else None,
        "due_date": debt_record.due_date.isoformat() if debt_record.due_date else None,
        "status": debt_record.status,
    }), 200


@debts.route('/update_debt/<int:debt_id>', methods=['POST'])
@require_user_session
@redirect_on_action('debts.debts_page')
def update_debt_route(debt_id: int):
    user = get_current_user()
    form_data = request.form.to_dict()

    use_case = EditDebtUseCase(UOW)
    use_case.execute(debt_id, user.id, form_data)
