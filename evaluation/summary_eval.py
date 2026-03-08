from rag.llm_pipeline import generate_summary


def evaluate_summary():
    query = "AI in healthcare"

    summary = generate_summary(query)

    print("Generated Summary:")
    print(summary)


if __name__ == "__main__":
    evaluate_summary()
