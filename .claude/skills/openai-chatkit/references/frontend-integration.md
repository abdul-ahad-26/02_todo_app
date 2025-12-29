# Frontend Integration Reference

Complete reference for ChatKit.js React integration.

## Installation

```bash
npm install @openai/chatkit-react
```

Or via CDN:
```html
<script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"></script>
```

## Basic Setup

### React Component

```tsx
import { ChatKit, useChatKit } from "@openai/chatkit-react";

export function App() {
  const { control } = useChatKit({
    api: {
      url: "http://localhost:8000/chatkit",
      domainKey: "local-dev",
    },
  });

  return (
    <ChatKit
      control={control}
      className="h-screen w-full"
    />
  );
}
```

### Vanilla JavaScript

```javascript
const chatkit = document.createElement("openai-chatkit");
chatkit.setOptions({
  api: {
    url: "http://localhost:8000/chatkit",
    domainKey: "local-dev",
  },
});
chatkit.classList.add("h-screen", "w-full");
document.body.appendChild(chatkit);
```

## useChatKit Hook

### Options

```tsx
const { control, thread, threads, isLoading } = useChatKit({
  // API Configuration
  api: {
    url: "http://localhost:8000/chatkit",
    domainKey: "local-dev",

    // Custom headers
    headers: () => ({
      "x-user-id": userId,
      "x-page-context": pageId,
    }),

    // For OpenAI-hosted backends
    async getClientSecret(existing) {
      if (existing) {
        // Refresh existing session
        return existing;
      }
      const res = await fetch("/api/chatkit/session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      const { client_secret } = await res.json();
      return client_secret;
    },
  },

  // Thread Configuration
  thread: {
    id: "thread_123", // Start with specific thread
  },

  // Event Handlers
  onResponseStart: () => {
    console.log("Response started");
  },

  onResponseEnd: () => {
    console.log("Response ended");
  },

  onError: (error) => {
    console.error("ChatKit error:", error);
  },

  // Widget Action Handler
  handleWidgetAction: async (action) => {
    console.log("Widget action:", action.type, action.payload);
    // Return false to prevent default handling
    return true;
  },

  // Client Effect Handler
  onEffect: (effect) => {
    if (effect.type === "open_url") {
      window.open(effect.payload.url, "_blank");
    } else if (effect.type === "toast") {
      showToast(effect.payload.message, effect.payload.type);
    }
  },

  // Entity Click Handler
  onEntityClick: (entity) => {
    console.log("Entity clicked:", entity.type, entity.id);
    // Navigate to entity detail page
    router.push(`/${entity.type}/${entity.id}`);
  },

  // File Upload Configuration
  fileUpload: {
    enabled: true,
    maxSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ["image/*", "application/pdf"],
  },
});
```

### Return Values

```tsx
const {
  control,     // Pass to ChatKit component
  thread,      // Current thread metadata
  threads,     // List of all threads
  isLoading,   // Loading state
  error,       // Error state
  sendMessage, // Programmatically send message
  sendAction,  // Programmatically trigger action
  createThread,// Create new thread
  deleteThread,// Delete thread
  switchThread,// Switch to different thread
} = useChatKit(options);
```

## ChatKit Component

### Props

```tsx
<ChatKit
  control={control}
  className="h-screen w-full"

  // Theme
  theme="light" // "light" | "dark" | "system"
  accentColor="blue" // Color scheme

  // Header
  header={{
    title: "Support Chat",
    subtitle: "We're here to help",
    logo: "/logo.svg",
    showThreadList: true,
  }}

  // Composer
  composer={{
    placeholder: "Type your message...",
    showAttachments: true,
    showTools: true,
    tools: [
      {
        id: "search",
        label: "Search",
        icon: "search",
        description: "Search the knowledge base",
      },
    ],
  }}

  // Messages
  messages={{
    showTimestamps: true,
    showAvatars: true,
    userAvatar: "/user-avatar.png",
    assistantAvatar: "/bot-avatar.png",
  }}

  // Empty State
  emptyState={{
    title: "Welcome!",
    description: "How can I help you today?",
    suggestions: [
      "What can you do?",
      "Help me with my order",
      "Show me products",
    ],
  }}

  // Disclaimer
  disclaimer={{
    text: "AI responses may contain errors.",
    link: {
      text: "Learn more",
      url: "/ai-policy",
    },
  }}
/>
```

## Customization

### Custom Theme

```tsx
<ChatKit
  control={control}
  theme={{
    colors: {
      primary: "#0066cc",
      background: "#ffffff",
      surface: "#f5f5f5",
      text: "#1a1a1a",
      textSecondary: "#666666",
      border: "#e0e0e0",
      error: "#dc2626",
      success: "#16a34a",
    },
    fonts: {
      sans: "Inter, system-ui, sans-serif",
      mono: "JetBrains Mono, monospace",
    },
    borderRadius: {
      sm: "4px",
      md: "8px",
      lg: "12px",
    },
  }}
/>
```

### Custom CSS

```css
/* Override ChatKit styles */
.chatkit-container {
  --chatkit-primary: #0066cc;
  --chatkit-background: #ffffff;
  --chatkit-surface: #f5f5f5;
}

.chatkit-message-user {
  background-color: var(--chatkit-primary);
  color: white;
}

.chatkit-message-assistant {
  background-color: var(--chatkit-surface);
}

.chatkit-composer-input {
  border-radius: 24px;
}
```

## Event Handling

### Widget Actions

Handle actions from widgets:

```tsx
const { control } = useChatKit({
  handleWidgetAction: async (action) => {
    switch (action.type) {
      case "add_to_cart":
        await addToCart(action.payload.productId);
        showToast("Added to cart!");
        return true; // Allow ChatKit to send action to server

      case "open_modal":
        openModal(action.payload.modalId);
        return false; // Prevent server call, handled client-side

      default:
        return true; // Default: send to server
    }
  },
});
```

### Client Effects

Handle server-triggered effects:

```tsx
const { control } = useChatKit({
  onEffect: (effect) => {
    switch (effect.type) {
      case "open_url":
        window.open(effect.payload.url, "_blank");
        break;

      case "toast":
        toast[effect.payload.type](effect.payload.message);
        break;

      case "navigate":
        router.push(effect.payload.path);
        break;

      case "sync_state":
        updateAppState(effect.payload);
        break;

      case "play_sound":
        playNotificationSound();
        break;
    }
  },
});
```

### Entity Clicks

Handle @-mention and annotation clicks:

```tsx
const { control } = useChatKit({
  onEntityClick: (entity) => {
    switch (entity.type) {
      case "article":
        router.push(`/articles/${entity.id}`);
        break;

      case "user":
        showUserProfile(entity.id);
        break;

      case "product":
        openProductModal(entity.id);
        break;
    }
  },
});
```

## Entity Search (Mentions)

Enable @-mentions in the composer:

```tsx
const { control } = useChatKit({
  api: { url: "/api/chatkit", domainKey: "local" },

  // Entity configuration
  entities: {
    enabled: true,
    trigger: "@", // Character to trigger search

    // Search function
    search: async (query, entityType) => {
      const results = await fetch(
        `/api/entities/search?q=${query}&type=${entityType}`
      ).then(r => r.json());

      return results.map(r => ({
        id: r.id,
        type: r.type,
        label: r.name,
        description: r.subtitle,
        icon: r.icon,
      }));
    },

    // Entity types to search
    types: [
      { id: "article", label: "Articles", icon: "document" },
      { id: "user", label: "Users", icon: "user" },
      { id: "product", label: "Products", icon: "shopping-bag" },
    ],
  },
});
```

## Programmatic Control

### Send Messages

```tsx
const { sendMessage } = useChatKit(options);

// Send text message
await sendMessage("Hello, I need help");

// Send with context
await sendMessage("Search for this", {
  context: {
    pageUrl: window.location.href,
    selectedText: getSelectedText(),
  },
});
```

### Trigger Actions

```tsx
const { sendAction } = useChatKit(options);

// Trigger action programmatically
await sendAction("refresh_data", {
  category: "electronics",
});
```

### Thread Management

```tsx
const { createThread, switchThread, deleteThread, threads } = useChatKit(options);

// Create new thread
const newThread = await createThread({
  title: "Support Request",
  metadata: { category: "billing" },
});

// Switch to thread
await switchThread(newThread.id);

// Delete thread
await deleteThread(threadId);

// List threads
console.log(threads); // [{ id, title, createdAt, ... }]
```

## File Uploads

### Configuration

```tsx
const { control } = useChatKit({
  fileUpload: {
    enabled: true,
    maxSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: [
      "image/jpeg",
      "image/png",
      "image/gif",
      "application/pdf",
      "text/plain",
    ],

    // Custom upload handler (optional)
    onUpload: async (file) => {
      // Upload to your storage
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      const { url, id } = await response.json();
      return { url, id };
    },
  },
});
```

### Drag and Drop

File drag-and-drop is enabled by default when `fileUpload.enabled` is true.

```tsx
<ChatKit
  control={control}
  composer={{
    dropzone: {
      text: "Drop files here",
      icon: "upload",
    },
  }}
/>
```

## Custom Components

### Custom Message Renderer

```tsx
import { ChatKit, MessageRenderer } from "@openai/chatkit-react";

function CustomMessage({ message, children }) {
  if (message.type === "custom_widget") {
    return <MyCustomWidget data={message.data} />;
  }
  return children; // Default rendering
}

<ChatKit
  control={control}
  components={{
    Message: CustomMessage,
  }}
/>
```

### Custom Header

```tsx
function CustomHeader({ thread, onBack }) {
  return (
    <div className="flex items-center gap-4 p-4 border-b">
      <button onClick={onBack}>
        <ArrowLeftIcon />
      </button>
      <div>
        <h2 className="font-bold">{thread?.title || "New Chat"}</h2>
        <p className="text-sm text-gray-500">Powered by AI</p>
      </div>
      <button className="ml-auto" onClick={() => openSettings()}>
        <SettingsIcon />
      </button>
    </div>
  );
}

<ChatKit
  control={control}
  components={{
    Header: CustomHeader,
  }}
/>
```

### Custom Composer

```tsx
function CustomComposer({ onSend, isLoading }) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSend(message);
      setMessage("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 p-4 border-t">
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
        className="flex-1 px-4 py-2 border rounded-full"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={!message.trim() || isLoading}
        className="px-6 py-2 bg-blue-500 text-white rounded-full disabled:opacity-50"
      >
        {isLoading ? "..." : "Send"}
      </button>
    </form>
  );
}

<ChatKit
  control={control}
  components={{
    Composer: CustomComposer,
  }}
/>
```

## Layout Options

### Full Page

```tsx
function FullPageChat() {
  const { control } = useChatKit(options);

  return (
    <div className="h-screen w-screen">
      <ChatKit control={control} className="h-full w-full" />
    </div>
  );
}
```

### Sidebar Panel

```tsx
function SidebarChat() {
  const [isOpen, setIsOpen] = useState(false);
  const { control } = useChatKit(options);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open Chat</button>

      {isOpen && (
        <div className="fixed right-0 top-0 h-screen w-96 shadow-lg">
          <ChatKit
            control={control}
            className="h-full w-full"
            header={{
              showClose: true,
              onClose: () => setIsOpen(false),
            }}
          />
        </div>
      )}
    </>
  );
}
```

### Floating Widget

```tsx
function FloatingChat() {
  const [isOpen, setIsOpen] = useState(false);
  const { control } = useChatKit(options);

  return (
    <>
      {isOpen ? (
        <div className="fixed bottom-4 right-4 w-96 h-[600px] rounded-lg shadow-xl overflow-hidden">
          <ChatKit
            control={control}
            className="h-full w-full"
            header={{
              showClose: true,
              onClose: () => setIsOpen(false),
            }}
          />
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-4 right-4 w-14 h-14 bg-blue-500 text-white rounded-full shadow-lg flex items-center justify-center"
        >
          <ChatIcon />
        </button>
      )}
    </>
  );
}
```

## Next.js Integration

### App Router

```tsx
// app/chat/page.tsx
"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";

export default function ChatPage() {
  const { control } = useChatKit({
    api: {
      url: "/api/chatkit",
      domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY!,
    },
  });

  return (
    <main className="h-screen">
      <ChatKit control={control} className="h-full" />
    </main>
  );
}
```

### API Route

```typescript
// app/api/chatkit/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const body = await request.text();

  // Forward to your Python backend
  const response = await fetch("http://localhost:8000/chatkit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // Forward auth headers
      Authorization: request.headers.get("Authorization") || "",
    },
    body,
  });

  // Stream response
  if (response.headers.get("Content-Type")?.includes("text/event-stream")) {
    return new NextResponse(response.body, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
    });
  }

  return NextResponse.json(await response.json());
}
```

## Best Practices

### Performance

1. **Lazy load ChatKit**: Don't load on every page
2. **Memoize handlers**: Use `useCallback` for event handlers
3. **Debounce entity search**: Prevent excessive API calls

### Accessibility

1. **Keyboard navigation**: ChatKit supports keyboard by default
2. **Screen readers**: Add aria-labels to custom components
3. **Focus management**: Handle focus when opening/closing chat

### Security

1. **Domain allowlist**: Configure allowed domains in OpenAI dashboard
2. **HTTPS**: Always use HTTPS in production
3. **Auth tokens**: Never expose secrets client-side

### Error Handling

```tsx
const { control, error } = useChatKit({
  onError: (err) => {
    if (err.code === "RATE_LIMITED") {
      showToast("Please wait before sending another message");
    } else if (err.code === "UNAUTHORIZED") {
      router.push("/login");
    } else {
      console.error("ChatKit error:", err);
      showToast("Something went wrong. Please try again.");
    }
  },
});

// Display error state
if (error) {
  return <ErrorBoundary error={error} onRetry={() => window.location.reload()} />;
}
```
