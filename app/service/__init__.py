from werkzeug.security import check_password_hash, generate_password_hash
from app.ext import db
from app.service.s_Users import UserService 
from app.service.s_Admin import AdminService
from app.service.s_Income import IncomeService
from app.service.s_Expenses import ExpenseService
from app.service.s_Debts import DebtsService
from app.service.s_DebtPayments import DebtPaymentsService
from app.service.s_SavingTransactions import SavingTransactionsService


US_INS = UserService()
IS_INS = IncomeService()
ES_INS = ExpenseService()
DS_INS = DebtsService()
DPS_INS = DebtPaymentsService()
STS_INS = SavingTransactionsService()