def calculate_business_risk(extracted_data):
    business_risk_score = 0
    risk_messages = []

    if extracted_data.get("penalty_clause") == "Not specified":
        business_risk_score += 15
        risk_messages.append({
            "type": "warning",
            "message": "Penalty clause is missing."
        })

    if extracted_data.get("incoterms") == "Not specified":
        business_risk_score += 10
        risk_messages.append({
            "type": "warning",
            "message": "Incoterms are missing. Delivery responsibility is unclear."
        })

    if "advance" in extracted_data.get("payment_terms", "").lower():
        business_risk_score += 20
        risk_messages.append({
            "type": "error",
            "message": "Advance payment required. This increases financial risk."
        })

    if extracted_data.get("delivery_time", 0) >= 8:
        business_risk_score += 20
        risk_messages.append({
            "type": "warning",
            "message": "Long delivery time detected."
        })

    if extracted_data.get("price_change", 0) > 0 and extracted_data.get("price_change", 0) < 10:
        business_risk_score += 10
        risk_messages.append({
            "type": "warning",
            "message": "Small price increase detected."
        })

    elif extracted_data.get("price_change", 0) >= 10 and extracted_data.get("price_change", 0) < 20:
        business_risk_score += 20
        risk_messages.append({
            "type": "error",
            "message": "Medium price increase detected."
        })

    elif extracted_data.get("price_change", 0) >= 20:
        business_risk_score += 30
        risk_messages.append({
            "type": "error",
            "message": "High price increase detected."
        })

    if extracted_data.get("price_validity") == "Not specified":
        business_risk_score += 10
        risk_messages.append({
            "type": "warning",
            "message": "Price validity is missing."
        })

    if extracted_data.get("minimum_order_quantity", 0) > 0:
        business_risk_score += 10
        risk_messages.append({
            "type": "info",
            "message": f"Minimum order quantity found: {extracted_data.get('minimum_order_quantity')}"
        })

    if extracted_data.get("payment_terms") == "Not specified":
        business_risk_score += 10
        risk_messages.append({
            "type": "warning",
            "message": "Payment terms are missing."
        })
    
    if business_risk_score < 30:
        risk_level = "LOW"
    elif business_risk_score < 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return business_risk_score, risk_level, risk_messages