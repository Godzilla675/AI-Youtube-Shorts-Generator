# AI Youtube Shorts Generator
FIXED VERSION
AI Youtube Shorts Generator is a Python tool designed to generate engaging YouTube shorts from long-form videos. By leveraging the power of GPT-4, Gemini 2.5 Flash with thinking mode, and Whisper, it extracts the most interesting highlights, detects speakers, and crops the content vertically for shorts. This tool supports multiple AI models and two analysis modes for maximum flexibility.

If you wish to add shorts generation into your application, here is an api to create shorts from long form videos :- https://docs.vadoo.tv/docs/guide/create-ai-clips

![longshorts](https://github.com/user-attachments/assets/3f5d1abf-bf3b-475f-8abf-5e253003453a)

## Features

- **Video Download**: Given a YouTube URL, the tool downloads the video.
- **Dual Analysis Modes**:
  - **Transcript Mode**: Transcribes audio with Whisper, then analyzes with AI (supports GPT-4o and Gemini models)
  - **Vision Mode**: AI watches and hears the video directly using Gemini's multimodal capabilities (no transcription needed)
- **Multiple AI Models**: Choose from GPT-4o, Gemini 2.5 Flash (with thinking mode), Gemini 2.5 Pro (with thinking mode), Gemini 1.5 Flash, or Gemini 1.5 Pro
- **Highlight Extraction**: Automatically identifies the most engaging parts of the video for shorts.
- **Speaker Detection**: Detects speakers in the video.
- **Vertical Cropping**: Crops the highlighted sections vertically, making them perfect for shorts.

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg
- OpenCV

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator.git
   cd AI-Youtube-Shorts-Generator
   ```

2. Create a virtual environment

```bash
python3.10 -m venv venv
```

3. Activate a virtual environment:

```bash
source venv/bin/activate # On Windows: venv\Scripts\activate
```

4. Install the python dependencies:

```bash
pip install -r requirements.txt
```
---

1. Set up the environment variables.

Create a `.env` file in the project root directory and add your API keys:

```bash
# For GPT-4o (Transcript Mode)
OPENAI_API=your_openai_api_key_here

# For Gemini models (both modes)
GEMINI_API=your_gemini_api_key_here
```

**Getting API Keys:**
- OpenAI API: https://platform.openai.com/api-keys (requires payment)
- Gemini API: https://makersuite.google.com/app/apikey (free tier available)

**Note:** You only need the API key for the models you plan to use. If you only want to use Gemini models, you don't need an OpenAI API key.

## Usage

1. Ensure your `.env` file is correctly set up with your API keys.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Choose your analysis mode:
   - **Mode 1 (Transcript Mode)**: Traditional approach - transcribes audio first, then AI analyzes the transcript
     - Supports: GPT-4o, Gemini 2.5 Flash (thinking mode), Gemini 2.5 Pro (thinking mode), Gemini 1.5 Flash, Gemini 1.5 Pro
   - **Mode 2 (Vision Mode)**: Advanced approach - Gemini watches and hears the video directly
     - Supports: Gemini 2.5 Flash (thinking mode), Gemini 2.5 Pro (thinking mode), Gemini 1.5 Flash, Gemini 1.5 Pro (GPT models can't analyze videos)
4. Select your preferred AI model from the available options
5. Enter the YouTube URL when prompted
6. The tool will generate a vertical short saved as `Final.mp4`

### Which Mode Should You Use?

- **Transcript Mode**: Faster, cheaper, good for videos with clear speech
- **Vision Mode**: More accurate for visual content, understands context from both audio and video, better for videos where visuals are important

### Model Comparison

**Transcript Mode Models:**
- **GPT-4o**: Most capable OpenAI model, best for complex content, requires OpenAI API (paid)
- **Gemini 2.5 Flash**: Latest with thinking mode, fastest, excellent balance of speed and quality (Recommended), free tier available
- **Gemini 2.5 Pro**: Most capable with thinking mode, best for complex analysis, free tier available
- **Gemini 1.5 Flash**: Fast and efficient, good for most use cases, free tier available
- **Gemini 1.5 Pro**: Capable and reliable, good for detailed analysis, free tier available

**Vision Mode Models (Gemini only):**
- **Gemini 2.5 Flash**: Latest with thinking mode - Recommended for most users, fastest with best quality
- **Gemini 2.5 Pro**: Most capable with thinking mode - Best for complex video understanding
- **Gemini 1.5 Flash**: Good for basic video analysis, fast and efficient
- **Gemini 1.5 Pro**: Good for detailed video understanding, reliable and capable

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

This is a v0.1 release and might have some bugs. Please report any issues on the [GitHub Repository](https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator).

### Other useful Video AI Projects

[AI Influencer generator](https://github.com/SamurAIGPT/AI-Influencer-Generator)

[Text to Video AI](https://github.com/SamurAIGPT/Text-To-Video-AI)

[Faceless Video Generator](https://github.com/SamurAIGPT/Faceless-Video-Generator)

[AI B-roll generator](https://github.com/Anil-matcha/AI-B-roll)

[No-code AI Youtube Shorts Generator](https://www.vadoo.tv/clip-youtube-video)

[Sora AI Video Generator](https://www.vadoo.tv/sora-ai-video-generator)
