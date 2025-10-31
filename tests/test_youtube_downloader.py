"""
Tests for YoutubeDownloader.py
Tests the YouTube video download functionality
"""
import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Components.YoutubeDownloader import download_youtube_video, get_video_size


class TestYoutubeDownloader(unittest.TestCase):
    """Test cases for YouTube downloader functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_url = "https://www.youtube.com/watch?v=test123"
        self.mock_title = "Test Video"
        
    def test_get_video_size(self):
        """Test video size calculation"""
        mock_stream = MagicMock()
        mock_stream.filesize = 10485760  # 10 MB in bytes
        
        size_mb = get_video_size(mock_stream)
        self.assertEqual(size_mb, 10.0)
        
    def test_get_video_size_zero(self):
        """Test video size calculation with zero size"""
        mock_stream = MagicMock()
        mock_stream.filesize = 0
        
        size_mb = get_video_size(mock_stream)
        self.assertEqual(size_mb, 0.0)
        
    @patch('Components.YoutubeDownloader.YouTube')
    @patch('Components.YoutubeDownloader.ffmpeg')
    @patch('builtins.input', return_value='0')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    @patch('os.remove')
    def test_download_progressive_video(self, mock_remove, mock_exists, mock_makedirs, 
                                       mock_input, mock_ffmpeg, mock_youtube):
        """Test downloading a progressive video stream"""
        # Setup mocks
        mock_yt = MagicMock()
        mock_yt.title = self.mock_title
        mock_youtube.return_value = mock_yt
        
        # Create mock stream
        mock_stream = MagicMock()
        mock_stream.resolution = "720p"
        mock_stream.filesize = 10485760
        mock_stream.is_progressive = True
        mock_stream.download.return_value = "videos/video_Test Video.mp4"
        
        mock_yt.streams.filter.return_value.order_by.return_value.desc.return_value = [mock_stream]
        
        # Execute
        result = download_youtube_video(self.test_url)
        
        # Verify
        self.assertEqual(result, "videos/video_Test Video.mp4")
        mock_youtube.assert_called_once_with(self.test_url)
        mock_stream.download.assert_called_once()
        mock_makedirs.assert_called_once_with('videos')
        
    @patch('Components.YoutubeDownloader.YouTube')
    @patch('Components.YoutubeDownloader.ffmpeg')
    @patch('builtins.input', return_value='0')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    @patch('os.remove')
    def test_download_adaptive_video(self, mock_remove, mock_exists, mock_makedirs,
                                     mock_input, mock_ffmpeg, mock_youtube):
        """Test downloading an adaptive video stream (video + audio merge)"""
        # Setup mocks
        mock_yt = MagicMock()
        mock_yt.title = self.mock_title
        mock_youtube.return_value = mock_yt
        
        # Create mock video stream
        mock_video_stream = MagicMock()
        mock_video_stream.resolution = "1080p"
        mock_video_stream.filesize = 20971520
        mock_video_stream.is_progressive = False
        mock_video_stream.download.return_value = "videos/video_Test Video.webm"
        
        # Create mock audio stream
        mock_audio_stream = MagicMock()
        mock_audio_stream.download.return_value = "videos/audio_Test Video.webm"
        
        mock_yt.streams.filter.return_value.order_by.return_value.desc.return_value = [mock_video_stream]
        mock_yt.streams.filter.return_value.first.return_value = mock_audio_stream
        
        # Mock ffmpeg
        mock_ffmpeg.input.return_value = MagicMock()
        mock_ffmpeg.output.return_value = MagicMock()
        mock_ffmpeg.run.return_value = None
        
        # Execute
        result = download_youtube_video(self.test_url)
        
        # Verify
        self.assertTrue(result.endswith('.mp4'))
        mock_youtube.assert_called_once_with(self.test_url)
        mock_video_stream.download.assert_called_once()
        mock_audio_stream.download.assert_called_once()
        
    @patch('Components.YoutubeDownloader.YouTube')
    @patch('builtins.input', return_value='0')
    def test_download_video_exception(self, mock_input, mock_youtube):
        """Test error handling when download fails"""
        # Setup mock to raise exception
        mock_youtube.side_effect = Exception("Network error")
        
        # Execute
        result = download_youtube_video(self.test_url)
        
        # Verify - should return None on error
        self.assertIsNone(result)
        
    @patch('Components.YoutubeDownloader.YouTube')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.input', return_value='0')
    def test_download_video_directory_exists(self, mock_input, mock_exists, mock_youtube):
        """Test that videos directory is not created if it already exists"""
        # Setup mocks
        mock_yt = MagicMock()
        mock_yt.title = self.mock_title
        mock_youtube.return_value = mock_yt
        
        mock_stream = MagicMock()
        mock_stream.resolution = "720p"
        mock_stream.filesize = 10485760
        mock_stream.is_progressive = True
        mock_stream.download.return_value = "videos/video_Test Video.mp4"
        
        mock_yt.streams.filter.return_value.order_by.return_value.desc.return_value = [mock_stream]
        
        # Execute
        with patch('os.makedirs') as mock_makedirs:
            result = download_youtube_video(self.test_url)
            
            # Verify directory creation was not called
            mock_makedirs.assert_not_called()


if __name__ == '__main__':
    unittest.main()
