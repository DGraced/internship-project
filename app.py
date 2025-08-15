from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data for demonstration purposes
utility_data = {
    "userId1": {
        "paymentHistory": [
            {"date": "2024-01-01", "amount": 100, "utility": "electricity", "paidOnTime": True},
            {"date": "2024-02-01", "amount": 110, "utility": "electricity", "paidOnTime": False, "daysLate": 5},
            # Add more entries as needed
        ],
        "accounts": {
            "electricity": {"startDate": "2023-01-01"},
            "water": {"startDate": "2023-06-01"},
            "internet": {"startDate": "2023-01-01"},
        }
    }
}

#1. payment consistency
def calculate_payment_consistency(userId):
    user_data = utility_data.get(userId)
    if not user_data:
        return None

    payments = user_data['paymentHistory']
    on_time_payments = sum(1 for p in payments if p.get('paidOnTime'))
    total_payments = len(payments)
    avg_days_early = sum(-p.get('daysLate', 0) for p in payments if p.get('daysLate', 0) < 0) / total_payments
    avg_days_late = sum(p.get('daysLate', 0) for p in payments if p.get('daysLate', 0) > 0) / total_payments

    return {
        "onTimePaymentPercentage": (on_time_payments / total_payments) * 100 if total_payments else 0,
        "averageDaysEarly": avg_days_early,
        "averageDaysLate": avg_days_late
    }

#2. payment default
def calculate_payment_defaults(userId):
    user_data = utility_data.get(userId)
    if not user_data:
        return None

    payments = user_data['paymentHistory']
    missed_payments = sum(1 for p in payments if not p.get('paidOnTime'))
    streaks = 0
    current_streak = 0
    max_streak = 0

    for p in payments:
        if p.get('paidOnTime'):
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0

    return {
        "missedPayments": missed_payments,
        "longestOnTimeStreak": max_streak
    }

#3. account history
def calculate_account_history(userId):
    user_data = utility_data.get(userId)
    if not user_data:
        return None

    accounts = user_data['accounts']
    account_lengths = {k: {"lengthInMonths": (2024 - int(v['startDate'][:4])) * 12 + (9 - int(v['startDate'][5:7]))} for k, v in accounts.items()}
    total_accounts = len(accounts)

    return {
        "accountHistory": account_lengths,
        "totalNumberOfAccounts": total_accounts
    }

#4. payment amounts
def calculate_payment_amounts(userId):
    user_data = utility_data.get(userId)
    if not user_data:
        return None

    payments = user_data['paymentHistory']
    utility_totals = {}
    utility_counts = {}

    for p in payments:
        utility = p['utility']
        utility_totals[utility] = utility_totals.get(utility, 0) + p['amount']
        utility_counts[utility] = utility_counts.get(utility, 0) + 1

    average_payments = {utility: utility_totals[utility] / utility_counts[utility] for utility in utility_totals}
    payment_trends = {utility: "stable" for utility in utility_totals} # Placeholder for trend calculation

    return {
        "averageMonthlyPayments": average_payments,
        "paymentTrends": payment_trends
    }

@app.route('/api/utility-bill-history/payment-consistency', methods=['GET'])
def get_payment_consistency():
    userId = request.args.get('userId')
    result = calculate_payment_consistency(userId)
    if result is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(result)

@app.route('/api/utility-bill-history/payment-defaults', methods=['GET'])
def get_payment_defaults():
    userId = request.args.get('userId')
    result = calculate_payment_defaults(userId)
    if result is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(result)

@app.route('/api/utility-bill-history/account-history', methods=['GET'])
def get_account_history():
    userId = request.args.get('userId')
    result = calculate_account_history(userId)
    if result is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(result)

@app.route('/api/utility-bill-history/payment-amounts', methods=['GET'])
def get_payment_amounts():
    userId = request.args.get('userId')
    result = calculate_payment_amounts(userId)
    if result is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)