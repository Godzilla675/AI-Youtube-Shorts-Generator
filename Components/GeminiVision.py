import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API")

if not gemini_api_key:
    raise ValueError("GEMINI_API key not found. Make sure it is defined in the .env file.")

genai.configure(api_key=gemini_api_key)

class VideoHighlight(BaseModel):
    """
    The response should strictly follow the following structure: -
     {
        start: "Start time of the clip",
        content: "Highlight Text",
        end: "End Time for the highlighted clip"
     }
    """
    start: float = Field(description="Start time of the clip in seconds")
    content: str = Field(description="Highlight Text describing the interesting part")
    end: float = Field(description="End time for the highlighted clip in seconds")

def GetHighlightFromVideo(video_path, model_name="gemini-2.5-flash-002"):
    """
    Analyze video directly using Gemini's vision capabilities to find highlights.
    
    Args:
        video_path: Path to the video file
        model_name: Gemini model to use (gemini-2.5-flash-002, gemini-2.5-pro-002, gemini-1.5-flash, or gemini-1.5-pro)
    
    Returns:
        Tuple of (start_time, end_time) for the highlight
    """
    video_file = None
    try:
        print(f"Uploading video for analysis with {model_name}...")
        
        # Upload the video file
        video_file = genai.upload_file(path=video_path)
        
        # Wait for the file to be processed
        print("Processing video...")
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = genai.get_file(video_file.name)
        
        if video_file.state.name == "FAILED":
            raise ValueError("Video processing failed")
        
        print("Video processed successfully. Analyzing content with thinking mode enabled...")
        
        # Configure generation with thinking mode and max tokens
        generation_config = genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=8192,
            response_mime_type="application/json",
        )
        
        # Create the model with thinking mode enabled for 2.5 models
        if "2.5" in model_name or "2-5" in model_name:
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                system_instruction="You are an expert video analyst specializing in identifying engaging content for short-form videos. Think deeply about the visual and audio elements before providing your analysis."
            )
        else:
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
        
        # Create the prompt for highlight extraction
        prompt = """
        Watch this video carefully and identify the most engaging and interesting part that would make a great YouTube Short (under 60 seconds).
        
        Consider:
        - Dramatic moments or key points
        - Engaging dialogue or explanations
        - Visual interest
        - Self-contained segments that make sense on their own
        
        You MUST provide your response in this exact JSON format:
        {
            "start": <start_time_in_seconds>,
            "content": "<brief description of why this segment is interesting>",
            "end": <end_time_in_seconds>
        }
        
        Requirements:
        - The segment MUST be continuous (one start and one end time)
        - Duration must be less than 60 seconds
        - Times must be in seconds as numbers (not strings)
        - The segment should be self-contained and engaging
        
        Return ONLY the JSON, no other text.
        """
        
        # Generate content with thinking mode
        response = model.generate_content([video_file, prompt])
        
        # Parse the response
        import json
        import re
        
        response_text = response.text.strip()
        
        # Try to extract JSON from response
        json_match = re.search(r'\{[^}]+\}', response_text)
        if json_match:
            json_str = json_match.group(0)
            result = json.loads(json_str)
            
            start = float(result.get("start", 0))
            end = float(result.get("end", 0))
            content = result.get("content", "")
            
            print(f"\nHighlight found: {content}")
            print(f"Time range: {start}s - {end}s ({end-start}s duration)")
            
            # Validate the times
            if start >= end:
                print("Error: Invalid time range (start >= end)")
                raise ValueError("Invalid time range")
            
            if (end - start) > 60:
                print("Warning: Segment is longer than 60 seconds, truncating...")
                end = start + 60
            
            return int(start), int(end)
        else:
            raise ValueError("Could not parse JSON response from Gemini")
            
    except Exception as e:
        print(f"Error in GetHighlightFromVideo: {e}")
        print(f"Response was: {response.text if 'response' in locals() else 'No response'}")
        
        # Fallback: ask user if they want to try again
        Ask = input("Error - Try again? (y/n) -> ").lower()
        if Ask == "y":
            return GetHighlightFromVideo(video_path, model_name)
        
        raise e
    
    finally:
        # Always clean up the uploaded file
        if video_file:
            try:
                genai.delete_file(video_file.name)
                print("Cleaned up uploaded video file")
            except:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    # Test the function
    test_video = input("Enter path to test video: ")
    model = input("Enter model (gemini-2.5-flash-002/gemini-2.5-pro-002/gemini-1.5-flash/gemini-1.5-pro): ") or "gemini-2.5-flash-002"
    
    start, end = GetHighlightFromVideo(test_video, model)
    print(f"\nFinal result: Start={start}, End={end}")
