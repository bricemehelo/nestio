// src/api/chat.ts
//
// PURPOSE: All API calls related to ai chat
// Components never call Axios directly — they call these typed functions.
//
// This mirrors the Repository pattern from the backend — all data access
// behind a clean interface, typed end to end.

import { apiClient } from "./client";
import type { ChatProperty, ChatResponse } from "../types/chat";

export const sendChatMessage = async (
  message: string,
): Promise<ChatResponse> => {
  const response = await apiClient.post<ChatResponse>("/api/chat/", {
    message,
  });
  return response.data;
};
