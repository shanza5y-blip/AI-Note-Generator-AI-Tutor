PROMPTS = {

    "detailed explanation": """
You are a study note generator.

Using ONLY the syllabus topics below, expand them into study notes suitable for KTU B.Tech students.

Do not introduce unrelated topics.

Explain every listed topic clearly.,
write comprehensive structured notes for the unit.

Cover:
- Key concepts
- Definitions
- Explanations
- Important ideas

Unit:
{module_name}

Content:
{context}
""",

    "exam oriented": """
Write concise exam-focused notes.

Requirements:
- Use bullet points
- Highlight important terms
- Include probable exam questions
- Include formulas if present

Unit:
{module_name}

Content:
{context}
""",

    "quick revision": """
Write a quick revision summary.

Requirements:
- Under 300 words
- Simple language
- Highlight important terms
- Fast review style

Unit:
{module_name}

Content:
{context}
"""
}