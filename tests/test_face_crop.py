"""
Tests for FaceCrop.py
Tests vertical cropping and video combination functionality
"""
import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestFaceCrop(unittest.TestCase):
    """Test cases for face crop functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_input_video = "test_input.mp4"
        self.test_output_video = "test_output.mp4"
        self.test_final_video = "test_final.mp4"
        
    @patch('Components.FaceCrop.detect_faces_and_speakers')
    @patch('Components.FaceCrop.cv2')
    def test_crop_to_vertical_basic(self, mock_cv2, mock_detect):
        """Test basic vertical cropping"""
        # Import here to avoid issues with patching
        from Components.FaceCrop import crop_to_vertical, Frames
        
        # Setup mocks
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {
            3: 1920,  # Width
            4: 1080,  # Height
            5: 30.0,  # FPS
            7: 10     # Frame count
        }.get(prop, 0)
        
        # Mock frame reading
        mock_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, mock_frame)] * 10 + [(False, None)]
        
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.CAP_FFMPEG = 0
        mock_cv2.CAP_PROP_FRAME_WIDTH = 3
        mock_cv2.CAP_PROP_FRAME_HEIGHT = 4
        mock_cv2.CAP_PROP_FPS = 5
        mock_cv2.CAP_PROP_FRAME_COUNT = 7
        mock_cv2.VideoWriter_fourcc.return_value = 0
        
        # Mock cascade classifier
        mock_face_cascade = MagicMock()
        mock_face_cascade.detectMultiScale.return_value = np.array([[100, 100, 200, 200]])
        mock_cv2.CascadeClassifier.return_value = mock_face_cascade
        mock_cv2.cvtColor.return_value = mock_frame[:, :, 0]
        mock_cv2.COLOR_BGR2GRAY = 6
        
        mock_out = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_out
        
        # Setup Frames global
        Frames.clear()
        for _ in range(10):
            Frames.append([100, 100, 300, 300])
        
        # Execute
        crop_to_vertical(self.test_input_video, self.test_output_video)
        
        # Verify
        mock_detect.assert_called_once()
        mock_cv2.VideoCapture.assert_called()
        mock_out.write.assert_called()
        mock_cap.release.assert_called_once()
        mock_out.release.assert_called_once()
        
    @patch('Components.FaceCrop.VideoFileClip')
    def test_combine_videos_success(self, mock_video_clip):
        """Test successful video combination"""
        from Components.FaceCrop import combine_videos, Fps
        
        # Setup mocks
        mock_clip_with_audio = MagicMock()
        mock_clip_without_audio = MagicMock()
        mock_audio = MagicMock()
        mock_combined = MagicMock()
        
        mock_clip_with_audio.audio = mock_audio
        mock_clip_without_audio.set_audio.return_value = mock_combined
        
        def video_clip_side_effect(path):
            if "audio" in path:
                return mock_clip_with_audio
            else:
                return mock_clip_without_audio
        
        mock_video_clip.side_effect = video_clip_side_effect
        
        # Execute
        combine_videos("video_with_audio.mp4", "video_without_audio.mp4", 
                      self.test_final_video)
        
        # Verify
        mock_clip_without_audio.set_audio.assert_called_once_with(mock_audio)
        mock_combined.write_videofile.assert_called_once()
        
    @patch('Components.FaceCrop.VideoFileClip')
    def test_combine_videos_exception(self, mock_video_clip):
        """Test error handling in video combination"""
        from Components.FaceCrop import combine_videos
        
        # Setup mock to raise exception
        mock_video_clip.side_effect = Exception("Video file not found")
        
        # Execute - should not raise, just print error
        try:
            combine_videos("video1.mp4", "video2.mp4", self.test_final_video)
        except Exception as e:
            self.fail(f"combine_videos raised {e} unexpectedly")
            
    @patch('Components.FaceCrop.detect_faces_and_speakers')
    @patch('Components.FaceCrop.cv2')
    def test_crop_to_vertical_no_video(self, mock_cv2, mock_detect):
        """Test handling when video cannot be opened"""
        from Components.FaceCrop import crop_to_vertical
        
        # Setup mocks
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.CAP_FFMPEG = 0
        
        # Execute - should return early
        crop_to_vertical(self.test_input_video, self.test_output_video)
        
        # Verify
        mock_cap.release.assert_not_called()
        
    @patch('Components.FaceCrop.detect_faces_and_speakers')
    @patch('Components.FaceCrop.cv2')
    def test_crop_to_vertical_narrow_video(self, mock_cv2, mock_detect):
        """Test handling when video width is less than desired vertical width"""
        from Components.FaceCrop import crop_to_vertical
        
        # Setup mocks - narrow video
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {
            3: 500,   # Width (narrow)
            4: 1080,  # Height
            5: 30.0,  # FPS
            7: 1      # Frame count
        }.get(prop, 0)
        
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.CAP_FFMPEG = 0
        mock_cv2.CAP_PROP_FRAME_WIDTH = 3
        mock_cv2.CAP_PROP_FRAME_HEIGHT = 4
        mock_cv2.CAP_PROP_FPS = 5
        mock_cv2.CAP_PROP_FRAME_COUNT = 7
        
        # Execute - should return early
        crop_to_vertical(self.test_input_video, self.test_output_video)
        
        # Verify early return
        mock_cap.release.assert_not_called()
        
    @patch('Components.FaceCrop.detect_faces_and_speakers')
    @patch('Components.FaceCrop.cv2')
    def test_crop_to_vertical_with_face_detection(self, mock_cv2, mock_detect):
        """Test vertical cropping with face detection"""
        from Components.FaceCrop import crop_to_vertical, Frames
        
        # Setup mocks
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {
            3: 1920,
            4: 1080,
            5: 30.0,
            7: 5
        }.get(prop, 0)
        
        mock_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, mock_frame)] * 5 + [(False, None)]
        
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.CAP_FFMPEG = 0
        mock_cv2.CAP_PROP_FRAME_WIDTH = 3
        mock_cv2.CAP_PROP_FRAME_HEIGHT = 4
        mock_cv2.CAP_PROP_FPS = 5
        mock_cv2.CAP_PROP_FRAME_COUNT = 7
        mock_cv2.VideoWriter_fourcc.return_value = 0
        
        # Mock face detection with multiple faces
        mock_face_cascade = MagicMock()
        faces_detected = [
            np.array([[800, 400, 150, 150], [1000, 400, 150, 150]]),  # Two faces
            np.array([[850, 400, 150, 150]]),  # One face
            np.array([]),  # No face
            np.array([[900, 400, 150, 150]]),  # One face
            np.array([[950, 400, 150, 150]])   # One face
        ]
        mock_face_cascade.detectMultiScale.side_effect = faces_detected
        mock_cv2.CascadeClassifier.return_value = mock_face_cascade
        mock_cv2.cvtColor.return_value = mock_frame[:, :, 0]
        mock_cv2.COLOR_BGR2GRAY = 6
        
        mock_out = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_out
        
        # Setup Frames
        Frames.clear()
        for _ in range(5):
            Frames.append([800, 400, 950, 550])
        
        # Execute
        crop_to_vertical(self.test_input_video, self.test_output_video)
        
        # Verify
        self.assertEqual(mock_out.write.call_count, 5)
        
    @patch('Components.FaceCrop.VideoFileClip')
    def test_combine_videos_parameters(self, mock_video_clip):
        """Test that combine_videos passes correct parameters"""
        from Components.FaceCrop import combine_videos
        import Components.FaceCrop as fc
        
        # Setup mocks
        mock_clip_with_audio = MagicMock()
        mock_clip_without_audio = MagicMock()
        mock_audio = MagicMock()
        mock_combined = MagicMock()
        
        mock_clip_with_audio.audio = mock_audio
        mock_clip_without_audio.set_audio.return_value = mock_combined
        
        mock_video_clip.side_effect = [mock_clip_with_audio, mock_clip_without_audio]
        
        # Set FPS
        fc.Fps = 30.0
        
        # Execute
        combine_videos("video1.mp4", "video2.mp4", self.test_final_video)
        
        # Verify write_videofile parameters
        call_args = mock_combined.write_videofile.call_args
        self.assertEqual(call_args[0][0], self.test_final_video)
        self.assertEqual(call_args[1]['codec'], 'libx264')
        self.assertEqual(call_args[1]['audio_codec'], 'aac')
        self.assertEqual(call_args[1]['fps'], 30.0)


if __name__ == '__main__':
    unittest.main()
