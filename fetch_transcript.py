from youtube_transcript_api import YouTubeTranscriptApi
import os

videos = [
    {
        "video_id": "fKJ18NSHzCE",
        "video_url": "https://www.youtube.com/watch?v=fKJ18NSHzCE",
        "expert_name": "Mike King",
        "video_title": "Ranking in Google's AI Results in 2026 with Mike King",
        "video_date": "January 2026",
        "file_name": "mike-king.md"
    },
    {
        "video_id": "2htSIT0HLjs",
        "video_url": "https://www.youtube.com/watch?v=2htSIT0HLjs",
        "expert_name": "Lily Ray",
        "video_title": "The Future of SEO: Lily Ray on Google Updates, AI Search & GEO Spam",
        "video_date": "March 2026",
        "file_name": "lily-ray.md"
    },
    {
        "video_id": "vhZS8trALwQ",
        "video_url": "https://www.youtube.com/watch?v=vhZS8trALwQ",
        "expert_name": "Mike King",
        "video_title": "Decoding the Future of SEO with Mike King",
        "video_date": "June 2025",
        "file_name": "mike-king-2.md"
    }
]

output_dir = "research/youtube-transcripts"
os.makedirs(output_dir, exist_ok=True)

ytt_api = YouTubeTranscriptApi()

for video in videos:
    try:
        transcript = ytt_api.fetch(video["video_id"])
        full_text = " ".join([entry.text for entry in transcript])
        output_path = os.path.join(output_dir, video["file_name"])
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {video['expert_name']} — YouTube Transcript\n\n")
            f.write(f"**Video Title:** {video['video_title']}\n\n")
            f.write(f"**URL:** {video['video_url']}\n\n")
            f.write(f"**Date:** {video['video_date']}\n\n")
            f.write("---\n\n")
            f.write(full_text)
        print(f"✅ Saved: {video['file_name']}")
    except Exception as e:
        print(f"❌ Failed for {video['expert_name']}: {e}")