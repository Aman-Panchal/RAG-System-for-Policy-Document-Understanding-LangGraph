from app.graph.main_graph import build_graph

if __name__ == "__main__":
    graph = build_graph()

    while True:
        query = input("\nAsk something: ")

        if query == "exit":
            break

        send_email = input("Send email? (y/n): ").lower() == "y"
        user_email = ""

        if send_email:
            user_email = input("Enter email: ")

        result = graph.invoke({
            "query": query,
            "send_email": send_email,
            "user_email": user_email
        })

        print("\nFinal Answer:")
        print(result["answer"])

        if send_email:
            print("Email Status:", result.get("email_status"))
