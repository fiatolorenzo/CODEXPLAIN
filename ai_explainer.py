"""This module imports the OpenAI library for use in AI applications."""

from openai import OpenAI

client = OpenAI()

def explain_finding(finding: dict) -> str:
    """This function retrieves the message from a given finding dictionary."""

    message = finding.get("message", "")
    symbol = finding.get("symbol", "")
    context_lines = finding.get("code_context", [])
    context = "\n".join(context_lines)

    prompt = f"""
    You are helping a beginner programmer.

    Explain the following Python issue clearly and briefly.

    Issue:
    {symbol} - {message}

    Code:
    {context}
    
    Respond using plain text (no markdown, no ** symbols).

    Respond in this format:

    Problem:
    <1-2 sentences>

    Why:
    <1-2 sentences>

    Fix:
    <short actionable fix>
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    explanation = response.choices[0].message.content.strip()
    return explanation

if __name__ == "__main__":
    test_finding = {
        "message": "Access to member before definition",
        "symbol": "E0203",
        "code_context": ["if self.value > 10:"]
    }

    result = explain_finding(test_finding)
    print(result)
