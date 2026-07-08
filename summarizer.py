import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

MODEL = "llama-3.3-70b-versatile"


def _try_parse(s):
    """Parse JSON, tolerating literal control characters (e.g. raw newlines)
    that the model sometimes puts inside string values."""
    try:
        return json.loads(s, strict=False)
    except json.JSONDecodeError:
        return None


def summarize(text: str, style: str = "concise", length: str = "medium") -> dict:
    system_prompt = """You are an expert text summarizer. Your job is to distill text into clear, accurate summaries without losing important information.
Always respond in valid JSON with keys: "summary" and "key_points" (a list of 3-5 strings)."""

    style_instructions = {
        "concise":  "Write a clear, concise summary in flowing prose.",
        "bullets":  "Write the summary as bullet points, each on a new line starting with •",
        "eli5":     "Explain this like I'm 5 years old. Use very simple words and analogies.",
        "academic": "Write a formal academic-style abstract with precise language.",
    }

    length_instructions = {
        "short":  "Keep it under 50 words.",
        "medium": "Aim for 100-150 words.",
        "long":   "Be thorough, around 200-250 words.",
    }

    user_prompt = f"""Please summarize the following text.

Style: {style_instructions.get(style, style_instructions['concise'])}
Length: {length_instructions.get(length, length_instructions['medium'])}

TEXT TO SUMMARIZE:
\"\"\"
{text}
\"\"\"

Respond ONLY with a single, flat JSON object in this exact format — do not nest JSON inside the "summary" string, do not escape or re-encode the JSON, and do not wrap it in markdown code fences:
{{
  "summary": "your summary here as plain text",
  "key_points": ["point 1", "point 2", "point 3"]
}}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    parsed = _try_parse(raw)

    if isinstance(parsed, dict):
        result = parsed
    elif isinstance(parsed, str):
        inner = _try_parse(parsed)
        result = inner if isinstance(inner, dict) else {"summary": parsed, "key_points": []}
    else:
        result = {"summary": raw, "key_points": []}

    summary_val = result.get("summary", "")
    if isinstance(summary_val, str) and summary_val.strip().startswith("{"):
        nested = _try_parse(summary_val)
        if isinstance(nested, dict) and "summary" in nested:
            result["summary"] = nested["summary"]
            if not result.get("key_points"):
                result["key_points"] = nested.get("key_points", [])

    if not isinstance(result.get("summary"), str):
        result["summary"] = str(result.get("summary", ""))
    result.setdefault("key_points", [])

    result["word_count_original"] = len(text.split())
    result["word_count_summary"]  = len(result["summary"].split())
    result["compression_ratio"]   = round((1 - result["word_count_summary"] / max(result["word_count_original"], 1)) * 100, 1)

    return result

