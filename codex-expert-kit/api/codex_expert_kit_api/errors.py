from __future__ import annotations

from fastapi.responses import JSONResponse


def error_response(error_code: str, message: str, status_code: int, details: dict | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "ok": False,
            "error": {
                "error_code": error_code,
                "code": error_code,
                "message": message,
                "details": details or {},
                "retryable": False,
                "request_id": "local_contract_test"
            }
        },
    )


def ok_response(data: dict, source: str = "knowledge_items_index") -> dict:
    return {
        "ok": True,
        "data": data,
        "meta": {
            "request_id": "local_contract_test",
            "served_at": "2026-06-08T00:00:00+08:00",
            "data_version": "local",
            "source": source,
        },
    }
