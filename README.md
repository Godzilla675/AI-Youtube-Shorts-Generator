# AI Youtube Shorts Generator
FIXED VERSION
AI Youtube Shorts Generator is a Python tool designed to generate engaging YouTube shorts from long-form videos. By leveraging the power of GPT-4, Gemini 2.0 Flash, and Whisper, it extracts the most interesting highlights, detects speakers, and crops the content vertically for shorts. This tool supports multiple AI models and two analysis modes for maximum flexibility.

If you wish to add shorts generation into your application, here is an api to create shorts from long form videos :- https://docs.vadoo.tv/docs/guide/create-ai-clips

![longshorts](https://github.com/user-attachments/assets/3f5d1abf-bf3b-475f-8abf-5e253003453a)

## Features

- **Video Download**: Given a YouTube URL, the tool downloads the video.
- **Dual Analysis Modes**:
  - **Transcript Mode**: Transcribes audio with Whisper, then analyzes with AI (supports GPT-4o and Gemini models)
  - **Vision Mode**: AI watches and hears the video directly using Gemini's multimodal capabilities (no transcription needed)
- **Multiple AI Models**: Choose from GPT-4o, Gemini 2.0 Flash, Gemini 1.5 Flash, or Gemini 1.5 Pro
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

You can get a Gemini API key for free at: https://makersuite.google.com/app/apikey

## Usage

1. Ensure your `.env` file is correctly set up with your API keys.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Choose your analysis mode:
   - **Mode 1 (Transcript Mode)**: Traditional approach - transcribes audio first, then AI analyzes the transcript
     - Supports: GPT-4o, Gemini 2.0 Flash, Gemini 1.5 Flash, Gemini 1.5 Pro
   - **Mode 2 (Vision Mode)**: Advanced approach - Gemini watches and hears the video directly
     - Supports: Gemini 2.0 Flash, Gemini 1.5 Flash, Gemini 1.5 Pro (GPT models can't analyze videos)
4. Select your preferred AI model from the available options
5. Enter the YouTube URL when prompted
6. The tool will generate a vertical short saved as `Final.mp4`

### Which Mode Should You Use?

- **Transcript Mode**: Faster, cheaper, good for videos with clear speech
- **Vision Mode**: More accurate for visual content, understands context from both audio and video, better for videos where visuals are important

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
