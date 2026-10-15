import json
import re

import gradio as gr
from textblob import TextBlob


# ---------------------------------------------------------------------------
# Helpers (provided). They avoid TextBlob features that need extra downloads.
# ---------------------------------------------------------------------------
def split_sentences(text):
    """Split text into sentences on . ! or ? followed by whitespace."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def split_words(text):
    """Return the words in text (letters, digits, and apostrophes)."""
    return re.findall(r"[A-Za-z0-9']+", text)


# ---------------------------------------------------------------------------
# Tool 1 (provided): from the Hugging Face MCP Course, Unit 2
# ---------------------------------------------------------------------------
def sentiment_analysis(text: str) -> str:
    """
    Analyze the sentiment of the given text.

    Args:
        text (str): The text to analyze

    Returns:
        str: A JSON string containing polarity, subjectivity, and assessment
    """
    sentiment = TextBlob(text).sentiment
    result = {
        "polarity": round(sentiment.polarity, 2),          # -1 (negative) to 1 (positive)
        "subjectivity": round(sentiment.subjectivity, 2),  # 0 (objective) to 1 (subjective)
        "assessment": "positive" if sentiment.polarity > 0
                      else "negative" if sentiment.polarity < 0 else "neutral",
    }
    return json.dumps(result)


# ---------------------------------------------------------------------------
# Tool 2: word and sentence counts
# ---------------------------------------------------------------------------
def text_statistics(text: str) -> str:
    # TODO 1: write a Google-style docstring (summary line, Args:, Returns:)
    # TODO 1: return json.dumps of {"word_count", "sentence_count",
    #         "avg_sentence_length"} using split_words / split_sentences.
    #         Round the average to 1 decimal; guard against 0 sentences.
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Tool 3: rank sentences by sentiment
# ---------------------------------------------------------------------------
def rank_sentences(text: str, order: str, top_k: int) -> str:
    # TODO 2: write a docstring whose Args: block describes ALL three parameters
    # TODO 2: score each sentence with TextBlob(sentence).sentiment.polarity,
    #         sort by order ("most_positive" = highest first,
    #         "most_negative" = lowest first), and return json.dumps of the
    #         first top_k items as [{"sentence": ..., "polarity": ...}, ...]
    raise NotImplementedError


# ---------------------------------------------------------------------------
# One gr.Interface per tool. Each becomes one tab in the UI AND one MCP tool.
# ---------------------------------------------------------------------------
demo = gr.TabbedInterface(
    [
        gr.Interface(fn=sentiment_analysis, inputs=gr.Textbox(label="Text"), outputs=gr.Textbox()),
        # TODO 3: add a gr.Interface for text_statistics (one Textbox in, one out)
        # TODO 3: add a gr.Interface for rank_sentences with three inputs:
        #         gr.Textbox, gr.Radio(["most_positive", "most_negative"], value=...),
        #         and gr.Number(value=3, precision=0)
    ],
    tab_names=["Sentiment"],  # TODO 3: one name per tab
    title="Review Toolkit",
)

if __name__ == "__main__":
    demo.launch()  # TODO 4: start the MCP server and create a public share link
