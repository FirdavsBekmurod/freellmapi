---
name: whisper-transcribe
description: Use to transcribe speech from audio or video files to text, subtitles (.srt/.vtt) or JSON with OpenAI Whisper, to translate speech to English, or to detect the spoken language. Triggers on requests like "транскрибируй", "расшифруй аудио", "сделай субтитры", "transcribe this recording", "speech to text".
---

# Whisper transcription

Runs OpenAI Whisper locally through `scripts/transcribe.py`. No API key is needed; models are downloaded on first use.

## Setup (once per machine)

```bash
pip install -U openai-whisper   # also pulls PyTorch, which is large
ffmpeg -version                 # ffmpeg must be on PATH (apt install ffmpeg / brew install ffmpeg)
```

If `import whisper` fails, install it as above before doing anything else. Without a GPU Whisper runs on CPU and is slow on long files, so pick a smaller model.

## Usage

```bash
python scripts/transcribe.py INPUT [--model base] [--language ru] [--task transcribe] [--format txt] [--out-dir DIR]
```

- `INPUT`: any audio or video ffmpeg can read (mp3, wav, m4a, mp4, mkv, ogg...).
- `--model`: `tiny`, `base` (default), `small`, `medium`, `large-v3`, `turbo`. Larger is more accurate and slower.
- `--language`: code such as `ru`, `en`, `uz`. Omit to auto-detect. Set it when you know it; auto-detect can guess wrong on short or noisy clips.
- `--task translate`: outputs English text regardless of the spoken language.
- `--format`: `txt` (default), `srt`, `vtt`, `json`, or `all`. Files are written as `<input-stem>.<format>` in `--out-dir` (default: next to the input). The plain text is also printed to stdout.

## Choosing a model

| Situation | Model |
| --- | --- |
| Quick draft, clear English | `tiny` / `base` |
| Everyday use, good balance | `small` |
| Accuracy matters, non-English, accents, noise | `medium` / `large-v3` (needs a lot of RAM, ideally a GPU) |
| Fast and accurate on GPU | `turbo` |

English-only `.en` variants (`base.en`, `small.en`) are slightly better for English only.

## Workflow

1. Confirm the input file exists and note its language if the user mentioned it.
2. Pick a model from the table. For files longer than ~10 minutes on CPU, warn the user about the time and start with `small` or smaller.
3. Run the script. Use `--format srt` when the user wants subtitles, `--format all` if unsure.
4. Report where the output files were written and show the transcript, or a short excerpt if it is long.
5. Do not claim the transcript is perfect; Whisper can hallucinate on silence and mishear names. Offer to re-run with a larger model or an explicit `--language`.

## Troubleshooting

- `ffmpeg not found`: install ffmpeg, then retry.
- Model download fails: it needs network access to download weights (75 MB for `tiny` up to about 3 GB for `large`). Check the network or use a smaller model.
- Out of memory: use a smaller model.
- Wrong language or gibberish: pass `--language` explicitly.
- Using it with Remotion captions: produce `--format srt` (or `json`), then follow the `remotion-captions` skill to import it.
