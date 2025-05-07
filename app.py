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
    response = "I'm not sure how to help with that yet."

    # Check if deposit type is already selected in the context
    for ctx in output_contexts:
        params = ctx.get("parameters", {})
        if "deposit_type" in params:
            deposit_type = params["deposit_type"].lower()

    # STEP 1: User asks to open a deposit (no type selected yet)
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

    # STEP 2: User specifies a type of deposit
    if deposit_type:
        deposit_data = services["deposit"]["types"].get(deposit_type.replace(" ", "_"))
        if deposit_data:
            response = (
                f"Here are the details for {deposit_type.title()}:\n\n"
                f"💻 **Online**\n"
                f"🔗 Link: {deposit_data['online']['link']}\n"
                f"🧾 Steps: {deposit_data['online']['steps']}\n\n"
                f"📝 **Offline**\n"
                f"🖨️ Form: {deposit_data['offline']['form_link']}\n"
                f"📋 Steps: {deposit_data['offline']['steps']}\n\n"
                f"📄 Interest Rate: {deposit_data['interest_rate']}\n"
                f"⏳ Tenure: {deposit_data['tenure']}"
            )
        else:
            response = f"Sorry, I couldn't find info for '{deposit_type}' deposit."

    return jsonify({
        "fulfillmentText": response
    })

if __name__ == "__main__":
    app.run(debug=True)
