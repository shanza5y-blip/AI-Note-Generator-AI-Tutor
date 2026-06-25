import React, { useEffect, useRef, useState } from "react";
import Message from "../pages/Message";
import {
  HISTORY,
  INITIAL_MESSAGES,
  BOT_REPLIES,
  QUICK_REPLIES,
} from "../data/chatData";

const TutorChatPage = ({ onOpenNoteViewer }) => {
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [typing, setTyping] = useState(false);

  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop =
        scrollRef.current.scrollHeight;
    }
  }, [messages, typing]);

  const getCurrentTime = () => {
    return new Date().toLocaleTimeString([], {
      hour: "numeric",
      minute: "2-digit",
    });
  };

  const sendMessage = (text) => {
    const message = (text || input).trim();

    if (!message) return;

    setMessages((prev) => [
      ...prev,
      {
        from: "user",
        text: message,
        time: getCurrentTime(),
      },
    ]);

    setInput("");
    setTyping(true);

    setTimeout(() => {
      const randomReply =
        BOT_REPLIES[
          Math.floor(
            Math.random() * BOT_REPLIES.length
          )
        ];

      setTyping(false);

      setMessages((prev) => [
        ...prev,
        {
          from: "bot",
          text: randomReply,
          time: getCurrentTime(),
        },
      ]);
    }, 1200);
  };

  return (
    <div className="tutor-page">
      {/* =========================
          SIDEBAR
      ========================= */}

      <div
        className={`tutor-sidebar ${
          sidebarOpen ? "open" : "closed"
        }`}
      >
        {/* Logo */}

        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="logo-box">✦</div>
            <span>NoteAI</span>
          </div>

          <button
            className="new-chat-btn"
            onClick={() =>
              setMessages(INITIAL_MESSAGES)
            }
          >
            + New Chat
          </button>
        </div>

        {/* Search */}

        <div className="sidebar-search">
          <input
            type="text"
            placeholder="Search chats..."
          />
        </div>

        {/* History */}

        <div className="sidebar-history">
          {Object.entries(HISTORY).map(
            ([section, items]) => (
              <div
                key={section}
                className="history-section"
              >
                <h4>{section}</h4>

                {items.map((chat) => (
                  <button
                    key={chat.id}
                    className={`history-item ${
                      chat.active
                        ? "active"
                        : ""
                    }`}
                  >
                    <div className="history-title">
                      {chat.title}
                    </div>

                    <div className="history-preview">
                      {chat.preview}
                    </div>
                  </button>
                ))}
              </div>
            )
          )}
        </div>

        {/* Profile */}

        <div className="sidebar-profile">
          <div className="profile-avatar">
            U
          </div>

          <div className="profile-info">
            <h5>Student</h5>
            <p>Free Plan</p>
          </div>
        </div>
      </div>

      {/* =========================
          MAIN CHAT AREA
      ========================= */}

      <div className="chat-main">
        {/* Header */}

        <div className="chat-header">
          <button
            className="menu-btn"
            onClick={() =>
              setSidebarOpen(!sidebarOpen)
            }
          >
            ☰
          </button>

          <div className="chat-header-info">
            <div className="chat-bot-icon">
              ✦
            </div>

            <div>
              <h3>NoteAI Tutor</h3>
              <p>Online • Ready to help</p>
            </div>
          </div>

          <div className="chat-header-actions">
            <button
              className="save-notes-btn"
              onClick={() => {
                if (onOpenNoteViewer) {
                  onOpenNoteViewer();
                }
              }}
            >
              Save as Notes
            </button>
          </div>
        </div>

        {/* Messages */}

        <div
          className="chat-messages"
          ref={scrollRef}
        >
          {messages.map(
            (message, index) => (
              <Message
                key={index}
                message={message}
              />
            )
          )}

          {/* Typing */}

          {typing && (
            <div className="chat-message">
              <div className="chat-avatar">
                <div className="bot-avatar">
                  ✦
                </div>
              </div>

              <div className="typing-bubble">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            </div>
          )}
        </div>

        {/* Quick Replies */}

        <div className="quick-replies">
          {QUICK_REPLIES.map((reply) => (
            <button
              key={reply}
              className="quick-reply-btn"
              onClick={() =>
                sendMessage(reply)
              }
            >
              {reply}
            </button>
          ))}
        </div>

        {/* Input */}

        <div className="chat-input-container">
          <div className="chat-input-box">
            <textarea
              value={input}
              onChange={(e) =>
                setInput(e.target.value)
              }
              placeholder="Ask your tutor anything..."
              rows="1"
              className="chat-input"
              onKeyDown={(e) => {
                if (
                  e.key === "Enter" &&
                  !e.shiftKey
                ) {
                  e.preventDefault();
                  sendMessage();
                }
              }}
            />

            <button
              className="send-btn"
              onClick={() =>
                sendMessage()
              }
              disabled={!input.trim()}
            >
              ➤
            </button>
          </div>

          <p className="chat-footer-text">
            NoteAI Tutor can make mistakes.
            Verify important information.
          </p>
        </div>
      </div>
    </div>
  );
};

export default TutorChatPage;