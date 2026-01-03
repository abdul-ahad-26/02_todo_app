# OpenAI ChatKit Setup and Integration

## Table of Contents

1. [ChatKit Overview](#chatkit-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Basic Configuration](#basic-configuration)
4. [Backend Integration](#backend-integration)
5. [Authentication](#authentication)
6. [Deployment](#deployment)

## ChatKit Overview

**OpenAI ChatKit** is a pre-built React component for creating chat interfaces that connect to OpenAI agents. It handles:

- Message display and formatting
- User input
- Streaming responses
- File uploads (if enabled)
- Conversation management

### When to Use ChatKit

- **Quick prototypes**: Get a chat UI running in minutes
- **Standard chat interfaces**: When you need a simple, polished chat experience
- **OpenAI integration**: Works seamlessly with OpenAI Agents SDK

## Installation and Setup

### Install ChatKit

```bash
npm install @openai/chatkit
```

### Basic Next.js Setup

```typescript
// app/page.tsx
'use client'

import { ChatKit } from '@openai/chatkit'
import '@openai/chatkit/styles.css'

export default function Home() {
  return (
    <div className="h-screen">
      <ChatKit
        apiUrl="/api/chat"
        welcomeMessage="Hello! I'm your todo assistant. How can I help you today?"
      />
    </div>
  )
}
```

## Basic Configuration

### ChatKit Props

```typescript
interface ChatKitProps {
  // Required
  apiUrl: string  // Backend endpoint for chat

  // Optional
  welcomeMessage?: string
  placeholder?: string
  headers?: Record<string, string>  // Custom headers (e.g., auth tokens)
  conversationId?: string  // Resume existing conversation
  onMessageSent?: (message: string) => void
  onResponseReceived?: (response: string) => void
  onError?: (error: Error) => void
  streamingEnabled?: boolean  // Enable streaming responses
  maxHeight?: string
  className?: string
}
```

### Example Configuration

```typescript
'use client'

import { ChatKit } from '@openai/chatkit'
import { useState, useEffect } from 'react'

export default function ChatPage() {
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [authToken, setAuthToken] = useState<string>('')

  useEffect(() => {
    // Get auth token from session
    const token = localStorage.getItem('auth_token')
    if (token) setAuthToken(token)
  }, [])

  return (
    <div className="container mx-auto h-screen p-4">
      <ChatKit
        apiUrl="/api/chat"
        welcomeMessage="Welcome to your Todo Assistant! You can ask me to add tasks, list your todos, mark them complete, and more."
        placeholder="Type your message... (e.g., 'Add task to buy groceries')"
        headers={{
          'Authorization': `Bearer ${authToken}`
        }}
        conversationId={conversationId ?? undefined}
        onMessageSent={(msg) => console.log('Sent:', msg)}
        onResponseReceived={(resp) => console.log('Received:', resp)}
        onError={(err) => console.error('Chat error:', err)}
        streamingEnabled={true}
        maxHeight="calc(100vh - 100px)"
        className="shadow-lg rounded-lg"
      />
    </div>
  )
}
```

## Backend Integration

### Expected API Contract

ChatKit expects your backend endpoint to:

1. Accept POST requests with message payload
2. Return JSON response with assistant message
3. Optionally support streaming

### Request Format

```typescript
// POST /api/chat
{
  "message": "Add task to buy groceries",
  "conversation_id": 123  // Optional, for resuming conversations
}
```

### Response Format

```typescript
// Response
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your todo list.",
  "tool_calls": [  // Optional, for debugging
    {
      "name": "add_task",
      "arguments": {
        "title": "Buy groceries"
      }
    }
  ]
}
```

### Next.js API Route Example

```typescript
// app/api/chat/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { message, conversation_id } = await request.json()

    // Get user from auth token
    const authHeader = request.headers.get('authorization')
    const token = authHeader?.replace('Bearer ', '')
    const userId = await getUserFromToken(token)

    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    // Call backend agent API
    const response = await fetch(`${process.env.BACKEND_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id
      })
    })

    if (!response.ok) {
      throw new Error('Backend request failed')
    }

    const data = await response.json()

    return NextResponse.json({
      conversation_id: data.conversation_id,
      response: data.response,
      tool_calls: data.tool_calls  // Optional
    })

  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: 'Failed to process message' },
      { status: 500 }
    )
  }
}
```

### FastAPI Backend Integration

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "https://your-app.vercel.app"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[list] = None

@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest):
    """Chat endpoint for ChatKit."""

    # Load conversation history
    messages = fetch_history(user_id, request.conversation_id)
    messages.append({"role": "user", "content": request.message})

    # Run agent with MCP tools
    runner = Runner(client=client, agent=agent)
    response = runner.run(messages=messages)

    # Execute tools (if needed)
    while response.status == "requires_action":
        # ... execute MCP tools
        pass

    # Get final response
    final_message = response.messages[-1]

    # Save to database
    conversation = save_conversation(user_id, request.conversation_id, messages, final_message)

    return ChatResponse(
        conversation_id=conversation.id,
        response=final_message["content"],
        tool_calls=extract_tool_calls(response)
    )
```

## Authentication

### Better Auth Integration

ChatKit works with Better Auth JWT tokens:

```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth/client'

export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL,
  plugins: [
    // Enable JWT
    jwt({
      expiresIn: '7d',
      secret: process.env.BETTER_AUTH_SECRET
    })
  ]
})

// Get token for ChatKit
export async function getAuthToken(): Promise<string | null> {
  const session = await auth.getSession()
  return session?.jwt ?? null
}
```

### Protected Chat Component

```typescript
'use client'

import { ChatKit } from '@openai/chatkit'
import { useSession } from '@/lib/auth'
import { useEffect, useState } from 'react'

export default function ProtectedChat() {
  const { data: session, status } = useSession()
  const [token, setToken] = useState<string>('')

  useEffect(() => {
    if (session?.jwt) {
      setToken(session.jwt)
    }
  }, [session])

  if (status === 'loading') {
    return <div>Loading...</div>
  }

  if (!session) {
    return <div>Please sign in to use the chat.</div>
  }

  return (
    <ChatKit
      apiUrl="/api/chat"
      headers={{
        'Authorization': `Bearer ${token}`
      }}
      welcomeMessage={`Welcome back, ${session.user.name}!`}
    />
  )
}
```

### Backend Token Verification

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify JWT token and return user_id."""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    authenticated_user_id: str = Depends(verify_token)
):
    """Protected chat endpoint."""

    # Ensure user can only access their own chat
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Process chat
    # ...
```

## Deployment

### Domain Allowlist (Required for Production)

Before deploying ChatKit to production, configure OpenAI's domain allowlist:

1. **Deploy your frontend** to get production URL:
   - Vercel: `https://your-app.vercel.app`
   - Custom domain: `https://yourdomain.com`

2. **Add domain to OpenAI allowlist**:
   - Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
   - Click "Add domain"
   - Enter your frontend URL (without trailing slash)
   - Save changes

3. **Get domain key**:
   - OpenAI provides a domain key after adding
   - Add to environment variables

### Environment Variables

```bash
# .env.local (Next.js frontend)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
NEXT_PUBLIC_AUTH_URL=https://your-app.vercel.app
BETTER_AUTH_SECRET=your-secret
BACKEND_URL=https://your-backend.com

# Backend
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
BETTER_AUTH_SECRET=your-secret
```

### Vercel Deployment

```bash
# Deploy frontend
npm run build
vercel deploy --prod

# Configure environment variables in Vercel dashboard
# Settings > Environment Variables
```

### Backend Deployment

```bash
# Docker deployment
docker build -t todo-agent-backend .
docker run -p 8000:8000 \
  -e DATABASE_URL=$DATABASE_URL \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  todo-agent-backend
```

### CORS Configuration for Production

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Dev
        "https://your-app.vercel.app",  # Prod
        "https://yourdomain.com"  # Custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Testing Deployment

```bash
# Test frontend → backend connection
curl -X POST https://your-app.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -d '{"message": "Hello"}'

# Test backend directly
curl -X POST https://your-backend.com/api/test_user/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add task to test deployment"}'
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| CORS errors | Check allow_origins in backend CORS config |
| Domain not allowed | Add domain to OpenAI allowlist |
| 401 Unauthorized | Verify JWT token is being sent in headers |
| Connection refused | Check backend URL and ensure it's accessible |
| Conversation not resuming | Verify conversation_id is being persisted |

### Debug Mode

```typescript
<ChatKit
  apiUrl="/api/chat"
  onError={(error) => {
    console.error('ChatKit error:', error)
    // Send to error tracking service
  }}
  onMessageSent={(msg) => console.log('Sent:', msg)}
  onResponseReceived={(resp) => console.log('Received:', resp)}
/>
```
