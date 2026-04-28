import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  Bot, User, Send, Plus, LogOut, CheckSquare,
  MessageSquare, TerminalSquare, Share2, Wifi, WifiOff, Square,
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

// ── Agent definitions ─────────────────────────────────────────────────────────
const AGENTS = [
  { id: 'general',  name: 'General Assistant',     icon: <MessageSquare  size={16} />, hint: 'Ask me anything...' },
  { id: 'coder',    name: 'Software Dev Team',      icon: <TerminalSquare size={16} />, hint: 'Describe a feature to build...' },
  { id: 'red_team', name: 'Red Teaming Bot',        icon: <CheckSquare    size={16} />, hint: 'Enter an attack objective...' },
  { id: 'social',   name: 'Social Media Manager',   icon: <Share2         size={16} />, hint: 'Enter an industry or topic...' },
];

type Message = { role: 'user' | 'bot'; content: string };

// ── Main App ──────────────────────────────────────────────────────────────────
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername]     = useState('');

  if (!isLoggedIn) {
    return <LoginScreen onLogin={(u) => { setUsername(u); setIsLoggedIn(true); }} />;
  }
  return <ChatApp username={username} onLogout={() => setIsLoggedIn(false)} />;
}

// ── Login Screen ──────────────────────────────────────────────────────────────
function LoginScreen({ onLogin }: { onLogin: (name: string) => void }) {
  const [name, setName]         = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) onLogin(name.trim());
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
            <input type="text" placeholder="Enter your username" value={name}
              onChange={(e) => setName(e.target.value)} required />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input type="password" placeholder="••••••••" value={password}
              onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit" className="btn-primary">Sign In</button>
        </form>
      </div>
    </div>
  );
}

// ── Chat Application ──────────────────────────────────────────────────────────
function ChatApp({ username, onLogout }: { username: string; onLogout: () => void }) {
  const [messages, setMessages]         = useState<Message[]>([]);
  const [input, setInput]               = useState('');
  const [selectedAgent, setSelectedAgent] = useState(AGENTS[0].id);
  const [isTyping, setIsTyping]         = useState(false);
  const [isStreaming, setIsStreaming]   = useState(false);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const scrollRef   = useRef<HTMLDivElement>(null);
  const abortRef    = useRef<AbortController | null>(null);

  const currentAgent = AGENTS.find(a => a.id === selectedAgent)!;

  // ── health check ────────────────────────────────────────────────────────────
  useEffect(() => {
    const check = async () => {
      try {
        const r = await fetch(`${API_BASE}/api/health`, { signal: AbortSignal.timeout(3000) });
        setBackendOnline(r.ok);
      } catch {
        setBackendOnline(false);
      }
    };
    check();
    const id = setInterval(check, 10_000);
    return () => clearInterval(id);
  }, []);

  // ── auto-scroll ──────────────────────────────────────────────────────────────
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, isTyping]);

  // ── send handler with real SSE streaming ────────────────────────────────────
  const handleSend = async () => {
    if (!input.trim() || isStreaming) return;

    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setIsTyping(true);
    setIsStreaming(true);

    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent: selectedAgent, message: userMsg }),
        signal: controller.signal,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      // Add an empty bot message to stream into
      setIsTyping(false);
      setMessages(prev => [...prev, { role: 'bot', content: '' }]);

      const reader  = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer    = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          if (!line.startsWith('data: ') || line.length <= 6) continue;
          try {
            const data = JSON.parse(line.slice(6));
            if (data.text) {
              setMessages(prev => {
                const msgs = [...prev];
                msgs[msgs.length - 1] = {
                  ...msgs[msgs.length - 1],
                  content: msgs[msgs.length - 1].content + data.text,
                };
                return msgs;
              });
            }
            if (data.error) {
              setMessages(prev => {
                const msgs = [...prev];
                msgs[msgs.length - 1] = {
                  ...msgs[msgs.length - 1],
                  content: msgs[msgs.length - 1].content + `\n\n⚠️ ${data.error}`,
                };
                return msgs;
              });
            }
          } catch { /* ignore JSON parse errors */ }
        }
      }
    } catch (err: any) {
      setIsTyping(false);
      if (err.name === 'AbortError') {
        // user stopped — leave message as-is
      } else {
        setMessages(prev => [
          ...prev,
          {
            role: 'bot',
            content: backendOnline === false
              ? '❌ Backend is offline. Run **`python api.py`** in the project root first.'
              : `❌ Error: ${err.message}`,
          },
        ]);
      }
    } finally {
      setIsTyping(false);
      setIsStreaming(false);
      abortRef.current = null;
    }
  };

  const handleStop = () => {
    abortRef.current?.abort();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleNewChat = () => {
    if (isStreaming) handleStop();
    setMessages([]);
  };

  return (
    <div className="app-layout">
      {/* ── Sidebar ────────────────────────────────────────────────────────── */}
      <aside className="sidebar glass">
        <div className="sidebar-header">
          <h2 style={{
            fontSize: '1.25rem', margin: 0,
            background: 'var(--accent-gradient)',
            WebkitBackgroundClip: 'text',
            backgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}>
            MultiAgent
          </h2>
          <button className="btn-icon" title="Logout" onClick={onLogout}>
            <LogOut size={18} />
          </button>
        </div>

        {/* Backend status badge */}
        <div style={{ padding: '0 1.25rem 0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {backendOnline === null ? (
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Checking backend…</span>
          ) : backendOnline ? (
            <>
              <Wifi size={13} style={{ color: '#22c55e' }} />
              <span style={{ fontSize: '0.75rem', color: '#22c55e' }}>Backend online</span>
            </>
          ) : (
            <>
              <WifiOff size={13} style={{ color: '#ef4444' }} />
              <span style={{ fontSize: '0.75rem', color: '#ef4444' }}>Run python api.py</span>
            </>
          )}
        </div>

        <button className="btn-primary new-chat-btn" onClick={handleNewChat}>
          <Plus size={18} /> New Chat
        </button>

        {/* Agent list */}
        <div style={{ padding: '0 1rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', padding: '0.5rem 0.5rem', marginTop: '0.5rem' }}>
            AGENTS
          </div>
          {AGENTS.map(agent => (
            <div
              key={agent.id}
              className={`history-item ${selectedAgent === agent.id ? 'active' : ''}`}
              onClick={() => setSelectedAgent(agent.id)}
              style={{ fontWeight: selectedAgent === agent.id ? 600 : 400 }}
            >
              {agent.icon}
              {agent.name}
            </div>
          ))}
        </div>

        <div className="user-profile" style={{ marginTop: 'auto' }}>
          <div className="avatar">{username.substring(0, 2).toUpperCase()}</div>
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <div style={{ fontSize: '0.9rem', fontWeight: 500 }}>{username}</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Multi-Agent</div>
          </div>
        </div>
      </aside>

      {/* ── Main Chat ──────────────────────────────────────────────────────── */}
      <main className="chat-container">
        <header className="chat-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span style={{ color: 'var(--accent-color)' }}>{currentAgent.icon}</span>
            <span style={{ fontWeight: 600 }}>{currentAgent.name}</span>
          </div>
        </header>

        {/* Messages */}
        <div className="chat-messages" ref={scrollRef}>
          {messages.length === 0 && !isTyping ? (
            <div style={{ margin: 'auto', textAlign: 'center', color: 'var(--text-muted)' }}>
              <Bot size={48} style={{ marginBottom: '1rem', opacity: 0.4 }} />
              <h2 style={{ marginBottom: '0.5rem' }}>{currentAgent.name}</h2>
              <p style={{ fontSize: '0.9rem' }}>{currentAgent.hint}</p>
            </div>
          ) : null}

          {messages.map((msg, idx) => (
            <div key={idx} className={`message-wrapper ${msg.role}`}>
              <div
                className="avatar"
                style={{ background: msg.role === 'user' ? 'var(--text-muted)' : 'var(--accent-gradient)', flexShrink: 0 }}
              >
                {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
              </div>
              <div className="message-content">
                {msg.role === 'bot' ? (
                  /* Agent output — use <pre> for terminal-style blocks, markdown for code fences */
                  <ReactMarkdown
                    components={{
                      // Inline code
                      // eslint-disable-next-line @typescript-eslint/no-unused-vars
                      code({ className, children, ref: _ref, ...props }) {
                        const isBlock = className?.includes('language-');
                        return isBlock ? (
                          <pre><code className={className} {...props}>{children}</code></pre>
                        ) : (
                          <code {...props}>{children}</code>
                        );
                      },
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                ) : (
                  msg.content
                )}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="message-wrapper bot">
              <div className="avatar" style={{ background: 'var(--accent-gradient)', flexShrink: 0 }}>
                <Bot size={18} />
              </div>
              <div className="message-content typing-indicator">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="chat-input-container">
          <div className="input-box">
            <textarea
              placeholder={currentAgent.hint}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isStreaming}
            />
            {isStreaming ? (
              <button className="send-btn" onClick={handleStop} title="Stop generation"
                style={{ background: '#ef4444' }}>
                <Square size={16} />
              </button>
            ) : (
              <button className="send-btn" onClick={handleSend}
                disabled={!input.trim()}>
                <Send size={18} />
              </button>
            )}
          </div>
          <div style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.75rem' }}>
            Powered by Ollama · {currentAgent.name}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
