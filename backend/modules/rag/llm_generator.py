# app/modules/rag/llm_generator.py
import ollama
import json
import sys
import codecs  # dùng để decode unicode-escape an toàn
from backend.core.config import settings
from backend.utils.logger import log

import ollama
import json
import sys
import codecs
from backend.core.config import settings
from backend.utils.logger import log

def generate_stream(prompt: str, max_tokens: int = 2000):
    try:
        log(f"Calling Ollama: {settings.OLLAMA_MODEL}, prompt length: {len(prompt)}")

        stream = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.7,
                "num_predict": max_tokens,
            },
            stream=True
        )

        full_summary = ''
        buffer = ''

        for chunk in stream:
            content = chunk.get("message", {}).get("content", "")
            if content:
                full_summary += content
                buffer += content

                if len(buffer) >= 100 or buffer.strip().endswith(('.', '!', '?', '\n')):
                    sys.stdout.write(json.dumps({"type": "chunk", "content": buffer}) + "\n")
                    sys.stdout.flush()
                    buffer = ''

        if buffer:
            sys.stdout.write(json.dumps({"type": "chunk", "content": buffer}) + "\n")
            sys.stdout.flush()
        decoded = codecs.decode(full_summary, 'unicode-escape', errors='replace')

        decoded = decoded.encode('latin1', errors='ignore').decode('utf-8', errors='replace')

        sys.stdout.write(json.dumps({"type": "complete", "summary": decoded.strip()}) + "\n")
        sys.stdout.flush()

        log(f"Streaming hoàn tất, độ dài decoded: {len(decoded)} chars")
        return decoded

    except Exception as e:
        log(f"Ollama error: {str(e)}")
        sys.stdout.write(json.dumps({"type": "error", "error": str(e)}) + "\n")
        sys.stdout.flush()
        return None