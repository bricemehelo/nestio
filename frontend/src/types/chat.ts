export interface ChatProperty {
  id: number;
  title: string;
  price: number;
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  property_type: string;
  status: string;
  verified: boolean;
  description: string;
}

export interface ChatResponse {
  response: string;
  properties_found: number;
  properties: ChatProperty[];
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  properties?: ChatProperty[];
}
