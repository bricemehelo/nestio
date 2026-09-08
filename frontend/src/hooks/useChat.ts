//src/hooks/useProperties.ts
//
// PURPOSE: Custom React Query for all chat through ai
//
//

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { sendChatMessage } from "../api/chat";
import type { ChatResponse } from "../types/chat";

const mutation = useMutation({
  mutationFn: sendChatMessage,
});
