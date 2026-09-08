//src/componnents/ChatPanel.tsx
//
// PURPOSE: Chat panel for AI chat. Uses React Query to send messages to the backend.
// The backend calls the AI service and returns a structured response with properties found.
//
// PATTERN: Container — manages state and data fetching, renders child components for UI.

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { sendChatMessage } from "../api/chat";
import type { ChatMessage, ChatProperty } from "../types/chat";

interface ChatPanelProps {
  onProrpertySelect: (property: ChatProperty) => void;
}

export function ChatPanel({ onPropertySelect }: ChatPanelProps) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const chatMutation = useMutation({
    mutationFn: sendChatMessage,

    onSuccess: (data) => {
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.response,
          properties: data.properties,
        },
      ]);
    },
  });

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || chatMutation.isPending) {
      return;
    }

    setMessages((currentMessages) => [
      ...currentMessages,
      {
        id: crypto.randomUUID(),
        role: "user",
        content: trimmedMessage,
      },
    ]);

    setMessage("");
    chatMutation.mutate(trimmedMessage);
  }

  return (
    <aside className="chat-panel">
      <header className="chat-panel__header">
        <h2>Nestio AI</h2>
        <p>Describe the property you are looking for.</p>
      </header>

      <div className="chat-panel__messages">
        {messages.length === 0 && (
          <p className="chat-panel__empty">
            Try: “Find a 3-bedroom flat for sale in Lekki under ₦10 million.”
          </p>
        )}

        {messages.map((chatMessage) => (
          <div
            className={`chat-message chat-message--${chatMessage.role}`}
            key={chatMessage.id}
          >
            <p>{chatMessage.content}</p>

            {chatMessage.properties?.map((property) => (
              <button
                className="chat-property-card"
                key={property.id}
                onClick={() => onPropertySelect(property)}
                type="button"
              >
                <strong>{property.title}</strong>
                <span>₦{property.price.toLocaleString()}</span>
                <span>{property.address}</span>
                {!property.verified && (
                  <small className="chat-property-card__unverified">
                    Unverified listing
                  </small>
                )}
              </button>
            ))}
          </div>
        ))}

        {chatMutation.isPending && (
          <p className="chat-panel__loading">Searching listings…</p>
        )}

        {chatMutation.isError && (
          <p className="chat-panel__error">
            The AI search is temporarily unavailable. Please try again.
          </p>
        )}
      </div>

      <form className="chat-panel__form" onSubmit={handleSubmit}>
        <input
          aria-label="Property search message"
          disabled={chatMutation.isPending}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Describe the property you need…"
          value={message}
        />

        <button
          disabled={!message.trim() || chatMutation.isPending}
          type="submit"
        >
          Send
        </button>
      </form>
    </aside>
  );
}
