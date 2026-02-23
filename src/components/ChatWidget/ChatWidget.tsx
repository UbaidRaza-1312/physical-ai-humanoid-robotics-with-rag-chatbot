import React, { useState, useRef, useEffect } from 'react';
import './ChatWidget.css';

// ============================================================================
// Type Definitions
// ============================================================================

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  sources?: Source[];
}

interface Source {
  file: string;
  module: string;
  score: number;
}

interface ChatWidgetProps {
  backendUrl?: string;
  position?: 'bottom-right' | 'bottom-left';
}

// ============================================================================
// ChatWidget Component
// ============================================================================

/**
 * Panaversity RAG Chat Widget
 * 
 * A floating chat widget embedded in the Docusaurus site.
 * Features:
 * - Floating chat bubble in bottom-right corner
 * - Real-time chat with textbook AI
 * - Support for English and Urdu
 * - Context-aware questions from selected text
 * - Source citations for answers
 */
export const ChatWidget: React.FC<ChatWidgetProps> = ({
  backendUrl = 'http://localhost:8000',
  position = 'bottom-right',
}) => {
  // State
  const [isOpen, setIsOpen] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [language, setLanguage] = useState<'en' | 'ur'>('en');
  
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  // Generate unique session ID
  const sessionIdRef = useRef<string>(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);

  // ============================================================================
  // Effects
  // ============================================================================

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Listen for text selection events
  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      const selectedText = selection?.toString().trim();
      
      if (selectedText && selectedText.length > 0 && selectedText.length < 500) {
        setSelectedText(selectedText);
      } else {
        setSelectedText(null);
      }
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    return () => document.removeEventListener('selectionchange', handleSelectionChange);
  }, []);

  // Load chat history from localStorage
  useEffect(() => {
    const savedMessages = localStorage.getItem(`chat_history_${sessionIdRef.current}`);
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (e) {
        console.error('Failed to load chat history:', e);
      }
    }
  }, []);

  // Save chat history to localStorage
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(`chat_history_${sessionIdRef.current}`, JSON.stringify(messages));
    }
  }, [messages]);

  // ============================================================================
  // Helper Functions
  // ============================================================================

  const generateMessageId = () => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (language === 'ur') {
      if (hour < 12) return 'صبح بخیر! میں آپ کی کیا مدد کر سکتا ہوں؟';
      if (hour < 18) return 'دوپہر بخیر! میں آپ کی کیا مدد کر سکتا ہوں؟';
      return 'شام بخیر! میں آپ کی کیا مدد کر سکتا ہوں؟';
    }
    if (hour < 12) return 'Good morning! How can I help you today?';
    if (hour < 18) return 'Good afternoon! How can I help you today?';
    return 'Good evening! How can I help you today?';
  };

  // ============================================================================
  // API Calls
  // ============================================================================

  const sendMessage = async (query: string, selection: string | null = null) => {
    if (!query.trim()) return;

    setIsTyping(true);

    // Add user message
    const userMessage: Message = {
      id: generateMessageId(),
      role: 'user',
      content: query,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    try {
      // Choose endpoint based on whether there's selected text
      const endpoint = selection 
        ? `${backendUrl}/ask-with-selection`
        : `${backendUrl}/chat`;

      const requestBody = selection
        ? {
            query,
            selected_text: selection,
            session_id: sessionIdRef.current,
            language,
          }
        : {
            query,
            session_id: sessionIdRef.current,
            language,
          };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message
      const assistantMessage: Message = {
        id: generateMessageId(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        sources: data.sources,
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Clear selection after using it
      if (selection) {
        setSelectedText(null);
      }
    } catch (error) {
      console.error('Chat error:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: generateMessageId(),
        role: 'assistant',
        content: language === 'ur' 
          ? 'معذرت، کوئی خرابی پیش آگئی ہے۔ براہ کرم دوبارہ کوشش کریں۔'
          : 'I apologize, but an error occurred. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // ============================================================================
  // Event Handlers
  // ============================================================================

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      sendMessage(inputValue.trim(), selectedText);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    localStorage.removeItem(`chat_history_${sessionIdRef.current}`);
  };

  const handleLanguageToggle = () => {
    setLanguage(prev => prev === 'en' ? 'ur' : 'en');
  };

  const handleQuickQuestion = (question: string) => {
    sendMessage(question, selectedText);
  };

  // ============================================================================
  // Render
  // ============================================================================

  return (
    <div className={`chat-widget ${position} ${isOpen ? 'open' : ''}`}>
      {/* Chat Toggle Button */}
      {!isOpen && (
        <button 
          className="chat-toggle-button"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
        >
          <svg className="chat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
          {selectedText && (
            <span className="selection-indicator">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <circle cx="18" cy="6" r="4" />
              </svg>
            </span>
          )}
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-header-title">
              <span className="chat-robot-icon">🤖</span>
              <div>
                <h3 className="chat-title">
                  {language === 'ur' ? 'پانورسٹی اسسٹنٹ' : 'Panaversity Assistant'}
                </h3>
                <p className="chat-subtitle">
                  {language === 'ur' 
                    ? 'Physical AI & Humanoid Robotics' 
                    : 'Physical AI & Humanoid Robotics'}
                </p>
              </div>
            </div>
            <div className="chat-header-actions">
              <button
                className="chat-language-toggle"
                onClick={handleLanguageToggle}
                title={language === 'ur' ? 'Switch to English' : 'اردو میں تبدیل کریں'}
              >
                {language === 'ur' ? 'EN' : 'اردو'}
              </button>
              <button
                className="chat-clear-button"
                onClick={handleClearChat}
                title={language === 'ur' ? 'چیٹ صاف کریں' : 'Clear chat'}
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="3,6 5,6 21,6" />
                  <path d="M19,6v14a2,2,0,0,1-2,2H7a2,2,0,0,1-2-2V6m3,0V4a2,2,0,0,1,2-2h4a2,2,0,0,1,2,2v2" />
                </svg>
              </button>
              <button
                className="chat-close-button"
                onClick={() => setIsOpen(false)}
                aria-label="Close chat"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          </div>

          {/* Selected Text Banner */}
          {selectedText && (
            <div className="selected-text-banner">
              <div className="selected-text-info">
                <svg viewBox="0 0 24 24" fill="currentColor" className="selection-icon">
                  <path d="M4,6h16v2H4V6z M4,11h16v2H4V11z M4,16h10v2H4V16z" />
                </svg>
                <span className="selected-text-label">
                  {language === 'ur' ? 'منتخب شدہ متن:' : 'Selected text:'}
                </span>
              </div>
              <div className="selected-text-preview">{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}</div>
              <button
                className="clear-selection-button"
                onClick={() => setSelectedText(null)}
                title={language === 'ur' ? 'انتخاب صاف کریں' : 'Clear selection'}
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          )}

          {/* Messages */}
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="chat-welcome">
                <div className="welcome-icon">📚</div>
                <h4 className="welcome-title">
                  {language === 'ur' 
                    ? 'کتاب میں خوش آمدید!' 
                    : 'Welcome to the Textbook!'}
                </h4>
                <p className="welcome-message">
                  {getGreeting()}
                </p>
                
                {/* Quick Questions */}
                <div className="quick-questions">
                  <p className="quick-questions-label">
                    {language === 'ur' ? 'تیزی سے شروع کریں:' : 'Quick start:'}
                  </p>
                  <div className="quick-questions-list">
                    <button 
                      className="quick-question-chip"
                      onClick={() => handleQuickQuestion(language === 'ur' 
                        ? 'humanoid robotics کیا ہے؟'
                        : 'What is humanoid robotics?')}
                    >
                      {language === 'ur' ? '🤖 Humanoid Robotics' : '🤖 Humanoid Robotics'}
                    </button>
                    <button 
                      className="quick-question-chip"
                      onClick={() => handleQuickQuestion(language === 'ur'
                        ? 'ROS 2 کیا ہے؟'
                        : 'What is ROS 2?')}
                    >
                      {language === 'ur' ? '⚙️ ROS 2' : '⚙️ ROS 2'}
                    </button>
                    <button 
                      className="quick-question-chip"
                      onClick={() => handleQuickQuestion(language === 'ur'
                        ? 'Digital Twin کیسے کام کرتا ہے؟'
                        : 'How does Digital Twin work?')}
                    >
                      {language === 'ur' ? '🔮 Digital Twin' : '🔮 Digital Twin'}
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.role}`}
                >
                  <div className="message-avatar">
                    {message.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    <div className="message-text">{message.content}</div>
                    
                    {/* Sources */}
                    {message.sources && message.sources.length > 0 && (
                      <div className="message-sources">
                        <p className="sources-label">
                          {language === 'ur' ? 'ماخذ:' : 'Sources:'}
                        </p>
                        <div className="sources-list">
                          {message.sources.map((source, idx) => (
                            <div key={idx} className="source-item">
                              <span className="source-file">{source.file}</span>
                              <span className="source-module">• {source.module}</span>
                              <span className="source-score">
                                {(source.score * 100).toFixed(0)}% match
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <div className="message-time">
                      {new Date(message.timestamp).toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </div>
                  </div>
                </div>
              ))
            )}
            
            {/* Typing Indicator */}
            {isTyping && (
              <div className="message assistant typing">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form className="chat-input-form" onSubmit={handleSubmit}>
            <input
              ref={inputRef}
              type="text"
              className="chat-input"
              placeholder={
                selectedText
                  ? (language === 'ur' 
                      ? 'منتخب متن کے بارے میں پوچھیں...' 
                      : 'Ask about selected text...')
                  : (language === 'ur'
                      ? 'اپنا سوال لکھیں...'
                      : 'Type your question...')
              }
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={isTyping}
            />
            <button
              type="submit"
              className="chat-send-button"
              disabled={isTyping || !inputValue.trim()}
            >
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
