"""
Tests for Speaker.py
Tests voice activity detection and speaker detection functionality
"""
import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestSpeaker(unittest.TestCase):
    """Test cases for speaker detection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_video_path = "test_video.mp4"
        self.test_output_path = "test_output.mp4"
        self.test_audio_path = "temp_audio.wav"
        
    @patch('Components.Speaker.vad')
    def test_voice_activity_detection_speech(self, mock_vad):
        """Test voice activity detection with speech"""
        from Components.Speaker import voice_activity_detection
        
        # Setup mock
        mock_vad.is_speech.return_value = True
        audio_frame = b'\x00' * 960  # 30ms of audio at 16kHz
        
        # Execute
        result = voice_activity_detection(audio_frame)
        
        # Verify
        self.assertTrue(result)
        mock_vad.is_speech.assert_called_once_with(audio_frame, 16000)
        
    @patch('Components.Speaker.vad')
    def test_voice_activity_detection_no_speech(self, mock_vad):
        """Test voice activity detection without speech"""
        from Components.Speaker import voice_activity_detection
        
        # Setup mock
        mock_vad.is_speech.return_value = False
        audio_frame = b'\x00' * 960
        
        # Execute
        result = voice_activity_detection(audio_frame)
        
        # Verify
        self.assertFalse(result)
        
    @patch('Components.Speaker.AudioSegment')
    def test_extract_audio_from_video(self, mock_audio_segment):
        """Test audio extraction from video"""
        from Components.Speaker import extract_audio_from_video
        
        # Setup mocks
        mock_audio = MagicMock()
        mock_processed_audio = MagicMock()
        mock_audio.set_frame_rate.return_value = mock_processed_audio
        mock_processed_audio.set_channels.return_value = mock_processed_audio
        mock_audio_segment.from_file.return_value = mock_audio
        
        # Execute
        extract_audio_from_video(self.test_video_path, self.test_audio_path)
        
        # Verify
        mock_audio_segment.from_file.assert_called_once_with(self.test_video_path)
        mock_audio.set_frame_rate.assert_called_once_with(16000)
        mock_processed_audio.set_channels.assert_called_once_with(1)
        mock_processed_audio.export.assert_called_once_with(self.test_audio_path, format="wav")
        
    def test_process_audio_frame(self):
        """Test audio frame processing"""
        from Components.Speaker import process_audio_frame
        
        # Create sample audio data
        sample_rate = 16000
        frame_duration_ms = 30
        n = int(sample_rate * frame_duration_ms / 1000) * 2
        audio_data = b'\x00' * (n * 3)  # 3 frames worth
        
        # Execute
        frames = list(process_audio_frame(audio_data, sample_rate, frame_duration_ms))
        
        # Verify
        self.assertEqual(len(frames), 3)
        for frame in frames:
            self.assertEqual(len(frame), n)
            
    def test_process_audio_frame_incomplete(self):
        """Test audio frame processing with incomplete frame"""
        from Components.Speaker import process_audio_frame
        
        # Create sample audio data with incomplete frame
        sample_rate = 16000
        frame_duration_ms = 30
        n = int(sample_rate * frame_duration_ms / 1000) * 2
        audio_data = b'\x00' * (n * 2 + n // 2)  # 2.5 frames
        
        # Execute
        frames = list(process_audio_frame(audio_data, sample_rate, frame_duration_ms))
        
        # Verify - should only return complete frames
        self.assertEqual(len(frames), 2)
        
    @patch('Components.Speaker.cv2')
    @patch('Components.Speaker.extract_audio_from_video')
    @patch('Components.Speaker.wave.open')
    @patch('os.remove')
    def test_detect_faces_and_speakers_basic(self, mock_remove, mock_wave_open, 
                                             mock_extract, mock_cv2):
        """Test basic face and speaker detection"""
        from Components.Speaker import detect_faces_and_speakers, Frames
        
        # Clear Frames
        Frames.clear()
        
        # Setup mocks for wave file
        mock_wf = MagicMock()
        mock_wf.getframerate.return_value = 16000
        mock_wf.getnframes.return_value = 16000 * 2  # 2 seconds
        mock_wf.readframes.return_value = b'\x00' * (16000 * 2 * 2)
        mock_wave_open.return_value.__enter__.return_value = mock_wf
        
        # Setup video capture mocks
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [1920, 1080]  # width, height
        
        # Mock frame reading
        mock_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, mock_frame)] * 5 + [(False, None)]
        
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.VideoWriter_fourcc.return_value = 0
        
        # Mock DNN detections
        mock_net = MagicMock()
        detections = np.zeros((1, 1, 1, 7))
        detections[0, 0, 0] = [0, 0, 0.5, 0.3, 0.3, 0.5, 0.5]  # One face
        mock_net.forward.return_value = detections
        mock_cv2.dnn.readNetFromCaffe.return_value = mock_net
        
        mock_out = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_out
        
        # Execute
        detect_faces_and_speakers(self.test_video_path, self.test_output_path)
        
        # Verify
        mock_extract.assert_called_once()
        mock_cap.release.assert_called_once()
        mock_out.release.assert_called_once()
        mock_remove.assert_called_once_with(self.test_audio_path)
        self.assertGreater(len(Frames), 0)
        
    @patch('Components.Speaker.cv2')
    @patch('Components.Speaker.extract_audio_from_video')
    @patch('Components.Speaker.wave.open')
    @patch('os.remove')
    def test_detect_faces_and_speakers_multiple_faces(self, mock_remove, mock_wave_open,
                                                       mock_extract, mock_cv2):
        """Test detection with multiple faces"""
        from Components.Speaker import detect_faces_and_speakers, Frames
        
        # Clear Frames
        Frames.clear()
        
        # Setup mocks
        mock_wf = MagicMock()
        mock_wf.getframerate.return_value = 16000
        mock_wf.getnframes.return_value = 16000
        mock_wf.readframes.return_value = b'\x00' * (16000 * 2)
        mock_wave_open.return_value.__enter__.return_value = mock_wf
        
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [1920, 1080]
        
        mock_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, mock_frame)] * 3 + [(False, None)]
        
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.VideoWriter_fourcc.return_value = 0
        
        # Mock multiple face detections
        mock_net = MagicMock()
        detections = np.zeros((1, 1, 2, 7))  # 2 faces
        detections[0, 0, 0] = [0, 0, 0.5, 0.2, 0.2, 0.4, 0.4]
        detections[0, 0, 1] = [0, 0, 0.6, 0.5, 0.2, 0.7, 0.4]
        mock_net.forward.return_value = detections
        mock_cv2.dnn.readNetFromCaffe.return_value = mock_net
        
        mock_out = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_out
        
        # Execute
        detect_faces_and_speakers(self.test_video_path, self.test_output_path)
        
        # Verify
        self.assertGreater(len(Frames), 0)
        
    @patch('Components.Speaker.cv2')
    @patch('Components.Speaker.extract_audio_from_video')
    @patch('Components.Speaker.wave.open')
    @patch('os.remove')
    def test_detect_faces_and_speakers_no_faces(self, mock_remove, mock_wave_open,
                                                mock_extract, mock_cv2):
        """Test detection when no faces are found"""
        from Components.Speaker import detect_faces_and_speakers, Frames
        
        # Clear Frames
        Frames.clear()
        
        # Setup mocks
        mock_wf = MagicMock()
        mock_wf.getframerate.return_value = 16000
        mock_wf.getnframes.return_value = 16000
        mock_wf.readframes.return_value = b'\x00' * (16000 * 2)
        mock_wave_open.return_value.__enter__.return_value = mock_wf
        
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [1920, 1080]
        
        mock_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, mock_frame)] * 3 + [(False, None)]
        
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.VideoWriter_fourcc.return_value = 0
        
        # Mock no face detections
        mock_net = MagicMock()
        detections = np.zeros((1, 1, 1, 7))
        detections[0, 0, 0, 2] = 0.1  # Low confidence, below threshold
        mock_net.forward.return_value = detections
        mock_cv2.dnn.readNetFromCaffe.return_value = mock_net
        
        mock_out = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_out
        
        # Execute
        detect_faces_and_speakers(self.test_video_path, self.test_output_path)
        
        # Verify - Frames should contain None values
        self.assertGreater(len(Frames), 0)
        # First frame should be None when no face detected
        self.assertIsNone(Frames[0])
        
    @patch('Components.Speaker.cv2')
    @patch('Components.Speaker.extract_audio_from_video')
    @patch('Components.Speaker.wave.open')
    @patch('os.remove')
    def test_detect_faces_and_speakers_maintains_previous_frame(self, mock_remove, 
                                                                mock_wave_open,
                                                                mock_extract, mock_cv2):
        """Test that previous frame values are maintained when no face detected"""
        from Components.Speaker import detect_faces_and_speakers, Frames
        
        # Clear Frames
        Frames.clear()
        
        # Setup mocks
        mock_wf = MagicMock()
        mock_wf.getframerate.return_value = 16000
        mock_wf.getnframes.return_value = 16000
        mock_wf.readframes.return_value = b'\x00' * (16000 * 2)
        mock_wave_open.return_value.__enter__.return_value = mock_wf
        
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = [1920, 1080]
        
        mock_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, mock_frame)] * 4 + [(False, None)]
        
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.VideoWriter_fourcc.return_value = 0
        
        # Mock alternating face detections
        mock_net = MagicMock()
        detections_with_face = np.zeros((1, 1, 1, 7))
        detections_with_face[0, 0, 0] = [0, 0, 0.5, 0.3, 0.3, 0.5, 0.5]
        
        detections_no_face = np.zeros((1, 1, 1, 7))
        detections_no_face[0, 0, 0, 2] = 0.1  # Low confidence
        
        mock_net.forward.side_effect = [
            detections_with_face,
            detections_no_face,
            detections_no_face,
            detections_with_face
        ]
        mock_cv2.dnn.readNetFromCaffe.return_value = mock_net
        
        mock_out = MagicMock()
        mock_cv2.VideoWriter.return_value = mock_out
        
        # Execute
        detect_faces_and_speakers(self.test_video_path, self.test_output_path)
        
        # Verify - second and third frames should use previous valid values
        self.assertEqual(len(Frames), 4)
        self.assertIsNotNone(Frames[0])  # First frame has face
        self.assertIsNotNone(Frames[1])  # Uses previous frame
        self.assertEqual(Frames[1], Frames[0])  # Should be same as previous


if __name__ == '__main__':
    unittest.main()
