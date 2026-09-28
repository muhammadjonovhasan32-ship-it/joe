import os

from openai import OpenAI


def main() -> None:
    """Run a simple command-line AI assistant."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY topilmadi. Uni muhit o'zgaruvchisi sifatida o'rnating."
        )

    client = OpenAI(api_key=api_key)
    print("Joe AI yordamchisi ishga tushdi. Chiqish uchun 'exit' yozing.")

    while True:
        question = input("Siz: ").strip()
        if question.lower() in {"exit", "quit", "chiqish"}:
            print("Joe: Ko'rishguncha!")
            break
        if not question:
            continue

        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions="Siz foydali, halol va qisqa javob beradigan AI yordamchisiz.",
            input=question,
        )
        print(f"Joe: {response.output_text}\n")


if __name__ == "__main__":
    main()
