import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Bot, User, Send, Plus, LogOut, CheckSquare, MessageSquare, TerminalSquare } from 'lucide-react';

// Mock UI data for multi-agents
const AGENTS = [
  { id: 'general', name: 'General Assistant', icon: <MessageSquare size={16} /> },
  { id: 'coder', name: 'Software Dev Team', icon: <TerminalSquare size={16} /> },
  { id: 'red_team', name: 'Red Teaming Bot', icon: <CheckSquare size={16} /> },
];

// Mock database for Chat History
const MOCK_HISTORY = [
  { id: '1', title: 'Python Web Scraping', date: 'Today' },
  { id: '2', title: 'React Performance Tips', date: 'Yesterday' },
  { id: '3', title: 'SQL Database Design', date: 'Last Week' },
];

// Main App Component
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  
  if (!isLoggedIn) {
    return <LoginScreen onLogin={(user) => { setUsername(user); setIsLoggedIn(true); }} />;
  }

  return <ChatApp username={username} onLogout={() => setIsLoggedIn(false)} />;
}

// 4. Authentication (Login System) Component
function LoginScreen({ onLogin }: { onLogin: (name: string) => void }) {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) onLogin(name);
  };

  return (
    <div className="login-container">
      <div className="login-card glass">
        <div className="login-header">
          <h1>Welcome Back</h1>
          <p>Login to access your AI Agents</p>
        </div>
        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="input-group">
            <label>Username</label>
            <input 
              type="text" 
              placeholder="Enter your username" 
              value={name} 
              onChange={(e) => setName(e.target.value)} 
              required 
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input 
              type="password" 
              placeholder="••••••••" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
            />
          </div>
          <button type="submit" className="btn-primary">
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}

// Main Chat Application Component
function ChatApp({ username, onLogout }: { username: string, onLogout: () => void }) {
  const [messages, setMessages] = useState<{role: 'user' | 'bot', content: string}[]>([]);
  const [input, setInput] = useState('');
  const [selectedAgent, setSelectedAgent] = useState(AGENTS[0].id);
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  // 1. Streaming response simulator
  const simulateStream = (fullText: string) => {
    setIsTyping(false);
    let currentText = '';
    const msgIndex = messages.length + 1; // Wait, actually it's easier to append a new empty message and update it
    
    setMessages(prev => [...prev, { role: 'bot', content: '' }]);
    
    // Simulate typing effect by streaming word by word or chunk by chunk
    let i = 0;
    const interval = setInterval(() => {
      currentText = fullText.slice(0, i + 5);
      i += 5;
      
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1].content = currentText;
        return newMessages;
      });

      if (i >= fullText.length) {
        clearInterval(interval);
      }
    }, 20);
  };

  const handleSend = () => {
    if (!input.trim()) return;
    
    const userMsg = input;
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setIsTyping(true);

    // Mock API call to backend
    setTimeout(() => {
      simulateStream(`Hello! I am the **${AGENTS.find(a => a.id === selectedAgent)?.name}**. I received your message:\n\n> ${userMsg} \n\nHere is a code block showing how I'm ready to help:\n\n\`\`\`python\nprint("Connecting to backend servers...")\n\`\`\``);
    }, 1500);
  };

  return (
    <div className="app-layout">
      {/* 5. Chat History Sidebar */}
      <aside className="sidebar glass">
        <div className="sidebar-header">
          <h2 style={{ fontSize: '1.25rem', margin: 0, background: 'var(--accent-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            MultiAgent
          </h2>
          <button className="btn-icon" title="Settings"><LogOut size={18} onClick={onLogout}/></button>
        </div>
        
        <button className="btn-primary new-chat-btn">
          <Plus size={18} /> New Chat
        </button>

        <div className="chat-history">
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', padding: '0.5rem 0.5rem', marginTop: '0.5rem' }}>HISTORY</div>
          {MOCK_HISTORY.map(chat => (
            <div key={chat.id} className="history-item">
              <MessageSquare size={16} />
              {chat.title}
            </div>
          ))}
        </div>

        <div className="user-profile">
          <div className="avatar">{username.substring(0, 2).toUpperCase()}</div>
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <div style={{ fontSize: '0.9rem', fontWeight: 500 }}>{username}</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Pro Plan</div>
          </div>
        </div>
      </aside>

      {/* Main Chat Interface */}
      <main className="chat-container">
        {/* Header with Multi-Agent Switch */}
        <header className="chat-header">
          {/* 3. Multi-agent Switch */}
          <select 
            className="agent-selector"
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
          >
            {AGENTS.map(agent => (
              <option key={agent.id} value={agent.id}>
                {agent.name}
              </option>
            ))}
          </select>
        </header>

        {/* 2. Better UI (Avatars, Markdown, Code Blocks) */}
        <div className="chat-messages" ref={scrollRef}>
          {messages.length === 0 && !isTyping ? (
            <div style={{ margin: 'auto', textAlign: 'center', color: 'var(--text-muted)' }}>
              <Bot size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
              <h2>How can I help you today?</h2>
              <p>Select an agent from the top menu and start chatting.</p>
            </div>
          ) : null}

          {messages.map((msg, idx) => (
            <div key={idx} className={`message-wrapper ${msg.role}`}>
              <div className="avatar" style={{ background: msg.role === 'user' ? 'var(--text-muted)' : 'var(--accent-gradient)' }}>
                {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
              </div>
              <div className="message-content">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="message-wrapper bot">
              <div className="avatar" style={{ background: 'var(--accent-gradient)' }}>
                <Bot size={18} />
              </div>
              <div className="message-content typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="chat-input-container">
          <div className="input-box">
            <textarea 
              placeholder="Send a message to your agents..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <button className="send-btn" onClick={handleSend} disabled={!input.trim() || isTyping}>
              <Send size={18} />
            </button>
          </div>
          <div style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.75rem' }}>
            Multi-Agent system powered by Llama 2 / Ollama
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
