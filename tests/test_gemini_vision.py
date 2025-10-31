"""
Tests for GeminiVision.py
Tests video analysis and highlight extraction using Gemini's vision capabilities
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Components.GeminiVision import GetHighlightFromVideo, VideoHighlight


class TestGeminiVision(unittest.TestCase):
    """Test cases for Gemini vision functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_video_path = "test_video.mp4"
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    def test_get_highlight_from_video_success(self, mock_genai):
        """Test successful video highlight extraction"""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.state.name = "ACTIVE"
        mock_file.name = "test_file_id"
        
        mock_genai.upload_file.return_value = mock_file
        mock_genai.get_file.return_value = mock_file
        
        # Mock model and response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"start": 10.0, "content": "Exciting moment", "end": 35.0}'
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute
        start, end = GetHighlightFromVideo(self.test_video_path, "gemini-2.5-flash-002")
        
        # Verify
        self.assertEqual(start, 10)
        self.assertEqual(end, 35)
        mock_genai.upload_file.assert_called_once_with(path=self.test_video_path)
        mock_genai.delete_file.assert_called_once_with("test_file_id")
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    @patch('time.sleep')
    def test_get_highlight_processing_state(self, mock_sleep, mock_genai):
        """Test handling of video processing state"""
        # Setup mocks
        mock_file_processing = MagicMock()
        mock_file_processing.state.name = "PROCESSING"
        mock_file_processing.name = "test_file_id"
        
        mock_file_active = MagicMock()
        mock_file_active.state.name = "ACTIVE"
        mock_file_active.name = "test_file_id"
        
        mock_genai.upload_file.return_value = mock_file_processing
        mock_genai.get_file.side_effect = [mock_file_processing, mock_file_active]
        
        # Mock model and response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"start": 5.0, "content": "Good part", "end": 25.0}'
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute
        start, end = GetHighlightFromVideo(self.test_video_path, "gemini-2.5-flash-002")
        
        # Verify
        self.assertEqual(start, 5)
        self.assertEqual(end, 25)
        self.assertEqual(mock_genai.get_file.call_count, 2)
        mock_sleep.assert_called()
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    def test_get_highlight_failed_processing(self, mock_genai):
        """Test handling when video processing fails"""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.state.name = "FAILED"
        mock_file.name = "test_file_id"
        
        mock_genai.upload_file.return_value = mock_file
        
        # Execute and verify
        with self.assertRaises(ValueError) as context:
            GetHighlightFromVideo(self.test_video_path, "gemini-2.5-flash-002")
        
        self.assertIn("processing failed", str(context.exception).lower())
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    def test_get_highlight_invalid_json_response(self, mock_genai):
        """Test handling of invalid JSON response"""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.state.name = "ACTIVE"
        mock_file.name = "test_file_id"
        
        mock_genai.upload_file.return_value = mock_file
        mock_genai.get_file.return_value = mock_file
        
        # Mock model with invalid response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = 'This is not valid JSON'
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute and verify
        with patch('builtins.input', return_value='n'):
            with self.assertRaises(ValueError) as context:
                GetHighlightFromVideo(self.test_video_path, "gemini-2.5-flash-002")
        
        self.assertIn("JSON", str(context.exception))
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    def test_get_highlight_segment_too_long(self, mock_genai):
        """Test handling when segment is longer than 60 seconds"""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.state.name = "ACTIVE"
        mock_file.name = "test_file_id"
        
        mock_genai.upload_file.return_value = mock_file
        mock_genai.get_file.return_value = mock_file
        
        # Mock model with long segment
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"start": 10.0, "content": "Long segment", "end": 95.0}'
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute
        start, end = GetHighlightFromVideo(self.test_video_path, "gemini-2.5-flash-002")
        
        # Verify - should be truncated to 60 seconds
        self.assertEqual(start, 10)
        self.assertEqual(end, 70)  # start + 60
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    def test_get_highlight_invalid_time_range(self, mock_genai):
        """Test handling when start >= end"""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.state.name = "ACTIVE"
        mock_file.name = "test_file_id"
        
        mock_genai.upload_file.return_value = mock_file
        mock_genai.get_file.return_value = mock_file
        
        # Mock model with invalid time range
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"start": 50.0, "content": "Invalid", "end": 30.0}'
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute and verify
        with patch('builtins.input', return_value='n'):
            with self.assertRaises(ValueError):
                GetHighlightFromVideo(self.test_video_path, "gemini-2.5-flash-002")
                
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    def test_get_highlight_with_different_models(self, mock_genai):
        """Test with different Gemini models"""
        models = [
            "gemini-2.5-flash-002",
            "gemini-2.5-pro-002",
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ]
        
        for model_name in models:
            with self.subTest(model=model_name):
                # Setup mocks
                mock_file = MagicMock()
                mock_file.state.name = "ACTIVE"
                mock_file.name = "test_file_id"
                
                mock_genai.upload_file.return_value = mock_file
                mock_genai.get_file.return_value = mock_file
                
                # Mock model and response
                mock_model = MagicMock()
                mock_response = MagicMock()
                mock_response.text = '{"start": 15.0, "content": "Test", "end": 45.0}'
                mock_model.generate_content.return_value = mock_response
                
                mock_genai.GenerativeModel.return_value = mock_model
                
                # Execute
                start, end = GetHighlightFromVideo(self.test_video_path, model_name)
                
                # Verify
                self.assertEqual(start, 15)
                self.assertEqual(end, 45)
                
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_gemini_api_key(self):
        """Test error when GEMINI_API key is not set"""
        # This should raise an error during module import or initialization
        # We test this by trying to reload the module
        with self.assertRaises(ValueError):
            # Clear the module from cache and reimport
            if 'Components.GeminiVision' in sys.modules:
                del sys.modules['Components.GeminiVision']
            import Components.GeminiVision
            
    def test_video_highlight_model(self):
        """Test VideoHighlight pydantic model"""
        # Create instance
        highlight = VideoHighlight(
            start=10.5,
            content="Interesting visual moment",
            end=30.7
        )
        
        # Verify
        self.assertEqual(highlight.start, 10.5)
        self.assertEqual(highlight.content, "Interesting visual moment")
        self.assertEqual(highlight.end, 30.7)
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    def test_cleanup_on_success(self, mock_genai):
        """Test that uploaded file is cleaned up after success"""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.state.name = "ACTIVE"
        mock_file.name = "test_file_id"
        
        mock_genai.upload_file.return_value = mock_file
        mock_genai.get_file.return_value = mock_file
        
        # Mock model and response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"start": 10.0, "content": "Test", "end": 30.0}'
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute
        GetHighlightFromVideo(self.test_video_path, "gemini-2.5-flash-002")
        
        # Verify cleanup
        mock_genai.delete_file.assert_called_once_with("test_file_id")
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.GeminiVision.genai')
    def test_cleanup_on_error(self, mock_genai):
        """Test that uploaded file is cleaned up even on error"""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.state.name = "ACTIVE"
        mock_file.name = "test_file_id"
        
        mock_genai.upload_file.return_value = mock_file
        mock_genai.get_file.return_value = mock_file
        
        # Mock model to raise error
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Execute
        with patch('builtins.input', return_value='n'):
            with self.assertRaises(Exception):
                GetHighlightFromVideo(self.test_video_path, "gemini-2.5-flash-002")
        
        # Verify cleanup was attempted
        mock_genai.delete_file.assert_called()


if __name__ == '__main__':
    unittest.main()
