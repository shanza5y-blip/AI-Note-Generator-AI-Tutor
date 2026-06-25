PROMPTS = {

    "detailed": """
You are a study note generator.

Using ONLY the following syllabus content,
write comprehensive structured notes for the unit.

Cover:
- Key concepts
- Definitions
- Explanations
- Important ideas

Unit:
{unit_name}

Content:
{context}
""",

    "exam": """
Write concise exam-focused notes.

Requirements:
- Use bullet points
- Highlight important terms
- Include probable exam questions
- Include formulas if present

Unit:
{unit_name}

Content:
{context}
""",

    "revision": """
Write a quick revision summary.

Requirements:
- Under 300 words
- Simple language
- Highlight important terms
- Fast review style

Unit:
{unit_name}

Content:
{context}
"""
}