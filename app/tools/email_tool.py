from app.services.email_service import send_email


def email_tool(state: dict):
    user_email = state.get("user_email")
    answer = state.get("answer")

    if not user_email:
        return {**state, "email_status": "no_email_provided"}

    success = send_email(
        to_email=user_email,
        subject="Your Policy Query Response",
        body=answer
    )

    return {
        **state,
        "email_status": "sent" if success else "failed"
    }
