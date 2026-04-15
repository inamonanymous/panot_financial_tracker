from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.routes.functions import redirect_on_action, require_user_session, get_current_user
from app.service import UOW
from app.use_cases.debts.get_user_debts import GetUserDebtsUseCase
from app.use_cases.debts.get_debt_details import GetDebtDetailsUseCase
from app.use_cases.debts.create_debt import CreateDebtUseCase
from app.use_cases.debts.edit_debt import EditDebtUseCase
from app.use_cases.debts.delete_debt import DeleteDebtUseCase
from app.use_cases.debts.add_debt_payment import AddDebtPaymentUseCase

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

@debts.route('/debt_details/<int:debt_id>', methods=['GET'])
@require_user_session
def debt_details_page(debt_id: int):
    user = get_current_user()
    error_message = request.args.get("error_message")
    try:
        use_case = GetDebtDetailsUseCase(UOW)
        data = use_case.execute(debt_id, user.id)
        return render_template("auth/pages/debt_details.html", 
                             user=user, 
                             debt=data['debt'],
                             payments=data['payments'],
                             error_message=error_message)
    except Exception as e:
        return render_template("auth/pages/debts.html", user=user, error_message=str(e))

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


@debts.route('/add_debt_payment/<int:debt_id>', methods=['POST'])
@require_user_session
def add_debt_payment_route(debt_id: int):
    user = get_current_user()
    form_data = request.form.to_dict()

    payment_data = {
        'amount': float(form_data.get('amount')),
        'payment_date': form_data.get('payment_date'),
        'payment_method': form_data.get('payment_method', 'cash'),
        'remarks': form_data.get('remarks', '')
    }

    use_case = AddDebtPaymentUseCase(UOW)
    try:
        use_case.execute(debt_id, user.id, payment_data)
        return redirect(url_for('debts.debt_details_page', debt_id=debt_id))
    except Exception as e:
        return redirect(url_for('debts.debt_details_page', debt_id=debt_id, error_message=str(e)))


@debts.route('/delete_debt/<int:debt_id>', methods=['POST'])
@require_user_session
@redirect_on_action('debts.debts_page')
def delete_debt_route(debt_id: int):
    user = get_current_user()

    use_case = DeleteDebtUseCase(UOW)
    use_case.execute(debt_id, user.id)
