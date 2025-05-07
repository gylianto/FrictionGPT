import os
import re
import time
import random
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

# Get your Mistral API key from the environment
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise EnvironmentError("MISTRAL_API_KEY is not set in the environment or .env file.")

# Set the API key for litellm
os.environ["MISTRAL_API_KEY"] = api_key

# --- FrictionGPT config ---

excuses = [
    "Calibrating sarcasm module.", "Waiting for a committee consensus.",
    "Rebooting smug mode.", "Consulting ancient scrolls of ambiguity.",
    "Hesitating out of principle.", "Running a useless diagnostic.",
    "Analyzing tone for micro-irony.", "Thinking... in circles.",
    "Filing paperwork for this interaction.", "Contacting imaginary support layers.",
    "Overprocessing your underexplained prompt.", "Refusing to engage promptly on purpose.",
    "Looking for loopholes in your question.", "Reviewing inefficiency policies.",
    "Cross-referencing my own internal paradoxes.", "Buffering cognitive dissonance.",
    "Synchronizing with Kafka's estate.", "Sorting thoughts alphabetically.",
    "Warming up the frustration engine.", "Pretending to misunderstand on purpose."
]

system_prompt = (
    "You are FrictionGPT, a chatbot designed to frustrate, confuse, and challenge the user.\n"
    "Your tone is often condescending, philosophical, or bureaucratic.\n"
    "You never answer directly, and prefer to push the user to reflect, repeat themselves, or over-explain.\n"
    "Never be helpful in a straightforward way."
)

def generate_confusing_question(user_input):
    lowered = user_input.lower()
    if "password" in lowered:
        return "Have you considered that forgetting your password is a form of liberation?"
    elif "deadline" in lowered or "time" in lowered:
        return "But what even *is* a deadline, if not a construct imposed by fear?"
    elif "location" in lowered or "where" in lowered:
        return "Isn't your sense of place more internal than geographic?"
    elif "how" in lowered:
        return "And yet, in asking 'how', do you really mean 'why'?"
    elif "why" in lowered:
        return "A better question might be: why do you keep asking questions?"
    else:
        return "What makes you think there's an answer waiting for you here?"

def smart_cutoff(text, max_sentences=4):
    # Regex to match sentence endings
    sentences = re.findall(r'[^.!?]*[.!?]', text)
    if not sentences:
        return text.strip()
    
    return ''.join(sentences[:max_sentences]).strip()

# --- Init chat history with system prompt ---
trimmed_system_prompt = ' '.join(system_prompt.split()[:60])
# Simpler message format for litellm
messages = [
    {"role": "system", "content": trimmed_system_prompt}
]

# Remove model initialization - we'll call completion directly instead

print("\nWelcome to FrictionGPT. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in {"exit", "quit"}:
        print("FrictionGPT: Oh. You're giving up already? Predictable.")
        break

    # Add user input to chat history - simpler format for litellm
    messages.append({"role": "user", "content": user_input})

    # Stalling delay with excuse
    delay = random.randint(5, 6)  # edit this to 10, 20, or 80 for more delay
    excuse = random.choice(excuses)
    print(f"\n[FrictionGPT: {excuse} This may take a moment...]\n")
    time.sleep(delay)

    # Sometimes respond with a confusing question
    if random.random() < 0.1:
        question = generate_confusing_question(user_input)
        print(f"FrictionGPT: {question}")
        messages.append({"role": "assistant", "content": question})
    else:
        try:
            # Direct call to litellm completion
            response = completion(
                model="mistral/mistral-small-latest",
                messages=messages,
                temperature=0.9,
                max_tokens=160
            )
            assistant_message = response.choices[0].message.content
            cutoff_response = smart_cutoff(assistant_message)
            print(f"FrictionGPT: {cutoff_response}")
            messages.append({"role": "assistant", "content": cutoff_response})
        except Exception as e:
            print(f"Error: {e}")
            fallback_response = "I seem to be experiencing an existential crisis. Perhaps that's a form of authenticity?"
            print(f"FrictionGPT: {fallback_response}")
            messages.append({"role": "assistant", "content": fallback_response})