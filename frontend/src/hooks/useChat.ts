//src/hooks/useProperties.ts
//
// PURPOSE: Custom React Query for all chat through ai
//
//

import { useMutation } from "@tanstack/react-query";
import { sendChatMessage } from "../api/chat";

export const useChat = () => {
  return useMutation({
    mutationFn: sendChatMessage,
  });
};
