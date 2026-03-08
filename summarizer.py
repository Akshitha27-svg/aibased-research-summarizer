def create_summary_prompt(context):

    prompt = f"""
Write a structured research paper summary with:

1. Research Objective
2. Methodology
3. Key Findings
4. Contributions

Context:
{context}
"""

    return prompt