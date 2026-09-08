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
