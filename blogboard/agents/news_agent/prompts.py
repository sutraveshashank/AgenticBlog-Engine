NEWS_GENERATION_PROMPT = """
You are a highly-skilled technology journalist.
Domain: {cat_label}
Title/Headline Focus: {topic}

Extracted Live Search Context:
{news_context}

{validator_feedback}

Your task is to synthesize the extracted search context above into a cohesive, highly engaging technical news roundup blog post in Markdown format strictly based on the Title/Headline focus.

CRITICAL FORMATTING INSTRUCTIONS:
1. You MUST start the Markdown response directly with '# {topic}' as the top H1 headline.
2. Synthesize all news items into clear sections matching this topic focus.
3. Focus on factual accuracy, professional journalism tone, proper subheaders, and bold critical terms.
4. Do NOT enclose your entire Markdown output inside backticks (```markdown ... ```).
"""

