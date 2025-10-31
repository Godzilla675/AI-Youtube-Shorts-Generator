"""
Tests for Transcription.py
Tests audio transcription functionality using Whisper
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Components.Transcription import transcribeAudio


class TestTranscription(unittest.TestCase):
    """Test cases for audio transcription functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_audio_path = "test_audio.wav"
        
    @patch('Components.Transcription.torch')
    @patch('Components.Transcription.WhisperModel')
    def test_transcribe_audio_success(self, mock_whisper_model, mock_torch):
        """Test successful audio transcription"""
        # Setup mocks
        mock_torch.cuda.is_available.return_value = False
        
        # Create mock segments
        mock_segment1 = MagicMock()
        mock_segment1.text = " Hello world"
        mock_segment1.start = 0.0
        mock_segment1.end = 2.5
        
        mock_segment2 = MagicMock()
        mock_segment2.text = " This is a test"
        mock_segment2.start = 2.5
        mock_segment2.end = 5.0
        
        mock_model = MagicMock()
        mock_model.transcribe.return_value = ([mock_segment1, mock_segment2], None)
        mock_whisper_model.return_value = mock_model
        
        # Execute
        result = transcribeAudio(self.test_audio_path)
        
        # Verify
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [" Hello world", 0.0, 2.5])
        self.assertEqual(result[1], [" This is a test", 2.5, 5.0])
        mock_whisper_model.assert_called_once_with("base.en", device="cpu")
        
    @patch('Components.Transcription.torch')
    @patch('Components.Transcription.WhisperModel')
    def test_transcribe_audio_with_cuda(self, mock_whisper_model, mock_torch):
        """Test transcription with CUDA available"""
        # Setup mocks
        mock_torch.cuda.is_available.return_value = True
        
        mock_segment = MagicMock()
        mock_segment.text = " Test with GPU"
        mock_segment.start = 0.0
        mock_segment.end = 3.0
        
        mock_model = MagicMock()
        mock_model.transcribe.return_value = ([mock_segment], None)
        mock_whisper_model.return_value = mock_model
        
        # Execute
        result = transcribeAudio(self.test_audio_path)
        
        # Verify
        self.assertEqual(len(result), 1)
        mock_whisper_model.assert_called_once_with("base.en", device="cuda")
        
    @patch('Components.Transcription.torch')
    @patch('Components.Transcription.WhisperModel')
    def test_transcribe_audio_empty_result(self, mock_whisper_model, mock_torch):
        """Test transcription with no segments"""
        # Setup mocks
        mock_torch.cuda.is_available.return_value = False
        
        mock_model = MagicMock()
        mock_model.transcribe.return_value = ([], None)
        mock_whisper_model.return_value = mock_model
        
        # Execute
        result = transcribeAudio(self.test_audio_path)
        
        # Verify
        self.assertEqual(result, [])
        
    @patch('Components.Transcription.torch')
    @patch('Components.Transcription.WhisperModel')
    def test_transcribe_audio_exception(self, mock_whisper_model, mock_torch):
        """Test error handling when transcription fails"""
        # Setup mocks
        mock_torch.cuda.is_available.return_value = False
        mock_whisper_model.side_effect = Exception("Model loading failed")
        
        # Execute
        result = transcribeAudio(self.test_audio_path)
        
        # Verify
        self.assertEqual(result, [])
        
    @patch('Components.Transcription.torch')
    @patch('Components.Transcription.WhisperModel')
    def test_transcribe_audio_with_multiple_segments(self, mock_whisper_model, mock_torch):
        """Test transcription with multiple segments"""
        # Setup mocks
        mock_torch.cuda.is_available.return_value = False
        
        # Create multiple mock segments
        segments = []
        for i in range(5):
            mock_segment = MagicMock()
            mock_segment.text = f" Segment {i}"
            mock_segment.start = float(i * 2)
            mock_segment.end = float((i + 1) * 2)
            segments.append(mock_segment)
        
        mock_model = MagicMock()
        mock_model.transcribe.return_value = (segments, None)
        mock_whisper_model.return_value = mock_model
        
        # Execute
        result = transcribeAudio(self.test_audio_path)
        
        # Verify
        self.assertEqual(len(result), 5)
        for i, item in enumerate(result):
            self.assertEqual(item[0], f" Segment {i}")
            self.assertEqual(item[1], float(i * 2))
            self.assertEqual(item[2], float((i + 1) * 2))
            
    @patch('Components.Transcription.torch')
    @patch('Components.Transcription.WhisperModel')
    def test_transcribe_audio_parameters(self, mock_whisper_model, mock_torch):
        """Test that transcribe is called with correct parameters"""
        # Setup mocks
        mock_torch.cuda.is_available.return_value = False
        
        mock_model = MagicMock()
        mock_model.transcribe.return_value = ([], None)
        mock_whisper_model.return_value = mock_model
        
        # Execute
        transcribeAudio(self.test_audio_path)
        
        # Verify parameters
        mock_model.transcribe.assert_called_once_with(
            audio=self.test_audio_path,
            beam_size=5,
            language="en",
            max_new_tokens=128,
            condition_on_previous_text=False
        )


if __name__ == '__main__':
    unittest.main()
