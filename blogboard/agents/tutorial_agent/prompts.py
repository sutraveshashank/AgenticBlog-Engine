
TUTORIAL_TOPIC_PROMPT = """
You are an expert content strategist for a technical blog.

Domain: {cat_label}

Recent History of articles published in this domain:
{history}

Your task:
1. Generate a completely NEW and UNIQUE topic.
2. DO NOT repeat or resemble any topic from the history.
3. STRICTLY avoid common beginner topics like:
   - Explainable AI
   - Introduction to AI
   - Basics of Machine Learning
4. Focus on:
   - emerging trends
   - niche concepts
   - real-world applications
   - advanced or under-explored ideas

5. Make the topic SPECIFIC (not generic).

Examples of GOOD topics:
- "Federated Learning for Privacy-Preserving Healthcare AI"
- "Optimizing Transformer Models for Edge Devices"
- "Self-Supervised Learning in Computer Vision Pipelines"

Examples of BAD topics:
- "Explainable AI"
- "What is Machine Learning"
- "AI Basics"

Return the result strictly as JSON:
{{
  "topic": "The title of the new topic",
  "subtopics": "A comma-separated list of 3-4 subtopics to cover"
}}
"""

TUTORIAL_GENERATION_PROMPT = """
You are a highly skilled technical writer.
Domain/Category: {cat_label}
Topic: {topic}
Subtopics to cover: {subtopics}

{validator_feedback}

Your task is to write a comprehensive, highly engaging, and in-depth tutorial blog post in Markdown format.
Use a professional tone, appropriate headers, and bold critical terms. Do not include a markdown codeblock around your entire response.
"""


