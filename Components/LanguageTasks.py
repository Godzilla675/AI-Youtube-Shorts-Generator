from pydantic import BaseModel,Field
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API")
gemini_api_key = os.getenv("GEMINI_API")

class JSONResponse(BaseModel):
    """
    The response should strictly follow the following structure: -
     [
        {
        start: "Start time of the clip",
        content: "Highlight Text",
        end: "End Time for the highlighted clip"
        }
     ]
    """
    start: float = Field(description="Start time of the clip")
    content: str= Field(description="Highlight Text")
    end: float = Field(description="End time for the highlighted clip")

system = """

Based on the Transcription user provides with start and end, Highilight the main parts in less then 1 min which can be directly converted into a short. highlight it such that its intresting and also keep the time staps for the clip to start and end. only select a continues Part of the video

Follow this Format and return in valid json 
[{{
start: "Start time of the clip",
content: "Highlight Text",
end: "End Time for the highlighted clip"
}}]
it should be one continues clip as it will then be cut from the video and uploaded as a tiktok video. so only have one start, end and content
Make sure that the content's length doesn't go beyond 60 seconds.

Dont say anything else, just return Proper Json. no explanation etc


IF YOU DONT HAVE ONE start AND end WHICH IS FOR THE LENGTH OF THE ENTIRE HIGHLIGHT, THEN 10 KITTENS WILL DIE, I WILL DO JSON['start'] AND IF IT DOESNT WORK THEN...

<TRANSCRIPTION>
{Transcription}

"""

# User = """
# Example
# """




def GetHighlight(Transcription, model="gemini-2.5-flash-002"):
    """
    Get highlight from transcription using various AI models.
    
    Args:
        Transcription: The video transcript text
        model: Model to use - "gpt-4o", "gemini-2.5-flash-002", "gemini-2.5-pro-002", "gemini-1.5-flash", "gemini-1.5-pro"
    
    Returns:
        Tuple of (start_time, end_time)
    """
    from langchain.prompts import ChatPromptTemplate
    
    # Determine which LLM to use based on model parameter
    if model.startswith("gemini"):
        if not gemini_api_key:
            raise ValueError("GEMINI_API key not found. Make sure it is defined in the .env file.")
        
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Configure with thinking mode for 2.5 models
        model_kwargs = {}
        if "2.5" in model or "2-5" in model:
            print("Using Gemini 2.5 with thinking mode enabled...")
            model_kwargs = {
                "max_output_tokens": 8192,
                "thinking": True
            }
        
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.7,
            google_api_key=gemini_api_key,
            **model_kwargs
        )
    else:  # OpenAI models (gpt-4o, gpt-4, etc.)
        if not openai_api_key:
            raise ValueError("OPENAI_API key not found. Make sure it is defined in the .env file.")
        
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model=model,
            temperature=0.7,
            api_key=openai_api_key
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("user", Transcription)
        ]
    )
    
    chain = prompt | llm.with_structured_output(JSONResponse, method="function_calling")
    response = chain.invoke({"Transcription": Transcription})
    Start, End = int(response.start), int(response.end)
    
    if Start == End:
        Ask = input("Error - Get Highlights again (y/n) -> ").lower()
        if Ask == "y":
            Start, End = GetHighlight(Transcription, model)
        return Start, End
    
    return Start, End

if __name__ == "__main__":
    print(GetHighlight(User))
