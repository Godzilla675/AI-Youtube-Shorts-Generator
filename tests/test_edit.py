"""
Tests for Edit.py
Tests audio extraction and video cropping functionality
"""
import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Components.Edit import extractAudio, crop_video


class TestEdit(unittest.TestCase):
    """Test cases for video editing functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_video_path = "test_video.mp4"
        self.test_audio_path = "audio.wav"
        self.test_output_path = "output.mp4"
        
    @patch('Components.Edit.VideoFileClip')
    def test_extract_audio_success(self, mock_video_clip):
        """Test successful audio extraction"""
        # Setup mocks
        mock_clip = MagicMock()
        mock_audio = MagicMock()
        mock_clip.audio = mock_audio
        mock_video_clip.return_value = mock_clip
        
        # Execute
        result = extractAudio(self.test_video_path)
        
        # Verify
        self.assertEqual(result, "audio.wav")
        mock_video_clip.assert_called_once_with(self.test_video_path)
        mock_audio.write_audiofile.assert_called_once_with("audio.wav")
        mock_clip.close.assert_called_once()
        
    @patch('Components.Edit.VideoFileClip')
    def test_extract_audio_exception(self, mock_video_clip):
        """Test error handling when audio extraction fails"""
        # Setup mock to raise exception
        mock_video_clip.side_effect = Exception("File not found")
        
        # Execute
        result = extractAudio(self.test_video_path)
        
        # Verify
        self.assertIsNone(result)
        
    @patch('Components.Edit.VideoFileClip')
    def test_extract_audio_no_audio_stream(self, mock_video_clip):
        """Test extraction when video has no audio"""
        # Setup mocks
        mock_clip = MagicMock()
        mock_clip.audio = None
        mock_video_clip.return_value = mock_clip
        
        # Execute - should raise AttributeError
        with self.assertRaises(AttributeError):
            extractAudio(self.test_video_path)
            
    @patch('Components.Edit.VideoFileClip')
    def test_crop_video_success(self, mock_video_clip):
        """Test successful video cropping"""
        # Setup mocks
        mock_clip = MagicMock()
        mock_subclip = MagicMock()
        mock_clip.subclip.return_value = mock_subclip
        mock_video_clip.return_value.__enter__.return_value = mock_clip
        
        start_time = 10.0
        end_time = 30.0
        
        # Execute
        crop_video(self.test_video_path, self.test_output_path, start_time, end_time)
        
        # Verify
        mock_video_clip.assert_called_once_with(self.test_video_path)
        mock_clip.subclip.assert_called_once_with(start_time, end_time)
        mock_subclip.write_videofile.assert_called_once_with(
            self.test_output_path, codec='libx264'
        )
        
    @patch('Components.Edit.VideoFileClip')
    def test_crop_video_zero_duration(self, mock_video_clip):
        """Test cropping with zero duration"""
        # Setup mocks
        mock_clip = MagicMock()
        mock_subclip = MagicMock()
        mock_clip.subclip.return_value = mock_subclip
        mock_video_clip.return_value.__enter__.return_value = mock_clip
        
        start_time = 10.0
        end_time = 10.0  # Same as start
        
        # Execute
        crop_video(self.test_video_path, self.test_output_path, start_time, end_time)
        
        # Verify subclip was called even with zero duration
        mock_clip.subclip.assert_called_once_with(start_time, end_time)
        
    @patch('Components.Edit.VideoFileClip')
    def test_crop_video_invalid_range(self, mock_video_clip):
        """Test cropping with invalid time range (end before start)"""
        # Setup mocks
        mock_clip = MagicMock()
        mock_video_clip.return_value.__enter__.return_value = mock_clip
        mock_clip.subclip.side_effect = ValueError("Invalid time range")
        
        start_time = 30.0
        end_time = 10.0  # End before start
        
        # Execute - should raise ValueError
        with self.assertRaises(ValueError):
            crop_video(self.test_video_path, self.test_output_path, start_time, end_time)
            
    @patch('Components.Edit.VideoFileClip')
    def test_crop_video_with_float_times(self, mock_video_clip):
        """Test cropping with precise float time values"""
        # Setup mocks
        mock_clip = MagicMock()
        mock_subclip = MagicMock()
        mock_clip.subclip.return_value = mock_subclip
        mock_video_clip.return_value.__enter__.return_value = mock_clip
        
        start_time = 31.92
        end_time = 49.2
        
        # Execute
        crop_video(self.test_video_path, self.test_output_path, start_time, end_time)
        
        # Verify precise times are passed
        mock_clip.subclip.assert_called_once_with(start_time, end_time)
        mock_subclip.write_videofile.assert_called_once()


if __name__ == '__main__':
    unittest.main()
