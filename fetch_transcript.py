from youtube_transcript_api import YouTubeTranscriptApi
import os

videos = [
    {
        "video_id": "5DxwBti6yQY",
        "video_url": "https://www.youtube.com/watch?v=5DxwBti6yQY",
        "expert_name": "Ross Simmonds",
        "video_title": "All In on Claude: Travis Tallent on Building AI Systems That Actually Scale",
        "video_date": "2026",
        "file_name": "ross-simmonds.md"
    }
]

output_dir = "research/youtube-transcripts"
os.makedirs(output_dir, exist_ok=True)

ytt_api = YouTubeTranscriptApi()

for video in videos:
    try:
        transcript = ytt_api.fetch(video["video_id"], languages=["en-US", "en"])
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