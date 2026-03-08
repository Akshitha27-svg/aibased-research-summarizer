chat_history = []

def add_message(question, answer):
    chat_history.append({
        "question": question,
        "answer": answer
    })

def get_history():
    return chat_history