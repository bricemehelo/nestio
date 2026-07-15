//src/main.tsx

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import "./index.css";
import App from "./App.tsx";

// QueryClient holds the cache and configuration for all queries
// staleTime: how long cached data is considered fresh before refetching

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes — property listings don't change every second
      retry: 1, // Retry failed requests once before showing an error
    },
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    {/* QueryClientProvider makes React Query available to every component */}
    <QueryClientProvider client={queryClient}>
      <App />
      {/* ReactQueryDevtools is a dev-only tool for inspecting queries */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
    {/* <App /> is the root component of the app */}
  </StrictMode>,
);
