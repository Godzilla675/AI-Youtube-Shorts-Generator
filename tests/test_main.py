"""
Tests for main.py
Tests the main application workflow and menu system
"""
import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main


class TestMain(unittest.TestCase):
    """Test cases for main application"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_url = "https://www.youtube.com/watch?v=test123"
        self.test_video_path = "videos/test_video.mp4"
        
    @patch('builtins.print')
    def test_print_menu(self, mock_print):
        """Test menu display"""
        main.print_menu()
        
        # Verify menu items are printed
        self.assertGreater(mock_print.call_count, 5)
        
    @patch('builtins.input', return_value='1')
    def test_select_transcript_model_gpt4o(self, mock_input):
        """Test GPT-4o model selection"""
        result = main.select_transcript_model()
        self.assertEqual(result, "gpt-4o")
        
    @patch('builtins.input', return_value='2')
    def test_select_transcript_model_gemini_2_5_flash(self, mock_input):
        """Test Gemini 2.5 Flash selection"""
        result = main.select_transcript_model()
        self.assertEqual(result, "gemini-2.5-flash-002")
        
    @patch('builtins.input', return_value='3')
    def test_select_transcript_model_gemini_2_5_pro(self, mock_input):
        """Test Gemini 2.5 Pro selection"""
        result = main.select_transcript_model()
        self.assertEqual(result, "gemini-2.5-pro-002")
        
    @patch('builtins.input', return_value='4')
    def test_select_transcript_model_gemini_1_5_flash(self, mock_input):
        """Test Gemini 1.5 Flash selection"""
        result = main.select_transcript_model()
        self.assertEqual(result, "gemini-1.5-flash")
        
    @patch('builtins.input', return_value='5')
    def test_select_transcript_model_gemini_1_5_pro(self, mock_input):
        """Test Gemini 1.5 Pro selection"""
        result = main.select_transcript_model()
        self.assertEqual(result, "gemini-1.5-pro")
        
    @patch('builtins.input', return_value='')
    def test_select_transcript_model_default(self, mock_input):
        """Test default model selection"""
        result = main.select_transcript_model()
        self.assertEqual(result, "gemini-2.5-flash-002")
        
    @patch('builtins.input', return_value='1')
    def test_select_vision_model_gemini_2_5_flash(self, mock_input):
        """Test Gemini 2.5 Flash vision model selection"""
        result = main.select_vision_model()
        self.assertEqual(result, "gemini-2.5-flash-002")
        
    @patch('builtins.input', return_value='2')
    def test_select_vision_model_gemini_2_5_pro(self, mock_input):
        """Test Gemini 2.5 Pro vision model selection"""
        result = main.select_vision_model()
        self.assertEqual(result, "gemini-2.5-pro-002")
        
    @patch('builtins.input', return_value='3')
    def test_select_vision_model_gemini_1_5_flash(self, mock_input):
        """Test Gemini 1.5 Flash vision model selection"""
        result = main.select_vision_model()
        self.assertEqual(result, "gemini-1.5-flash")
        
    @patch('builtins.input', return_value='4')
    def test_select_vision_model_gemini_1_5_pro(self, mock_input):
        """Test Gemini 1.5 Pro vision model selection"""
        result = main.select_vision_model()
        self.assertEqual(result, "gemini-1.5-pro")
        
    @patch('builtins.input', return_value='')
    def test_select_vision_model_default(self, mock_input):
        """Test default vision model selection"""
        result = main.select_vision_model()
        self.assertEqual(result, "gemini-2.5-flash-002")
        
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_download_failure(self, mock_input, mock_download):
        """Test main function with download failure"""
        mock_input.side_effect = ['1', self.test_url]
        mock_download.return_value = None
        
        # Execute
        main.main()
        
        # Verify
        mock_download.assert_called_once_with(self.test_url)
        
    @patch('main.combine_videos')
    @patch('main.crop_to_vertical')
    @patch('main.crop_video')
    @patch('main.GetHighlight')
    @patch('main.transcribeAudio')
    @patch('main.extractAudio')
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_transcript_mode_success(self, mock_input, mock_download, mock_extract,
                                         mock_transcribe, mock_get_highlight, mock_crop,
                                         mock_crop_vertical, mock_combine):
        """Test successful transcript mode execution"""
        # Setup mocks
        mock_input.side_effect = ['1', '2', self.test_url]  # Mode 1, Gemini 2.5 Flash, URL
        mock_download.return_value = self.test_video_path
        mock_extract.return_value = "audio.wav"
        mock_transcribe.return_value = [
            ["Hello world", 0.0, 5.0],
            ["This is a test", 5.0, 10.0]
        ]
        mock_get_highlight.return_value = (10, 40)
        
        # Execute
        main.main()
        
        # Verify
        mock_download.assert_called_once_with(self.test_url)
        mock_extract.assert_called_once()
        mock_transcribe.assert_called_once()
        mock_get_highlight.assert_called_once()
        mock_crop.assert_called_once()
        mock_crop_vertical.assert_called_once()
        mock_combine.assert_called_once()
        
    @patch('main.combine_videos')
    @patch('main.crop_to_vertical')
    @patch('main.crop_video')
    @patch('main.GetHighlightFromVideo')
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_vision_mode_success(self, mock_input, mock_download,
                                     mock_get_highlight, mock_crop,
                                     mock_crop_vertical, mock_combine):
        """Test successful vision mode execution"""
        # Setup mocks
        mock_input.side_effect = ['2', '1', self.test_url]  # Mode 2, Gemini 2.5 Flash, URL
        mock_download.return_value = self.test_video_path
        mock_get_highlight.return_value = (15, 45)
        
        # Execute
        main.main()
        
        # Verify
        mock_download.assert_called_once_with(self.test_url)
        mock_get_highlight.assert_called_once()
        mock_crop.assert_called_once()
        mock_crop_vertical.assert_called_once()
        mock_combine.assert_called_once()
        
    @patch('main.extractAudio')
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_no_audio_file(self, mock_input, mock_download, mock_extract):
        """Test handling when audio extraction fails"""
        mock_input.side_effect = ['1', '2', self.test_url]
        mock_download.return_value = self.test_video_path
        mock_extract.return_value = None
        
        # Execute
        main.main()
        
        # Verify
        mock_extract.assert_called_once()
        
    @patch('main.transcribeAudio')
    @patch('main.extractAudio')
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_no_transcriptions(self, mock_input, mock_download, mock_extract,
                                   mock_transcribe):
        """Test handling when transcription fails"""
        mock_input.side_effect = ['1', '2', self.test_url]
        mock_download.return_value = self.test_video_path
        mock_extract.return_value = "audio.wav"
        mock_transcribe.return_value = []
        
        # Execute
        main.main()
        
        # Verify
        mock_transcribe.assert_called_once()
        
    @patch('main.GetHighlight')
    @patch('main.transcribeAudio')
    @patch('main.extractAudio')
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_highlight_exception(self, mock_input, mock_download, mock_extract,
                                     mock_transcribe, mock_get_highlight):
        """Test handling when highlight extraction raises exception"""
        mock_input.side_effect = ['1', '2', self.test_url]
        mock_download.return_value = self.test_video_path
        mock_extract.return_value = "audio.wav"
        mock_transcribe.return_value = [["Test", 0.0, 5.0]]
        mock_get_highlight.side_effect = Exception("API Error")
        
        # Execute
        main.main()
        
        # Verify exception was handled
        mock_get_highlight.assert_called_once()
        
    @patch('main.crop_video')
    @patch('main.GetHighlight')
    @patch('main.transcribeAudio')
    @patch('main.extractAudio')
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_invalid_highlight_times(self, mock_input, mock_download, mock_extract,
                                         mock_transcribe, mock_get_highlight, mock_crop):
        """Test handling of invalid highlight times"""
        mock_input.side_effect = ['1', '2', self.test_url]
        mock_download.return_value = self.test_video_path
        mock_extract.return_value = "audio.wav"
        mock_transcribe.return_value = [["Test", 0.0, 5.0]]
        mock_get_highlight.return_value = (-1, 0)  # Invalid times
        
        # Execute
        main.main()
        
        # Verify crop_video was not called
        mock_crop.assert_not_called()
        
    @patch('main.crop_video')
    @patch('main.GetHighlight')
    @patch('main.transcribeAudio')
    @patch('main.extractAudio')
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_start_greater_than_end(self, mock_input, mock_download, mock_extract,
                                        mock_transcribe, mock_get_highlight, mock_crop):
        """Test handling when start time is greater than end time"""
        mock_input.side_effect = ['1', '2', self.test_url]
        mock_download.return_value = self.test_video_path
        mock_extract.return_value = "audio.wav"
        mock_transcribe.return_value = [["Test", 0.0, 5.0]]
        mock_get_highlight.return_value = (50, 30)  # start > end
        
        # Execute
        main.main()
        
        # Verify crop_video was not called
        mock_crop.assert_not_called()
        
    @patch('main.GetHighlightFromVideo')
    @patch('main.download_youtube_video')
    @patch('builtins.input')
    def test_main_vision_mode_exception(self, mock_input, mock_download,
                                       mock_get_highlight):
        """Test handling when vision mode raises exception"""
        mock_input.side_effect = ['2', '1', self.test_url]
        mock_download.return_value = self.test_video_path
        mock_get_highlight.side_effect = Exception("Vision API Error")
        
        # Execute
        main.main()
        
        # Verify exception was handled
        mock_get_highlight.assert_called_once()


if __name__ == '__main__':
    unittest.main()
