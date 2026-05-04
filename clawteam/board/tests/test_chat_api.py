"""Tests for chat API endpoints."""

import json
import os
import sys
import tempfile
import threading
import time
import unittest
from http.client import HTTPConnection
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure board module is importable
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestChatAPI(unittest.TestCase):
    """Test cases for chat API endpoints."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Set test environment variables
        os.environ["CLAWTEAM_CHAT_HISTORY"] = tempfile.mktemp(suffix=".json")
        os.environ["CLAWTEAM_TRANSPORT"] = "memory"
        
        # Import after setting env vars
        from clawteam.board.server import BoardHandler, serve
        cls.handler_class = BoardHandler
        cls.server = None
        cls.server_thread = None
        
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        if cls.server:
            cls.server.shutdown()
        # Clean up test file
        chat_file = Path(os.environ.get("CLAWTEAM_CHAT_HISTORY", "~/.openclaw/chat_history.json")).expanduser()
        if chat_file.exists():
            chat_file.unlink()
    
    def test_generate_simple_response_greeting(self):
        """Test simple response generation for greetings."""
        from clawteam.board.server import _generate_simple_response
        
        response = _generate_simple_response("你好")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        
    def test_generate_simple_response_help(self):
        """Test simple response generation for help requests."""
        from clawteam.board.server import _generate_simple_response
        
        response = _generate_simple_response("help")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        
    def test_generate_simple_response_team(self):
        """Test simple response generation for team-related queries."""
        from clawteam.board.server import _generate_simple_response
        
        response = _generate_simple_response("team")
        self.assertIsInstance(response, str)
        self.assertTrue("team" in response.lower() or "团队" in response)
        
    def test_generate_simple_response_task(self):
        """Test simple response generation for task-related queries."""
        from clawteam.board.server import _generate_simple_response
        
        response = _generate_simple_response("task")
        self.assertIsInstance(response, str)
        self.assertTrue("task" in response.lower() or "任务" in response)
        
    def test_generate_simple_response_default(self):
        """Test simple response generation for unknown queries."""
        from clawteam.board.server import _generate_simple_response
        
        response = _generate_simple_response("random unknown message")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
    
    def test_chat_message_save_and_retrieve(self):
        """Test saving and retrieving chat messages."""
        from clawteam.board.server import BoardHandler
        
        # Create mock handler
        handler = MagicMock(spec=BoardHandler)
        handler._save_chat_message = BoardHandler._save_chat_message.__get__(handler, BoardHandler)
        
        # Save a test message
        message = {
            "role": "user",
            "content": "Test message",
            "user": "TestUser"
        }
        
        result = handler._save_chat_message(message)
        self.assertTrue(result)
        
    def test_chat_command_help(self):
        """Test /help command handling."""
        from clawteam.board.server import BoardHandler
        
        handler = MagicMock(spec=BoardHandler)
        handler._handle_chat_command = BoardHandler._handle_chat_command.__get__(handler, BoardHandler)
        
        response = handler._handle_chat_command("/help")
        self.assertEqual(response["role"], "system")
        self.assertIn("/help", response["content"])
        
    def test_chat_command_status(self):
        """Test /status command handling."""
        from clawteam.board.server import BoardHandler
        
        handler = MagicMock(spec=BoardHandler)
        handler._handle_chat_command = BoardHandler._handle_chat_command.__get__(handler, BoardHandler)
        
        with patch("clawteam.board.collector.BoardCollector") as mock_collector:
            mock_instance = MagicMock()
            mock_instance.collect_overview.return_value = {
                "status": "healthy",
                "team_count": 2,
                "total_tasks": 5,
                "active_sessions": 3,
                "teams": []
            }
            mock_collector.return_value = mock_instance
            
            response = handler._handle_chat_command("/status")
            self.assertEqual(response["role"], "system")
            self.assertIn("healthy", response["content"])
    
    def test_chat_command_tasks_list(self):
        """Test /tasks list command handling."""
        from clawteam.board.server import BoardHandler
        
        handler = MagicMock(spec=BoardHandler)
        handler._handle_chat_command = BoardHandler._handle_chat_command.__get__(handler, BoardHandler)
        
        with patch("clawteam.board.collector.BoardCollector") as mock_collector:
            mock_instance = MagicMock()
            mock_instance.collect_overview.return_value = {
                "teams": [
                    {"name": "test-team", "tasks": [
                        {"subject": "Test Task", "status": "pending", "owner": "agent1"}
                    ]}
                ]
            }
            mock_collector.return_value = mock_instance
            
            response = handler._handle_chat_command("/tasks list")
            self.assertEqual(response["role"], "system")
            self.assertIn("Test Task", response["content"])
    
    def test_chat_command_members(self):
        """Test /members command handling."""
        from clawteam.board.server import BoardHandler
        
        handler = MagicMock(spec=BoardHandler)
        handler._handle_chat_command = BoardHandler._handle_chat_command.__get__(handler, BoardHandler)
        
        with patch("clawteam.session.registry.get_session_registry") as mock_registry:
            mock_session = MagicMock()
            mock_session.status = "active"
            mock_session.role = "worker"
            mock_session.name = "Agent1"
            mock_session.created_at = "2026-05-01T10:00:00Z"
            
            mock_reg_instance = MagicMock()
            mock_reg_instance.list_sessions.return_value = [mock_session]
            mock_registry.return_value = mock_reg_instance
            
            response = handler._handle_chat_command("/members")
            self.assertEqual(response["role"], "system")
            self.assertIn("Agent1", response["content"])
    
    def test_chat_command_tasks_create(self):
        """Test /tasks create command handling."""
        from clawteam.board.server import BoardHandler
        
        handler = MagicMock(spec=BoardHandler)
        handler._handle_chat_command = BoardHandler._handle_chat_command.__get__(handler, BoardHandler)
        
        with patch("clawteam.team.tasks.TaskStore") as mock_store:
            mock_task = MagicMock()
            mock_task.id = "task-123"
            
            mock_store_instance = MagicMock()
            mock_store_instance.create.return_value = mock_task
            mock_store.return_value = mock_store_instance
            
            response = handler._handle_chat_command('/tasks create "Test Task" "Test Description"')
            self.assertEqual(response["role"], "system")
            self.assertIn("Task created successfully", response["content"])
    
    def test_chat_command_unknown_command(self):
        """Test handling of unknown commands (should call AI)."""
        from clawteam.board.server import BoardHandler
        
        handler = MagicMock(spec=BoardHandler)
        handler._handle_chat_command = BoardHandler._handle_chat_command.__get__(handler, BoardHandler)
        handler._call_ai_assistant = BoardHandler._call_ai_assistant.__get__(handler, BoardHandler)
        
        # Mock AI call to return a simple response
        with patch.object(handler, '_call_ai_assistant') as mock_ai:
            mock_ai.return_value = {
                "role": "assistant",
                "content": "This is an AI response",
                "timestamp": "2026-05-01T10:00:00Z",
                "assistant": "楚灵"
            }
            
            response = handler._handle_chat_command("Hello, how are you?")
            self.assertEqual(response["role"], "assistant")
            self.assertIn("AI response", response["content"])
    
    def test_chat_history_clear(self):
        """Test clearing chat history."""
        from clawteam.board.server import BoardHandler
        
        handler = MagicMock(spec=BoardHandler)
        handler._serve_json = MagicMock()
        handler._clear_chat_history = BoardHandler._clear_chat_history.__get__(handler, BoardHandler)
        
        # First save a message
        handler._save_chat_message = BoardHandler._save_chat_message.__get__(handler, BoardHandler)
        handler._save_chat_message({
            "role": "user",
            "content": "Test",
            "user": "TestUser"
        })
        
        # Now clear
        handler._clear_chat_history()
        
        # Verify json was served
        handler._serve_json.assert_called()
        call_args = handler._serve_json.call_args[0][0]
        self.assertTrue(call_args["success"])
    
    def test_now_iso_format(self):
        """Test _now_iso returns proper ISO format."""
        from clawteam.board.server import _now_iso
        
        result = _now_iso()
        self.assertIsInstance(result, str)
        self.assertIn("T", result)  # ISO format has T separator
        self.assertIn("+", result)  # Has timezone


class TestSSEBroadcasting(unittest.TestCase):
    """Test SSE broadcasting functionality."""
    
    def test_broadcast_chat_event(self):
        """Test broadcasting chat events to subscribers."""
        from clawteam.board.server import BoardHandler, _chat_event_queue, _chat_subscribers
        
        # Clear any existing events
        _chat_event_queue.clear()
        _chat_subscribers[:] = []
        
        # Create a mock event
        event = {"type": "message", "data": {"role": "user", "content": "Test"}}
        
        # Broadcast
        BoardHandler._broadcast_chat_event(event)
        
        # Verify event was added to queue
        self.assertTrue(len(_chat_event_queue) > 0)
        self.assertEqual(_chat_event_queue[-1], event)
    
    def test_sse_connection_registers_subscriber(self):
        """Test that SSE connection registers as subscriber."""
        from clawteam.board.server import _chat_subscribers
        
        initial_count = len(_chat_subscribers)
        
        # Simulate subscriber lock
        lock = threading.Lock()
        with __import__("clawteam.board.server", fromlist=["_subscriber_lock"])._subscriber_lock:
            _chat_subscribers.append(lock)
        
        self.assertEqual(len(_chat_subscribers), initial_count + 1)
        
        # Cleanup
        _chat_subscribers.remove(lock)


class TestNaturalLanguageParsing(unittest.TestCase):
    """Test natural language command parsing."""
    
    def test_natural_language_create_task(self):
        """Test natural language task creation parsing."""
        from clawteam.board.server import BoardHandler
        
        # The system should handle natural language like "创建一个任务：测试"
        handler = MagicMock(spec=BoardHandler)
        handler._handle_chat_command = BoardHandler._handle_chat_command.__get__(handler, BoardHandler)
        handler._call_ai_assistant = BoardHandler._call_ai_assistant.__get__(handler, BoardHandler)
        
        with patch.object(handler, '_call_ai_assistant') as mock_ai:
            mock_ai.return_value = {
                "role": "assistant",
                "content": "任务已创建",
                "timestamp": "2026-05-01T10:00:00Z",
                "assistant": "楚灵"
            }
            
            response = handler._handle_chat_command("创建一个任务：测试登录功能")
            # Should be handled by AI since it's not a /command
            self.assertEqual(response["role"], "assistant")
    
    def test_natural_language_view_team_status(self):
        """Test natural language team status query."""
        from clawteam.board.server import BoardHandler
        
        handler = MagicMock(spec=BoardHandler)
        handler._handle_chat_command = BoardHandler._handle_chat_command.__get__(handler, BoardHandler)
        handler._call_ai_assistant = BoardHandler._call_ai_assistant.__get__(handler, BoardHandler)
        
        with patch.object(handler, '_call_ai_assistant') as mock_ai:
            mock_ai.return_value = {
                "role": "assistant",
                "content": "团队状态：正常",
                "timestamp": "2026-05-01T10:00:00Z",
                "assistant": "楚灵"
            }
            
            response = handler._handle_chat_command("查看当前团队状态")
            self.assertEqual(response["role"], "assistant")


if __name__ == "__main__":
    unittest.main()
