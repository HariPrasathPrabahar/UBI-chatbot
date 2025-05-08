from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load service data from file
with open("services.json") as f:
    services = json.load(f)

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    query = req['queryResult']['queryText'].lower()
    output_contexts = req['queryResult'].get('outputContexts', [])

    # Default values
    deposit_type = None
    account_type = None
    payment_type = None
    forex_type = None
    response = "I'm not sure how to help with that yet."

    # Extract parameters if present
    for ctx in output_contexts:
        params = ctx.get("parameters", {})
        deposit_type = params.get("deposit_type", deposit_type)
        account_type = params.get("account_type", account_type)
        payment_type = params.get("payment_type", payment_type)
        forex_type = params.get("forex_type", forex_type)

    # Handle deposits
    if "deposit" in query and not deposit_type:
        response = (
            "We offer the following types of deposits:\n"
            "1️⃣ Fixed Deposit\n"
            "2️⃣ Recurring Deposit\n\n"
            "Please type which one you're interested in."
        )
        return jsonify({
            "fulfillmentText": response,
            "outputContexts": [{
                "name": f"{req['session']}/contexts/awaiting_deposit_type",
                "lifespanCount": 5
            }]
        })

    if deposit_type:
        data = services["deposit"]["types"].get(deposit_type.replace(" ", "_"))
        if data:
            response = (
                f"Here are the details for {deposit_type.title()} Deposit:\n\n"
                f"💻 Online: {data['online']['link']}\nSteps: {data['online']['steps']}\n\n"
                f"📝 Offline: {data['offline']['form_link']}\nSteps: {data['offline']['steps']}\n\n"
                f"📊 Interest & Tenure Info: {data['info_link']}"
            )

    # Handle accounts
    elif "account" in query and not account_type:
        response = (
            "You can open the following types of accounts:\n"
            "1️⃣ Savings Account\n"
            "2️⃣ Current Account\n\n"
            "Which one are you interested in?"
        )
        return jsonify({
            "fulfillmentText": response,
            "outputContexts": [{
                "name": f"{req['session']}/contexts/awaiting_account_type",
                "lifespanCount": 5
            }]
        })

    elif account_type:
        data = services["account"]["types"].get(account_type.replace(" ", "_"))
        if data:
            response = (
                f"Here is how to open a {account_type.title()} Account:\n\n"
                f"💻 Online: {data['online']['link']}\nSteps: {data['online']['steps']}\n\n"
                f"📝 Offline: {data['offline']['form_link']}\nSteps: {data['offline']['steps']}"
            )

    # Handle payments
    elif payment_type:
        data = services["payment"].get(payment_type.upper())
        if data:
            response = (
                f"📌 {payment_type.upper()} Info:\n"
                f"➡️ Limit & Timing: {data['details']}\n\n"
                f"💻 Online: {data['online']['link']}\n"
                f"📝 Offline: {data['offline']['steps']}"
            )

    # Handle forex
    elif forex_type:
        data = services["forex"].get(forex_type.lower())
        if data:
            response = (
                f"🌍 {forex_type.title()} Info:\n\n"
                f"💻 Online: {data['online']['link']}\n"
                f"📝 Offline: {data['offline']['steps']}"
            )

    return jsonify({
        "fulfillmentText": response
    })

if __name__ == "__main__":
    app.run(debug=True)
