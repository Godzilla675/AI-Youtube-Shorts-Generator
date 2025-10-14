from Components.YoutubeDownloader import download_youtube_video
from Components.Edit import extractAudio, crop_video
from Components.Transcription import transcribeAudio
from Components.LanguageTasks import GetHighlight
from Components.GeminiVision import GetHighlightFromVideo
from Components.FaceCrop import crop_to_vertical, combine_videos

def print_menu():
    print("\n" + "="*60)
    print("AI YouTube Shorts Generator")
    print("="*60)
    print("\nSelect Analysis Mode:")
    print("1. Transcript Mode (Original) - Transcribe audio, then analyze with AI")
    print("2. Vision Mode - AI watches and hears the video directly (Gemini only)")
    print("="*60)

def select_transcript_model():
    print("\nSelect AI Model for Transcript Analysis:")
    print("1. GPT-4o (OpenAI) - Default")
    print("2. Gemini 2.0 Flash Experimental (Google)")
    print("3. Gemini 1.5 Flash (Google)")
    print("4. Gemini 1.5 Pro (Google)")
    
    choice = input("\nEnter choice (1-4, default=1): ").strip() or "1"
    
    models = {
        "1": "gpt-4o",
        "2": "gemini-2.0-flash-exp",
        "3": "gemini-1.5-flash",
        "4": "gemini-1.5-pro"
    }
    
    return models.get(choice, "gpt-4o")

def select_vision_model():
    print("\nSelect Gemini Model for Vision Analysis:")
    print("1. Gemini 2.0 Flash Experimental - Latest and fastest")
    print("2. Gemini 1.5 Flash - Fast and efficient")
    print("3. Gemini 1.5 Pro - Most capable")
    
    choice = input("\nEnter choice (1-3, default=1): ").strip() or "1"
    
    models = {
        "1": "gemini-2.0-flash-exp",
        "2": "gemini-1.5-flash",
        "3": "gemini-1.5-pro"
    }
    
    return models.get(choice, "gemini-2.0-flash-exp")

def main():
    print_menu()
    
    mode = input("\nEnter mode (1 or 2, default=1): ").strip() or "1"
    
    url = input("\nEnter YouTube video URL: ")
    Vid = download_youtube_video(url)
    
    if not Vid:
        print("Unable to Download the video")
        return
    
    Vid = Vid.replace(".webm", ".mp4")
    print(f"Downloaded video and audio files successfully! at {Vid}")
    
    start = None
    stop = None
    
    if mode == "2":
        # Vision Mode - Gemini watches the video directly
        print("\n--- Vision Mode: AI will watch and analyze the video directly ---")
        model = select_vision_model()
        
        try:
            start, stop = GetHighlightFromVideo(Vid, model)
        except Exception as e:
            print(f"Error in vision mode: {e}")
            return
    
    else:
        # Transcript Mode - Traditional approach
        print("\n--- Transcript Mode: Transcribing audio first ---")
        model = select_transcript_model()
        
        Audio = extractAudio(Vid)
        if not Audio:
            print("No audio file found")
            return
        
        transcriptions = transcribeAudio(Audio)
        if len(transcriptions) == 0:
            print("No transcriptions found")
            return
        
        TransText = ""
        for text, time_start, time_end in transcriptions:
            TransText += (f"{time_start} - {time_end}: {text}")
        
        try:
            start, stop = GetHighlight(TransText, model)
        except Exception as e:
            print(f"Error in transcript mode: {e}")
            return
    
    # Process the highlight
    if start is not None and stop is not None and start >= 0 and stop > 0 and stop > start:
        print(f"\n✓ Highlight identified: {start}s - {stop}s (duration: {stop-start}s)")
        
        Output = "Out.mp4"
        print("\nCropping video to highlight...")
        crop_video(Vid, Output, start, stop)
        
        croped = "croped.mp4"
        print("Creating vertical format...")
        crop_to_vertical("Out.mp4", croped)
        
        print("Combining videos...")
        combine_videos("Out.mp4", croped, "Final.mp4")
        
        print("\n" + "="*60)
        print("✓ SUCCESS! Your short has been created: Final.mp4")
        print("="*60)
    else:
        print("Error in getting highlight")

if __name__ == "__main__":
    main()