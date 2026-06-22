#!/usr/bin/env python3
"""
Fetch YouTube transcripts for SEO experts and save them as Markdown files.

Selected videos (most relevant recent talks on AI-powered SEO content production):
  - Koray Tugberk Gubur: Master Semantic SEO & AI Agents (Feb 2026)
  - Lily Ray: GEO, AEO, LLMO — Separating Fact from Fiction (Nov 2025)
  - Ruben Hassid: How to Use AI to Grow on LinkedIn FAST (Jan 2025)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

OUTPUT_DIR = Path(__file__).parent / "research" / "youtube-transcripts"


@dataclass(frozen=True)
class ExpertVideo:
    slug: str
    expert: str
    title: str
    video_id: str
    published: str

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"


VIDEOS: list[ExpertVideo] = [
    ExpertVideo(
        slug="koray-tugberk-gubur",
        expert="Koray Tugberk Gubur",
        title="Master Semantic SEO & AI Agents with Koray Tugberk",
        video_id="mSHq_HxOyTA",
        published="2026-02-05",
    ),
    ExpertVideo(
        slug="lily-ray",
        expert="Lily Ray",
        title=(
            "GEO, AEO, LLMO: Separating Fact from Fiction & How to Win in AI Search "
            "- Lily Ray at MozCon 2025"
        ),
        video_id="2nJkT8zOzcM",
        published="2025-11-10",
    ),
    ExpertVideo(
        slug="ruben-hassid",
        expert="Ruben Hassid",
        title="How to Use AI to Grow on LinkedIn FAST (Algorithm Update)",
        video_id="9nvAEj5PaAI",
        published="2025-01-31",
    ),
]


def fetch_transcript_text(video_id: str) -> str:
    """Return the full transcript as plain text."""
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(video_id, languages=["en"])
    except NoTranscriptFound:
        fetched = api.fetch(video_id)
    return " ".join(snippet.text.strip() for snippet in fetched if snippet.text.strip())


def build_markdown(video: ExpertVideo, transcript: str) -> str:
    return (
        f"# {video.expert}\n\n"
        f"**Title:** {video.title}  \n"
        f"**URL:** {video.url}  \n"
        f"**Date:** {video.published}\n\n"
        f"---\n\n"
        f"## Transcript\n\n"
        f"{transcript}\n"
    )


def save_transcript(video: ExpertVideo) -> Path:
    print(f"Fetching transcript for {video.expert}...")
    transcript = fetch_transcript_text(video.video_id)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{video.slug}.md"
    output_path.write_text(build_markdown(video, transcript), encoding="utf-8")
    print(f"  Saved {len(transcript):,} characters -> {output_path}")
    return output_path


def main() -> int:
    errors: list[str] = []
    saved: list[Path] = []

    for video in VIDEOS:
        try:
            saved.append(save_transcript(video))
        except (TranscriptsDisabled, NoTranscriptFound) as exc:
            errors.append(f"{video.expert}: no transcript available ({exc})")
        except VideoUnavailable as exc:
            errors.append(f"{video.expert}: video unavailable ({exc})")
        except Exception as exc:
            errors.append(f"{video.expert}: {exc}")

    print()
    if saved:
        print(f"Successfully saved {len(saved)} transcript(s) to {OUTPUT_DIR}/")
    if errors:
        print("Errors:", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
