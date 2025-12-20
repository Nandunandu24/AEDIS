def generate_llm_response(email_text: str, sentiment: float) -> str:
    """
    Generates a customer response with tone adapted to sentiment.
    """

    if sentiment < -0.4:
        tone = (
            "We understand your frustration and appreciate your patience. "
        )
    elif sentiment > 0.3:
        tone = (
            "Thank you for reaching out. "
        )
    else:
        tone = (
            "Thank you for contacting us. "
        )

    body = (
        "Your request has been reviewed and is currently being handled within our standard timeline. "
        "If any additional information is required, we will contact you. "
        "Please feel free to reply if you need further assistance."
    )

    return tone + body
