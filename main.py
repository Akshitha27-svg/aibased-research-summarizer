from hybrid_rag_pipeline import hybrid_rag_pipeline

def main():
    print("\n==============================")
    print("  AI Research Paper Summarizer")
    print("  Hybrid RAG Pipeline Demo")
    print("==============================\n")

    query = input("Enter your research query: ")

    print("\nRunning Hybrid RAG Pipeline...\n")

    summary = hybrid_rag_pipeline(query)

    print("\n==============================")
    print("Generated Summary:")
    print("==============================\n")

    print(summary)
    print("\nPipeline execution completed.\n")


if __name__ == "__main__":
    main()
