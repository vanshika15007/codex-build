import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const quickPrompts = [
  "Build a 1-week study plan for physics",
  "Give me 5 real-world math applications",
  "Explain climate change with actionable solutions",
  "Prepare me for an interview case study",
];

const studyVideos = [
  {
    title: "Khan Academy - Study & Practice Library",
    topic: "Math, science, economics",
    url: "https://www.khanacademy.org/",
  },
  {
    title: "MIT OpenCourseWare",
    topic: "University-level engineering and science",
    url: "https://ocw.mit.edu/",
  },
  {
    title: "CrashCourse",
    topic: "High-quality concept videos",
    url: "https://www.youtube.com/@crashcourse",
  },
  {
    title: "TED-Ed",
    topic: "Real-world ideas and critical thinking",
    url: "https://www.youtube.com/@TEDEd",
  },
];

const scenarioChallenges = [
  {
    prompt:
      "🏥 Scenario 1: A city hospital has long patient wait times. Which first step is most professional? (A) Buy new software immediately (B) Collect data on patient flow and bottlenecks (C) Hire more staff without analysis)",
    answer: "b",
    feedback:
      "Excellent approach. Strong decisions start with measurable evidence and root-cause analysis.",
  },
  {
    prompt:
      "🌱 Scenario 2: A school wants to reduce plastic waste. What should come first? (A) Awareness campaign + baseline audit (B) Ban all plastics tomorrow (C) Ignore cost and logistics)",
    answer: "a",
    feedback:
      "Correct. A baseline audit and communication plan make sustainability changes realistic and scalable.",
  },
  {
    prompt:
      "📊 Scenario 3: Exam scores dropped across classes. Best first action? (A) Blame students (B) Review assessment quality and study habits data (C) Increase homework volume only)",
    answer: "b",
    feedback:
      "Great. Reviewing data and assessment quality helps you solve the right problem, not just symptoms.",
  },
];

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([
    {
      sender: "Bot",
      text: "Welcome to Nova Professional Learning Assistant. I can help with study plans, real-world problem solving, interview-style scenarios, and AI support via Gemini.",
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);
  const [typing, setTyping] = useState(false);
  const [error, setError] = useState("");
  const [challenge, setChallenge] = useState({ active: false, index: 0, score: 0 });
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

  const startScenarioGame = () => {
    setChallenge({ active: true, index: 0, score: 0 });
    pushMessage(
      "Bot",
      "🎯 Professional Scenario Challenge started. Reply with A, B, or C."
    );
  };

  const stopScenarioGame = () => {
    setChallenge({ active: false, index: 0, score: 0 });
    pushMessage("Bot", "Scenario challenge ended. You can restart anytime.");
  };

  const handleScenarioTurn = (rawMessage) => {
    const answer = rawMessage.trim().toLowerCase();
    if (!["a", "b", "c"].includes(answer)) {
      pushMessage("Bot", "Please answer using A, B, or C.");
      return;
    }

    const current = scenarioChallenges[challenge.index];
    const isCorrect = answer === current.answer;
    const nextScore = isCorrect ? challenge.score + 1 : challenge.score;

    pushMessage(
      "Bot",
      isCorrect
        ? `✅ Correct. ${current.feedback}`
        : `❌ Not the best choice this time. ${current.feedback}`
    );
    const nextIndex = challenge.index + 1;
    if (nextIndex >= scenarioChallenges.length) {
      pushMessage(
        "Bot",
        `Challenge complete. Final score: ${nextScore}/${scenarioChallenges.length}. Strong professional thinking practice!`
      );
      setChallenge({ active: false, index: 0, score: 0 });
      return;
    }

    setChallenge({ active: true, index: nextIndex, score: nextScore });
    pushMessage("Bot", scenarioChallenges[nextIndex].prompt);
  };

  const sendMessage = async (forcedMessage) => {
    const messageToSend = (forcedMessage ?? message).trim();
    if (!messageToSend || typing) return;
    pushMessage("You", messageToSend);
    setMessage("");

    setError("");

    if (challenge.active) {
      handleScenarioTurn(messageToSend);
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
          <h2 className="chat-title">Nova Professional Study Copilot</h2>
          <p className="subtitle">
            Real-world learning • Professional scenarios • Study-focused AI
          </p>
        </div>
        <div className="learning-hub">
          <div className="hub-card">
            <h3>Professional Scenario Game</h3>
            <p>Practice decision-making with realistic case situations.</p>
            <div className="toolbar">
              <button
                className="prompt-chip"
                onClick={startScenarioGame}
                disabled={typing || challenge.active}
              >
                Start Challenge
              </button>
              <button
                className="prompt-chip"
                onClick={stopScenarioGame}
                disabled={!challenge.active}
              >
                End Challenge
              </button>
            </div>
          </div>

          <div className="hub-card">
            <h3>Recommended Study Videos</h3>
            <ul className="video-list">
              {studyVideos.map((video) => (
                <li key={video.title}>
                  <a href={video.url} target="_blank" rel="noreferrer">
                    {video.title}
                  </a>
                  <span>{video.topic}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {error && <div className="error-banner">{error}</div>}

        <div className="toolbar toolbar-bottom">
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
              className={`message-row ${msg.sender === "You" ? "row-user" : "row-bot"}`}
            >
              {/* ✅ ADDED MESSAGE CONTENT (NO DELETION) */}
              <div className="message-bubble">
                <span className="message-text">{msg.text}</span>
                <span className="message-time">{msg.time}</span>
              </div>
            </div>
          ))}

          {typing && <div className="typing">Nova is preparing a response...</div>}
          <div ref={chatEndRef} />
        </div>

        <div className="input-area">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={challenge.active ? "Answer with A, B, or C" : "Ask about study plans, real-world problems, or concepts..."}
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