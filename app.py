# Inside webhook() — Add this block after 'account_type' logic

    elif "payment" in query:
        response = (
            "We offer the following payment options:\n"
            "💳 NEFT - Batch-based transfer, credited within 2 hrs.\n"
            "⚡ RTGS - Real-time transfer for ₹2 lakh and above.\n"
            "🔁 IMPS - Instant 24x7 transfer.\n"
            "Please tell me which one you're interested in."
        )
        return jsonify({
            "fulfillmentText": response,
            "outputContexts": [{
                "name": f"{req['session']}/contexts/awaiting_payment_type",
                "lifespanCount": 5
            }]
        })

    elif "forex" in query:
        response = (
            "Our Forex services include:\n"
            "🌍 Inward/Outward Remittance\n"
            "📄 Bill Discounting\n"
            "📈 Forward Contracts\n"
            "💱 Currency Conversion\n"
            "Which one do you want help with?"
        )
        return jsonify({
            "fulfillmentText": response,
            "outputContexts": [{
                "name": f"{req['session']}/contexts/awaiting_forex_type",
                "lifespanCount": 5
            }]
        })

    elif "payment_type" in req["queryResult"]["parameters"]:
        payment_type = req["queryResult"]["parameters"]["payment_type"].lower().replace(" ", "_")
        payment_data = services["payment"]["types"].get(payment_type)
        if payment_data:
            response = (
                f"{payment_type.upper()}:\n"
                f"ℹ️ {payment_data['description']}\n"
                f"💰 Limits: {payment_data['limits']}\n\n"
                f"💻 Online:\n"
                f"🔗 {payment_data['online']['link']}\n"
                f"🧾 {payment_data['online']['steps']}\n\n"
                f"🏦 Offline:\n"
                f"{payment_data['offline']['steps']}"
            )
        else:
            response = f"Sorry, I couldn’t find info on '{payment_type}'."

    elif "forex_type" in req["queryResult"]["parameters"]:
        forex_type = req["queryResult"]["parameters"]["forex_type"].lower().replace(" ", "_")
        forex_data = services["forex"]["types"].get(forex_type)
        if forex_data:
            response = (
                f"{forex_type.replace('_', ' ').title()}:\n\n"
                f"💻 Online:\n"
                f"🔗 {forex_data['online']['link']}\n"
                f"🧾 {forex_data['online']['steps']}\n\n"
                f"🏦 Offline:\n"
                f"{forex_data['offline']['steps']}"
            )
        else:
            response = f"Sorry, I couldn’t find info on '{forex_type}'."
