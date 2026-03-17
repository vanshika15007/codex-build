import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const quickPrompts = [
  "Plan a 3-day study schedule",
  "Give me tips to stay productive",
  "Tell me a fun science fact",
  "What courses do you offer?",
];

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([
    {
      sender: "Bot",
      text: "Hey! I’m Nova 🤖 — your all-purpose chatbot. I can help with study support, ideas, coding, general chats, and mini-games.",
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);
  const [typing, setTyping] = useState(false);
  const [error, setError] = useState("");
  const [game, setGame] = useState({ active: false, number: null, turns: 0 });
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, typing]);

  const pushMessage = (sender, text) => {
    setChat((prev) => [
      ...prev,
      {
        sender,
        text,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);
  };

  const startGuessGame = () => {
    const target = Math.floor(Math.random() * 20) + 1;
    setGame({ active: true, number: target, turns: 0 });
    pushMessage(
      "Bot",
      "🎮 Guess game started! I picked a number between 1 and 20. Type a number."
    );
  };

  const stopGuessGame = () => {
    setGame({ active: false, number: null, turns: 0 });
    pushMessage("Bot", "Game ended. Want to play again? Tap Start Game.");
  };

  const handleGameTurn = (rawMessage) => {
    const guess = Number(rawMessage);
    if (Number.isNaN(guess)) {
      pushMessage("Bot", "Please enter a valid number between 1 and 20.");
      return true;
    }

    const nextTurns = game.turns + 1;
    setGame((prev) => ({ ...prev, turns: nextTurns }));

    if (guess === game.number) {
      pushMessage("Bot", `🔥 Correct! You guessed it in ${nextTurns} tries.`);
      setGame({ active: false, number: null, turns: 0 });
      return true;
    }

    pushMessage(
      "Bot",
      guess < game.number
        ? "Too low ⬇️ Try again."
        : "Too high ⬆️ Try again."
    );
    return true;
  };

  const sendMessage = async (forcedMessage) => {
    const messageToSend = (forcedMessage ?? message).trim();
    if (!messageToSend || typing) return;
    pushMessage("You", messageToSend);
    setMessage("");

    setError("");

    if (game.active) {
      handleGameTurn(messageToSend);
      return;
    }

    setTyping(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        text: messageToSend,
      });

      const botReply =
        response?.data?.response || "I couldn't generate a response.";
      pushMessage("Bot", botReply);
    } catch {
      setError(
        "Could not reach backend. Please check if FastAPI server is running."
      );
      setTyping(false); // FIXED
    } finally {
      setTyping(false);
    }
  };

  const clearChat = () => {
    setChat((prev) => prev.slice(0, 1));
    setError("");
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <div className="chat-title-wrap">
          <h2 className="chat-title">✨ Nova Chat Studio</h2>
          <p className="subtitle">
            General AI assistant + student helper + mini games
          </p>
        </div>

        {error && <div className="error-banner">{error}</div>}

        <div className="toolbar">
          <button
            className="prompt-chip"
            onClick={startGuessGame}
            disabled={typing || game.active}
          >
            Start Guess Game
          </button>
          <button
            className="prompt-chip"
            onClick={stopGuessGame}
            disabled={!game.active}
          >
            End Game
          </button>
          <button
            className="prompt-chip"
            onClick={clearChat}
            disabled={typing || chat.length <= 1}
          >
            Clear Chat
          </button>
        </div>

        <div className="quick-prompts">
          {quickPrompts.map((prompt) => (
            <button
              key={prompt}
              className="prompt-chip ghost"
              onClick={() => sendMessage(prompt)}
              disabled={typing}
            >
              {prompt}
            </button>
          ))}
        </div>

        <div className="chat-box">
          {chat.map((msg, index) => (
            <div
              key={`${msg.sender}-${index}`}
              className={`message-row ${
                msg.sender === "You" ? "row-user" : "row-bot"
              }`}
            >
              {/* ✅ ADDED MESSAGE CONTENT (NO DELETION) */}
              <div className="message-bubble">
                <span className="message-text">{msg.text}</span>
                <span className="message-time">{msg.time}</span>
              </div>
            </div>
          ))}

          {typing && <div className="typing">Nova is thinking...</div>}
          <div ref={chatEndRef} />
        </div>

        <div className="input-area">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={
              game.active ? "Enter your guess (1-20)" : "Ask anything..."
            }
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            disabled={typing}
          />
          <button
            onClick={() => sendMessage()}
            disabled={typing || !message.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;