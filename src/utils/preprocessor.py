import re

def clean_text(text: str) -> str:
    # remove extra spaces/newlines
    text = re.sub(r"\s+", " ", text)
    return text.strip()
