import argparse
import json
from pathlib import Path

import httpx
from dotenv import load_dotenv


def call_agent(query: str, session_id: str, base_url: str) -> dict:
    response = httpx.post(
        f"{base_url.rstrip('/')}/agent/query",
        json={"query": query, "session_id": session_id},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Call the /agent/query endpoint")
    parser.add_argument("query", nargs="?", default="현재 테스트 상태를 요약해줘")
    parser.add_argument("--session-id", default="test-001")
    parser.add_argument("--base-url", default="http://localhost:8000")
    args = parser.parse_args()

    result = call_agent(args.query, args.session_id, args.base_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()