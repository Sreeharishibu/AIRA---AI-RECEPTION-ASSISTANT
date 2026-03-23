# AIRA — Copilot instructions for AI coding agents

Purpose
- Help AI agents become productive quickly in this Django app (AIRA).

Quick architecture summary
- Project type: Django 4.x monolith. Root Django project: `aira_admin` and app: `aira_app`.
- Key responsibilities:
  - `aira_app/models.py`: data models (`ChatbotQuery`, `DetailImage`, `InventoryItem`).
  - `aira_app/views.py`: majority of application logic (authentication, query matching, TTS, analytics, file uploads).
  - `aira_app/stt_utils.py`: STT integration (Vosk + ffmpeg). See STT flow and conversion.
  - `aira_admin/settings.py`: configuration (MEDIA_ROOT, VOSK_MODEL_PATH, STT_UPLOAD_DIR).

Where to start (local dev)
- Ensure system deps: `ffmpeg` available in PATH and a Vosk model downloaded.
- Python deps: at minimum install `Django`, `vosk`, `gTTS`, `openpyxl` (no requirements.txt provided).
- Run migrations and dev server:
  - `python manage.py migrate`
  - `python manage.py runserver`

Project-specific conventions & gotchas
- Simple session-based auth: `views.login_view` sets `request.session['is_logged_in']` (hard-coded credentials in `views.py`). Do not assume Django auth middleware for UI flows.
- STT pipeline: audio → saved to `settings.STT_UPLOAD_DIR` → `ffmpeg` converts to 16k mono WAV → Vosk model used in `aira_app/stt_utils.py:transcribe_audio()`.
  - Endpoint: `POST /stt/` (see `aira_app/urls.py`). Expects form file field named `audio` and is decorated with `@csrf_exempt`.
- Vosk model path is configured in `aira_admin/settings.py` as `VOSK_MODEL_PATH`. The repo contains a `Vosk models/` folder; update `VOSK_MODEL_PATH` to point there or set an absolute path in settings or env.
- TTS: `gTTS` output saved under `media/tts/` via `generate_tts_audio()` in `views.py`.
- Logging: user interactions are appended to `aira_query_log.xlsx` at `BASE_DIR` using `openpyxl` (see `log_interaction_to_excel()` and `load_logs_from_excel()` in `views.py`). Keep the workbook schema in sync (Timestamp, User Query, Matched Query, AIRA Answer).
- Image uploads: `DetailImage.image` uses `detail_image_upload_path()` to place files under `media/announcements/` or `media/placements/`.
- Deletions: views call `img.image.delete(save=False)` before model deletion to remove files from storage.

Debugging and testing tips
- If STT fails, check:
  - `VOSK_MODEL_PATH` points to an existing model directory.
  - `ffmpeg` invocation in `stt_utils.convert_to_wav_16k_mono()` runs (no stdout/stderr shown). Run conversion manually to reproduce.
- To test TTS and media serving locally, ensure `DEBUG = True` in `settings.py` so `urlpatterns` serves `MEDIA_URL`.
- Excel logs: open `aira_query_log.xlsx` in LibreOffice/Excel to verify rows; code expects first row to be header.

Integration points & external deps
- System binaries: `ffmpeg` (required). Always check it's in PATH for the server environment.
- Python packages used in codebase (search imports for exact names): `django`, `vosk`, `gtts`, `openpyxl`, `openpyxl`.
- External models: Vosk model folders included in repo root (`Vosk models/*`). Settings currently reference an absolute `D:\...` path — update when deploying locally or in CI.

Files to reference when making changes
- Main settings: [aira_admin/settings.py](aira_admin/aira_admin/settings.py)
- STT logic: [aira_app/stt_utils.py](aira_admin/aira_app/stt_utils.py)
- App views and business logic: [aira_app/views.py](aira_admin/aira_app/views.py)
- Models: [aira_app/models.py](aira_admin/aira_app/models.py)
- URL routes: [aira_app/urls.py](aira_admin/aira_app/urls.py)

Non-goals / things NOT to change without confirmation
- Replacing session auth with Django auth without discussing UX requirements (login is intentionally simple here).
- Moving or renaming the `aira_query_log.xlsx` file or changing its header schema without updating `load_logs_from_excel()`.

If you edit configuration
- Prefer setting `VOSK_MODEL_PATH` via an environment variable or change `settings.py` to resolve the repo model path:
  ```py
  VOSK_MODEL_PATH = os.environ.get('VOSK_MODEL_PATH') or str(BASE_DIR / 'Vosk models' / 'vosk-model-small-en-in-0.4')
  ```

When in doubt
- Run the server, exercise the web UI flows (login → userhome → ask queries → TTS + Excel logging). Use `/stt/` with a small WAV to validate Vosk.

Feedback
- Tell me any missing infra details (CI, preferred Python version, or target deployment) and I will update this file.
