import numpy as np

def precision_at_k(retrieved_ids, relevant_ids, k):
    retrieved_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    correct = len([r for r in retrieved_k if r in relevant_set])
    return correct / k


def recall_at_k(retrieved_ids, relevant_ids, k):
    retrieved_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    correct = len([r for r in retrieved_k if r in relevant_set])
    return correct / len(relevant_set)


def mean_reciprocal_rank(retrieved_ids, relevant_ids):
    relevant_set = set(relevant_ids)
    for idx, r in enumerate(retrieved_ids):
        if r in relevant_set:
            return 1 / (idx + 1)
    return 0
from rouge_score import rouge_scorer

def compute_rouge(generated, reference):
    scorer = rouge_scorer.RougeScorer(['rouge1','rouge2','rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return scores
from bert_score import score

def compute_bertscore(generated, reference):
    P, R, F1 = score([generated], [reference], lang="en")
    return {
        "Precision": float(P.mean()),
        "Recall": float(R.mean()),
        "F1": float(F1.mean())
    }