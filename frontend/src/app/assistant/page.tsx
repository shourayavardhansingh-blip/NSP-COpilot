"use client";

import { useState, useRef, useEffect } from "react";
import {
  Bot,
  User,
  Send,
  Sparkles,
  RotateCcw,
  Copy,
  Check,
  ExternalLink,
  ShieldAlert,
  Cpu,
  Clock,
  ArrowRight,
  BookOpen
} from "lucide-react";
import { sendChatMessage } from "@/lib/api";
import { Citation } from "@/lib/types";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  model_name?: string;
  latency_ms?: number;
  is_fallback?: boolean;
}

const SUGGESTED_QUERIES = [
  "I manufacture household water heaters (geysers). How can I identify the relevant standard, check if a QCO applies, and prepare a checklist?",
  "What is the difference between Scheme-I (ISI Mark) and Scheme-II (CRS) for electronics?",
  "Are all lithium-ion batteries and power banks subject to compulsory BIS certification in India?",
  "What are the mandatory requirements under the Toys Quality Control Order 2020?",
  "How do I locate BIS recognized testing laboratories for high strength TMT steel bars?"
];

export default function AssistantPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "initial",
      role: "assistant",
      content: `### Welcome to the BIS AI Compliance Assistant

I help manufacturers, importers, engineers, and quality teams navigate the Bureau of Indian Standards (BIS) regulatory framework.

You can ask me to:
- **Identify applicable Indian Standards (IS)** for any product or component.
- **Verify mandatory Quality Control Orders (QCO)** issued by GoI ministries.
- **Clarify Certification Schemes** (Scheme-I ISI Mark vs Scheme-II CRS).
- **Find accredited testing laboratories** and their testing scopes.

Every statement is strictly grounded in the database records with traceable citations. How can I assist your compliance project today?`,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = async (textToSend?: string) => {
    const text = (textToSend || input).trim();
    if (!text || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(text, conversationId);
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
        citations: data.citations,
        model_name: data.model_name,
        latency_ms: data.latency_ms,
        is_fallback: data.is_fallback,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: `> [!WARNING]\n> Unable to connect to the backend query service. Please verify that the API service is active.`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleReset = () => {
    setConversationId(undefined);
    setMessages([
      {
        id: "initial",
        role: "assistant",
        content: "Conversation history reset. Ask a new BIS compliance question to begin.",
      },
    ]);
  };

  return (
    <div className="max-w-5xl mx-auto flex flex-col h-[calc(100vh-8rem)]">
      {/* Header Bar */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Bot className="w-5 h-5 text-blue-400" /> BIS Compliance AI Assistant
          </h1>
          <p className="text-xs text-slate-400">
            Grounding user queries across verified Indian Standards & Gazette QCO decrees
          </p>
        </div>
        <button
          onClick={handleReset}
          className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium flex items-center gap-1.5 border border-slate-700 transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5" /> Reset Chat
        </button>
      </div>

      {/* Message Stream */}
      <div className="flex-1 overflow-y-auto space-y-6 pr-2">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            {msg.role === "assistant" && (
              <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 text-blue-400 flex items-center justify-center shrink-0 mt-1">
                <Bot className="w-4 h-4" />
              </div>
            )}

            <div
              className={`max-w-3xl rounded-2xl p-5 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-tr-none shadow-md"
                  : "bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none shadow-sm"
              }`}
            >
              {/* Message Content */}
              <div className="whitespace-pre-wrap space-y-2 font-normal">
                {msg.content}
              </div>

              {/* Citations Box for Assistant */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-5 pt-4 border-t border-slate-800/80">
                  <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-blue-400" />
                    Verified Evidence & Citations ({msg.citations.length})
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {msg.citations.map((c, i) => (
                      <div
                        key={i}
                        className="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800 text-xs space-y-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-blue-400">{c.identifier}</span>
                          <span className="px-1.5 py-0.2 rounded text-[10px] bg-slate-800 text-slate-400">
                            {c.source_type}
                          </span>
                        </div>
                        <div className="text-slate-300 font-medium line-clamp-1">{c.title}</div>
                        {c.source_url && (
                          <a
                            href={c.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-[11px] text-blue-400 hover:text-blue-300 hover:underline pt-0.5"
                          >
                            Official BIS Record <ExternalLink className="w-3 h-3" />
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Footer bar with model and copy button */}
              {msg.role === "assistant" && msg.id !== "initial" && (
                <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-500">
                  <div className="flex items-center gap-2">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                      <Cpu className="w-3 h-3" /> {msg.model_name || "Deterministic Grounded RAG"}
                    </span>
                    {msg.latency_ms !== undefined && (
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" /> {msg.latency_ms} ms
                      </span>
                    )}
                  </div>
                  <button
                    onClick={() => handleCopy(msg.content, msg.id)}
                    className="flex items-center gap-1 hover:text-slate-300 transition-colors"
                  >
                    {copiedId === msg.id ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-400" /> Copied
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" /> Copy Answer
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>

            {msg.role === "user" && (
              <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 text-slate-300 flex items-center justify-center shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 text-blue-400 flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 animate-spin" />
            </div>
            <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center gap-3">
              <div className="flex space-x-1.5">
                <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" />
                <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce [animation-delay:0.2s]" />
                <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce [animation-delay:0.4s]" />
              </div>
              <span>Searching Indian Standards catalogue & retrieving verified QCO records...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions (only if 1 message exists) */}
      {messages.length === 1 && (
        <div className="py-3">
          <div className="text-xs font-semibold text-slate-400 mb-2">Example Compliance Questions:</div>
          <div className="flex flex-wrap gap-2">
            {SUGGESTED_QUERIES.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleSubmit(q)}
                className="text-left text-xs px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-white transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Box */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit();
        }}
        className="pt-4 border-t border-slate-800"
      >
        <div className="relative flex items-center">
          <input
            type="text"
            placeholder="Ask a BIS standard, QCO mandate, or certification process question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            className="w-full pl-4 pr-12 py-3.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-inner disabled:opacity-60"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-2 p-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white disabled:opacity-40 disabled:hover:bg-blue-600 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
        <div className="flex justify-between text-[11px] text-slate-500 px-1 pt-1.5">
          <span>Grounds replies in real relational DB records • No API tokens or fees</span>
          <span>Press Enter to send</span>
        </div>
      </form>
    </div>
  );
}
