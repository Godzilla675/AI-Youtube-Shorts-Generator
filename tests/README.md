# AI YouTube Shorts Generator - Test Suite

This directory contains comprehensive tests for all functionalities of the AI YouTube Shorts Generator.

## Test Coverage

### Component Tests

1. **test_youtube_downloader.py**
   - Tests video download from YouTube
   - Tests video size calculation
   - Tests progressive and adaptive video streams
   - Tests video/audio merging
   - Tests error handling

2. **test_edit.py**
   - Tests audio extraction from video
   - Tests video cropping functionality
   - Tests various time ranges and edge cases
   - Tests error handling

3. **test_transcription.py**
   - Tests audio transcription with Whisper
   - Tests CUDA and CPU device selection
   - Tests multiple segments handling
   - Tests transcription parameters
   - Tests error handling

4. **test_language_tasks.py**
   - Tests highlight extraction from transcripts
   - Tests multiple AI models (GPT-4o, Gemini variants)
   - Tests thinking mode for Gemini 2.5 models
   - Tests API key validation
   - Tests error scenarios

5. **test_gemini_vision.py**
   - Tests video analysis with Gemini Vision
   - Tests video upload and processing
   - Tests highlight extraction from video
   - Tests various Gemini models
   - Tests time validation and truncation
   - Tests cleanup of uploaded files

6. **test_face_crop.py**
   - Tests vertical video cropping
   - Tests face detection and tracking
   - Tests video/audio combination
   - Tests edge cases (narrow videos, no video)
   - Tests multiple face handling

7. **test_speaker.py**
   - Tests voice activity detection
   - Tests audio extraction from video
   - Tests face and speaker detection
   - Tests frame tracking
   - Tests multiple face scenarios

8. **test_main.py**
   - Tests main application workflow
   - Tests menu system
   - Tests model selection (transcript and vision modes)
   - Tests both transcript and vision modes
   - Tests error handling at application level
   - Tests invalid input scenarios

## Running Tests

### Run All Tests

```bash
python tests/run_all_tests.py
```

or

```bash
python -m pytest tests/
```

### Run Specific Test Module

```bash
python tests/run_all_tests.py test_youtube_downloader
```

or

```bash
python -m unittest tests.test_youtube_downloader
```

### Run Specific Test Case

```bash
python -m unittest tests.test_youtube_downloader.TestYoutubeDownloader.test_get_video_size
```

## Test Design

All tests use **mocking** to avoid:
- Making actual API calls (OpenAI, Gemini)
- Downloading real YouTube videos
- Processing actual video/audio files
- Network dependencies

This ensures tests are:
- Fast
- Reliable
- Runnable offline
- Cost-free (no API costs)

## Dependencies

Tests require the following packages (already in requirements.txt):
- unittest (standard library)
- unittest.mock (standard library)

No additional test dependencies are needed.

## Test Results Interpretation

- **PASS**: All functionality works as expected
- **FAIL**: Test assertion failed - indicates a bug
- **ERROR**: Test raised an unexpected exception
- **SKIP**: Test was skipped (not applicable)

## Coverage Summary

The test suite provides comprehensive coverage of:
- ✓ Video downloading
- ✓ Audio extraction
- ✓ Video cropping
- ✓ Audio transcription
- ✓ AI-based highlight extraction (transcript mode)
- ✓ AI-based highlight extraction (vision mode)
- ✓ Face detection and tracking
- ✓ Speaker detection
- ✓ Voice activity detection
- ✓ Vertical video cropping
- ✓ Video/audio combination
- ✓ Main application workflow
- ✓ Error handling throughout

## Future Enhancements

Potential improvements to the test suite:
1. Integration tests with sample video files
2. Performance benchmarks
3. Code coverage reporting
4. Continuous integration setup
5. Visual regression testing for video output
