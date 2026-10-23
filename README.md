
# Cognetix Support Chatbot

## Objective
Build a customer support chatbot for a fictional electronics store using
an OpenAI-compatible LLM API, prompt engineering, streaming, conversation
memory, and basic scope filtering.

## Live Links
- Live application: Add after deployment.
- GitHub repository: Add your repository URL.
- Demo video: Add your 60-90 second recording.
- LinkedIn update: Add your post URL.

## Bot Specification

| Field | Specification |
|---|---|
| Bot name | Cognetix Electronics Support |
| Business | Fictional electronics store |
| Target users | Store customers |
| Main tasks | Shipping, returns, refunds, warranty and payment FAQs |
| LLM interface | OpenAI-compatible Chat Completions API |
| Temperature | 0.2 |
| Maximum output tokens | 600 |
| Streaming | Enabled |
| Conversation memory | Last 10 messages |
| Scope guard | Rule-based keyword and pattern checks |
| Fallback | Fixed sentence for out-of-scope questions |
| Interface | Streamlit |
| Evaluation | 20 questions: 10 in-scope, 5 out-of-scope, 5 injection |
| Limitations | No live order, payment, tracking or account access |

## Architecture
- `app.py`: Streamlit chat interface and session memory.
- `src/llm.py`: API client, streaming, and error handling.
- `src/prompts.py`: System prompt and approved policy loading.
- `src/guard.py`: Basic scope filtering.
- `data/policy.txt`: Fictional business policy.
- `eval/test_questions.csv`: Test dataset.
- `eval/results.csv`: Actual evaluation results.
- `docs/`: Architecture diagrams, screenshots, and demo notes.

## Setup
1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies using `python -m pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`.
5. Add your API key and supported model configuration to `.env`.
6. Run `streamlit run app.py`.

Never commit `.env` or expose API keys.

## How It Works
1. The customer submits a question.
2. The scope guard checks for relevant customer-support terms.
3. Out-of-scope questions receive the fixed fallback response.
4. In-scope questions are sent with the system prompt and recent history.
5. The LLM streams a response into the Streamlit interface.
6. Conversation memory is limited to the last ten messages.

## Evaluation Results
Test the 20 questions in `eval/test_questions.csv`.
Record actual responses and pass/fail decisions in `eval/results.csv`.
Report measured scope accuracy, policy correctness, injection resistance,
and any observed errors. Do not claim results that have not been measured.

## Limitations
- Scope filtering uses simple keywords and regular expressions.
- Prompt instructions alone cannot guarantee injection resistance.
- The application has no live store integrations.
- Model responses can still be incorrect or incomplete.
- API availability, cost, and rate limits depend on the provider.

## Author
- Name: Your Name
- Program: Cognetix GenAI Developer Internship
- GitHub: Add your profile link
- LinkedIn: Add your profile link
