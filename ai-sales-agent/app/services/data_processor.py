class DataProcessor:
    def process(self, payload: dict) -> dict:
        """
        Minimal cleaning + normalization. Keep it deterministic and lightweight.
        """
        if not isinstance(payload, dict):
            return {"processed": True, "payload": payload}

        url = payload.get("url") or payload.get("company_url")
        title = payload.get("title") or None
        description = payload.get("description") or None
        markdown = payload.get("markdown") or ""

        if isinstance(markdown, str):
            markdown = markdown.strip()

        def _norm_text(v):
            if v is None:
                return None
            if not isinstance(v, str):
                return str(v)
            v = " ".join(v.split())
            return v if v else None

        normalized = {
            "url": _norm_text(url),
            "name": _norm_text(title),
            "description": _norm_text(description),
            "content_markdown": markdown,
            "source": payload.get("source") or "unknown",
        }

        return {"processed": True, "normalized": normalized}

