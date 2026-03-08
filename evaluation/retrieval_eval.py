import json
from rag.vector_retriever import vector_search
from rag.hybrid_retriever import hybrid_search


def precision_at_k(retrieved_ids, relevant_ids, k):
    retrieved_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    correct = len([r for r in retrieved_k if r in relevant_set])
    return correct / k


def evaluate():
    with open("evaluation/test_queries.json", "r") as f:
        test_data = json.load(f)

    for test in test_data:
        query = test["query"]
        relevant = test["relevant_papers"]

        vector_results = vector_search(query)
        hybrid_results = hybrid_search(query)

        p_vector = precision_at_k(vector_results, relevant, 5)
        p_hybrid = precision_at_k(hybrid_results, relevant, 5)

        print("Query:", query)
        print("Vector Precision@5:", p_vector)
        print("Hybrid Precision@5:", p_hybrid)
        print("-" * 40)


if __name__ == "__main__":
    evaluate()
