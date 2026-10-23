
"""OpenAI-compatible LLM client with streaming and error handling."""

import os
from collections.abc import Iterator

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

load_dotenv()

TEMPERATURE = 0.2


def create_client() -> tuple[OpenAI, str, int]:
    """Create the LLM client and load its configuration."""
    api_key = os.getenv("LLM_API_KEY", "").strip()
    model_name = os.getenv("MODEL_NAME", "").strip()
    base_url = os.getenv("LLM_BASE_URL", "").strip()
    max_tokens = int(os.getenv("MAX_TOKENS", "600"))

    if not api_key or api_key == "your_api_key_here":
        raise ValueError("Configure LLM_API_KEY in your local .env file.")

    if not model_name or model_name == "your_model_name":
        raise ValueError("Configure MODEL_NAME in your local .env file.")

    if max_tokens < 1:
        raise ValueError("MAX_TOKENS must be a positive integer.")

    client_options = {"api_key": api_key}

    if base_url:
        client_options["base_url"] = base_url

    client = OpenAI(
        **client_options,
        timeout=45.0,
        max_retries=2,
    )

    return client, model_name, max_tokens


def stream_response(
    messages: list[dict[str, str]],
) -> Iterator[str]:
    """
    Stream response text from the configured model.

    Friendly errors are yielded to the UI without exposing credentials.
    """
    try:
        client, model_name, max_tokens = create_client()

        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=max_tokens,
            stream=True,
        )

        for chunk in stream:
            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content

            if content:
                yield content

    except AuthenticationError:
        yield "Authentication failed. Check your LLM API key."

    except RateLimitError:
        yield "The AI service rate limit or quota was reached. Please try again later."

    except APITimeoutError:
        yield "The AI service timed out. Please try again."

    except APIConnectionError:
        yield "Could not connect to the AI service. Check your connection and API configuration."

    except APIStatusError as exc:
        # Log only the status code, never credentials or request headers.
        print(f"LLM API error: HTTP {exc.status_code}")
        yield "The AI service returned an error. Please try again later."

    except (ValueError, TypeError) as exc:
        # Configuration messages are intentionally kept separate from secrets.
        yield f"Configuration error: {exc}"

    except Exception:
        # Avoid exposing arbitrary exception details in the public UI.
        yield "An unexpected error occurred. Please try again later."
