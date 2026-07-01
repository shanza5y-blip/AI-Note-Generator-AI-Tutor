import React, { useEffect, useRef, useState } from "react";
import Message from "./Message";
import { QUICK_REPLIES } from "../data/chatData";

const TutorChatPage = ({
  fileId,
  selectedSubject,
  onOpenNotes,
}) => {

  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [typing, setTyping] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop =
        scrollRef.current.scrollHeight;
    }
  }, [messages, typing]);

  useEffect(() => {
    localStorage.setItem(
      "noteai_chat_history",
      JSON.stringify(chatHistory)
    );
  }, [chatHistory]);

  useEffect(() => {
    const saved = localStorage.getItem(
      "noteai_chat_history"
    );

    if (saved) {
      setChatHistory(JSON.parse(saved));
    }
  }, []);

  const getCurrentTime = () =>
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  const loadConversation = (chat) => {
    setMessages(chat.messages);

    setChatHistory((prev) =>
      prev.map((c) => ({
        ...c,
        active: c.id === chat.id,
      }))
    );
  };

  const startNewChat = () => {
    if (messages.length > 0) {

      const firstQuestion =
        messages.find(
          (m) => m.from === "user"
        );

      setChatHistory((prev) => [
        {
          id: Date.now(),
          title:
            firstQuestion?.text || "New Chat",
          preview:
            messages[messages.length - 1]
              ?.text.slice(0, 60) + "...",
          messages: [...messages],
          active: true,
        },
        ...prev,
      ]);
    }

    setMessages([]);
    setInput("");
    setError("");
  };

  const clearHistory = () => {
    if (
      window.confirm(
        "Delete all chat history?"
      )
    ) {
      setChatHistory([]);
      localStorage.removeItem(
        "noteai_chat_history"
      );
    }
  };

  const sendMessage = async (
    customMessage = ""
  ) => {

    if (!fileId) {
      alert(
        "Please upload a syllabus first."
      );
      return;
    }

    const question =
      (customMessage || input).trim();

    if (!question) return;

    const userMessage = {
      from: "user",
      text: question,
      time: getCurrentTime(),
    };

    const updatedMessages = [
      ...messages,
      userMessage,
    ];

    setMessages(updatedMessages);

    setInput("");
    setTyping(true);
    setLoading(true);
    setError("");

    try {

      console.log({
        file_id: fileId,
        subject:
          selectedSubject?.name ||
          "Uploaded Subject",
        message: question,
      });

      const response = await fetch(
        "http://localhost:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            file_id: fileId,

            subject:
              selectedSubject?.name ||
              "Uploaded Subject",

            message: question,

            history: updatedMessages.map((msg) => ({
              role: msg.from === "user"
                ? "user"
                : "assistant",

              content: msg.text,
            })),
          }),
        }
      );

      let data = {};

      try {
        data = await response.json();
      } catch {
        data = {};
      }

      if (!response.ok) {
        throw new Error(
          JSON.stringify(data)
        );
      }

      const botMessage = {
        from: "bot",
        text: data.answer,
        time: getCurrentTime(),
        sources: data.sources || [],
      };

      const finalMessages = [...updatedMessages, botMessage];

      setMessages(finalMessages);

      setChatHistory((prev) => {
        const activeChat = prev.find((chat) => chat.active);

        if (activeChat) {
          return prev.map((chat) =>
            chat.active
              ? {
                ...chat,
                messages: finalMessages,
                preview: botMessage.text.slice(0, 60) + "...",
              }
              : chat
          );
        }

        const firstQuestion = finalMessages.find(
          (m) => m.from === "user"
        );

        return [
          {
            id: Date.now(),
            title: firstQuestion?.text || "New Chat",
            preview: botMessage.text.slice(0, 60) + "...",
            messages: finalMessages,
            active: true,
          },
          ...prev,
        ];
      });

    } catch (err) {

      console.error(err);

      setError(
        "Unable to reach the AI Tutor."
      );

      setMessages((prev) => [
        ...prev,
        {
          from: "bot",
          text: "Unable to reach the AI Tutor.",
          time: getCurrentTime(),
        },
      ]);

    } finally {

      setTyping(false);
      setLoading(false);

    }
  };

  return (

    <div className="tutor-page">

      <div
        className={`tutor-sidebar ${sidebarOpen
            ? "open"
            : "closed"
          }`}
      >

        <div className="sidebar-header">

          <div className="sidebar-logo">
            <div className="logo-box">
              ✦
            </div>

            <span>NoteAI</span>
          </div>

          <button
            className="new-chat-btn"
            onClick={startNewChat}
          >
            + New Chat
          </button>

          <button
            className="clear-history-btn"
            onClick={clearHistory}
          >
            🗑 Clear History
          </button>

        </div>

        <div className="sidebar-history">

          {chatHistory.length === 0 ? (

            <p
              style={{
                padding: 20,
                color: "#777",
              }}
            >
              No conversations yet
            </p>

          ) : (

            chatHistory.map((chat) => (

              <button
                key={chat.id}
                className={`history-item ${chat.active
                    ? "active"
                    : ""
                  }`}
                onClick={() =>
                  loadConversation(chat)
                }
              >

                <div className="history-title">
                  {chat.title}
                </div>

                <div className="history-preview">
                  {chat.preview}
                </div>

              </button>

            ))

          )}

        </div>

      </div>

      <div className="chat-main">

        <div className="chat-header">

          <button
            className="menu-btn"
            onClick={() =>
              setSidebarOpen(
                !sidebarOpen
              )
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
            </div>

          </div>

          <button
            className="save-notes-btn"
            onClick={onOpenNotes}
          >
            Save as Notes
          </button>

        </div>

        {error && (
          <div className="error-box">
            {error}
          </div>
        )}

        <div
          className="chat-messages"
          ref={scrollRef}
        >

          {messages.length === 0 ? (

            <div
              style={{
                textAlign: "center",
                marginTop: 80,
              }}
            >
              <h2>
                Welcome to NoteAI Tutor 👋
              </h2>

              <p>
                Ask anything about your uploaded syllabus.
              </p>
            </div>

          ) : (

            messages.map((message, index) => (
              <Message
                key={index}
                message={message}
              />
            ))

          )}

          {typing && (
            <div className="typing-bubble">
              Thinking...
            </div>
          )}

        </div>

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

        <div className="chat-input-container">

          <div className="chat-input-box">

            <textarea
              className="chat-input"
              value={input}
              rows={1}
              placeholder="Ask anything..."
              onChange={(e) =>
                setInput(e.target.value)
              }
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
              disabled={
                loading ||
                !input.trim()
              }
              onClick={() =>
                sendMessage()
              }
            >
              {loading
                ? "..."
                : "➤"}
            </button>

          </div>

        </div>

      </div>

    </div>

  );
};

export default TutorChatPage;