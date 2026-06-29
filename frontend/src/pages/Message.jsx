import React, { useState } from "react";

const Message = ({ message }) => {
  const isUser = message.from === "user";

  const [showSources, setShowSources] = useState(false);

  return (
    <div
      className={`chat-message ${
        isUser ? "chat-message-user" : "chat-message-bot"
      }`}
    >
      {/* Avatar */}
      <div className="chat-avatar">
        {isUser ? (
          <div className="user-avatar">U</div>
        ) : (
          <div className="bot-avatar">✦</div>
        )}
      </div>

      {/* Message Bubble */}
      <div className="chat-content">

        <div
          className={`chat-bubble ${
            isUser ? "user-bubble" : "bot-bubble"
          }`}
        >
          {message.text}
        </div>

        <div className="message-time">
          {message.time}
        </div>

        {/* SOURCES */}

        {!isUser &&
          message.sources &&
          message.sources.length > 0 && (
            <div className="sources-container">

              <button
                className="sources-btn"
                onClick={() =>
                  setShowSources(!showSources)
                }
              >
                {showSources
                  ? "▼ Hide Sources"
                  : "▶ Show Sources"}
              </button>

              {showSources && (
                <ul className="sources-list">
                  {message.sources.map(
                    (source, index) => (
                      <li key={index}>
  {typeof source === "string"
    ? source
    : JSON.stringify(source)}
</li>
                    )
                  )}
                </ul>
              )}
            </div>
          )}

      </div>

    </div>
  );
};

export default Message;
