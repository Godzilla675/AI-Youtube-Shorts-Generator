"""
Tests for LanguageTasks.py
Tests highlight extraction from transcription using various AI models
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Components.LanguageTasks import GetHighlight, JSONResponse


class TestLanguageTasks(unittest.TestCase):
    """Test cases for language task functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_transcription = "0.0 - 10.0: Hello everyone, this is an amazing video about AI.\n10.0 - 30.0: In this section, we'll discuss the most interesting concepts.\n30.0 - 50.0: This is the climax of our presentation with key insights."
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.LanguageTasks.ChatGoogleGenerativeAI')
    @patch('Components.LanguageTasks.ChatPromptTemplate')
    def test_get_highlight_with_gemini_2_5_flash(self, mock_prompt_template, mock_gemini_ai):
        """Test highlight extraction with Gemini 2.5 Flash"""
        # Setup mocks
        mock_llm = MagicMock()
        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.start = 10.0
        mock_response.end = 30.0
        
        mock_gemini_ai.return_value = mock_llm
        mock_prompt = MagicMock()
        mock_prompt_template.from_messages.return_value = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_llm.with_structured_output.return_value = mock_llm
        mock_chain.invoke.return_value = mock_response
        
        # Execute
        start, end = GetHighlight(self.test_transcription, model="gemini-2.5-flash-002")
        
        # Verify
        self.assertEqual(start, 10)
        self.assertEqual(end, 30)
        mock_gemini_ai.assert_called_once()
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.LanguageTasks.ChatGoogleGenerativeAI')
    @patch('Components.LanguageTasks.ChatPromptTemplate')
    def test_get_highlight_with_gemini_2_5_pro(self, mock_prompt_template, mock_gemini_ai):
        """Test highlight extraction with Gemini 2.5 Pro"""
        # Setup mocks
        mock_llm = MagicMock()
        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.start = 15.0
        mock_response.end = 45.0
        
        mock_gemini_ai.return_value = mock_llm
        mock_prompt = MagicMock()
        mock_prompt_template.from_messages.return_value = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_llm.with_structured_output.return_value = mock_llm
        mock_chain.invoke.return_value = mock_response
        
        # Execute
        start, end = GetHighlight(self.test_transcription, model="gemini-2.5-pro-002")
        
        # Verify
        self.assertEqual(start, 15)
        self.assertEqual(end, 45)
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.LanguageTasks.ChatGoogleGenerativeAI')
    @patch('Components.LanguageTasks.ChatPromptTemplate')
    def test_get_highlight_with_gemini_1_5_flash(self, mock_prompt_template, mock_gemini_ai):
        """Test highlight extraction with Gemini 1.5 Flash"""
        # Setup mocks
        mock_llm = MagicMock()
        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.start = 20.0
        mock_response.end = 40.0
        
        mock_gemini_ai.return_value = mock_llm
        mock_prompt = MagicMock()
        mock_prompt_template.from_messages.return_value = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_llm.with_structured_output.return_value = mock_llm
        mock_chain.invoke.return_value = mock_response
        
        # Execute
        start, end = GetHighlight(self.test_transcription, model="gemini-1.5-flash")
        
        # Verify
        self.assertEqual(start, 20)
        self.assertEqual(end, 40)
        
    @patch.dict(os.environ, {'OPENAI_API': 'test_openai_key'})
    @patch('Components.LanguageTasks.ChatOpenAI')
    @patch('Components.LanguageTasks.ChatPromptTemplate')
    def test_get_highlight_with_gpt4o(self, mock_prompt_template, mock_openai):
        """Test highlight extraction with GPT-4o"""
        # Setup mocks
        mock_llm = MagicMock()
        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.start = 5.0
        mock_response.end = 35.0
        
        mock_openai.return_value = mock_llm
        mock_prompt = MagicMock()
        mock_prompt_template.from_messages.return_value = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_llm.with_structured_output.return_value = mock_llm
        mock_chain.invoke.return_value = mock_response
        
        # Execute
        start, end = GetHighlight(self.test_transcription, model="gpt-4o")
        
        # Verify
        self.assertEqual(start, 5)
        self.assertEqual(end, 35)
        mock_openai.assert_called_once()
        
    @patch.dict(os.environ, {}, clear=True)
    def test_get_highlight_missing_gemini_api_key(self):
        """Test error when Gemini API key is missing"""
        # Execute and verify
        with self.assertRaises(ValueError) as context:
            GetHighlight(self.test_transcription, model="gemini-2.5-flash-002")
        
        self.assertIn("GEMINI_API", str(context.exception))
        
    @patch.dict(os.environ, {}, clear=True)
    def test_get_highlight_missing_openai_api_key(self):
        """Test error when OpenAI API key is missing"""
        # Execute and verify
        with self.assertRaises(ValueError) as context:
            GetHighlight(self.test_transcription, model="gpt-4o")
        
        self.assertIn("OPENAI_API", str(context.exception))
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.LanguageTasks.ChatGoogleGenerativeAI')
    @patch('Components.LanguageTasks.ChatPromptTemplate')
    @patch('builtins.input', return_value='n')
    def test_get_highlight_same_start_end(self, mock_input, mock_prompt_template, mock_gemini_ai):
        """Test handling when start and end times are the same"""
        # Setup mocks
        mock_llm = MagicMock()
        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.start = 10.0
        mock_response.end = 10.0  # Same as start
        
        mock_gemini_ai.return_value = mock_llm
        mock_prompt = MagicMock()
        mock_prompt_template.from_messages.return_value = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_llm.with_structured_output.return_value = mock_llm
        mock_chain.invoke.return_value = mock_response
        
        # Execute
        start, end = GetHighlight(self.test_transcription, model="gemini-2.5-flash-002")
        
        # Verify
        self.assertEqual(start, 10)
        self.assertEqual(end, 10)
        mock_input.assert_called_once()
        
    def test_json_response_model(self):
        """Test JSONResponse pydantic model"""
        # Create instance
        response = JSONResponse(
            start=10.5,
            content="Interesting highlight",
            end=30.7
        )
        
        # Verify
        self.assertEqual(response.start, 10.5)
        self.assertEqual(response.content, "Interesting highlight")
        self.assertEqual(response.end, 30.7)
        
    @patch.dict(os.environ, {'GEMINI_API': 'test_gemini_key'})
    @patch('Components.LanguageTasks.ChatGoogleGenerativeAI')
    @patch('Components.LanguageTasks.ChatPromptTemplate')
    def test_get_highlight_thinking_mode_enabled(self, mock_prompt_template, mock_gemini_ai):
        """Test that thinking mode is enabled for Gemini 2.5 models"""
        # Setup mocks
        mock_llm = MagicMock()
        mock_chain = MagicMock()
        mock_response = MagicMock()
        mock_response.start = 10.0
        mock_response.end = 30.0
        
        mock_gemini_ai.return_value = mock_llm
        mock_prompt = MagicMock()
        mock_prompt_template.from_messages.return_value = mock_prompt
        mock_prompt.__or__.return_value = mock_chain
        mock_llm.with_structured_output.return_value = mock_llm
        mock_chain.invoke.return_value = mock_response
        
        # Execute
        GetHighlight(self.test_transcription, model="gemini-2.5-flash-002")
        
        # Verify that thinking mode kwargs were passed
        call_args = mock_gemini_ai.call_args
        self.assertIsNotNone(call_args)
        # Check if thinking or max_output_tokens is in kwargs
        kwargs = call_args[1] if len(call_args) > 1 else call_args.kwargs
        # Thinking mode is enabled for 2.5 models
        self.assertTrue('max_output_tokens' in kwargs or 'thinking' in kwargs)


if __name__ == '__main__':
    unittest.main()
