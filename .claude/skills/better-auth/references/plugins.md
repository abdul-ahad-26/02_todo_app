# Better Auth Plugins Reference

## Table of Contents

- [Two-Factor Authentication (2FA)](#two-factor-authentication-2fa)
- [Passkeys (WebAuthn)](#passkeys-webauthn)
- [Username Plugin](#username-plugin)
- [Magic Link](#magic-link)
- [Organizations](#organizations)
- [Admin Plugin](#admin-plugin)

---

## Two-Factor Authentication (2FA)

TOTP-based two-factor authentication with backup codes.

### Server Setup

```typescript
import { betterAuth } from "better-auth";
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  appName: "My App", // Used as TOTP issuer
  plugins: [
    twoFactor({
      issuer: "my-app-name", // Optional custom issuer
      rateLimit: {
        window: 60,
        max: 3, // Only 3 2FA attempts per minute
      },
    }),
  ],
});
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/react";
import { twoFactorClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [
    twoFactorClient({
      onTwoFactorRedirect() {
        window.location.href = "/2fa"; // Redirect when 2FA required
      },
    }),
  ],
});
```

### Enable 2FA for User

```typescript
// Enable 2FA (returns QR code URI and backup codes)
const { data } = await authClient.twoFactor.enable({
  password: "user-password",
});

// data.totpURI - Use for QR code generation
// data.backupCodes - Store securely for recovery
// data.secret - Encrypted TOTP secret

// Verify TOTP to complete setup
await authClient.twoFactor.verifyTotp({ code: "123456" });
```

### Verify 2FA on Sign In

```typescript
// After sign-in redirects to 2FA page
await authClient.twoFactor.verifyTotp({
  code: "123456",
  trustDevice: true, // Trust for 30 days
});

// Or use backup code
await authClient.twoFactor.verifyBackupCode({
  code: "backup-code-here",
});
```

### Disable 2FA

```typescript
await authClient.twoFactor.disable({
  password: "user-password",
});
```

### Database Schema Addition

```sql
-- twoFactor table (auto-generated)
CREATE TABLE "twoFactor" (
  "id" TEXT PRIMARY KEY,
  "userId" TEXT NOT NULL REFERENCES "user"("id") ON DELETE CASCADE,
  "secret" TEXT NOT NULL,
  "backupCodes" TEXT NOT NULL,
  "createdAt" TIMESTAMP DEFAULT NOW()
);
```

---

## Passkeys (WebAuthn)

Passwordless authentication using device biometrics or security keys.

### Installation

```bash
npm install @better-auth/passkey
```

### Server Setup

```typescript
import { betterAuth } from "better-auth";
import { passkey } from "@better-auth/passkey";

export const auth = betterAuth({
  plugins: [
    passkey({
      rpName: "My App", // Relying party name
      rpID: "localhost", // Domain (no protocol/port)
      origin: "http://localhost:3000", // Full origin URL
    }),
  ],
});
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/react";
import { passkeyClient } from "@better-auth/passkey/client";

export const authClient = createAuthClient({
  plugins: [passkeyClient()],
});
```

### Register Passkey

```typescript
// Register new passkey for authenticated user
await authClient.passkey.addPasskey({
  name: "My MacBook", // Optional device name
});
```

### Sign In with Passkey

```typescript
await authClient.signIn.passkey();
```

### List & Delete Passkeys

```typescript
// List user's passkeys
const { data } = await authClient.passkey.listPasskeys();

// Delete passkey
await authClient.passkey.deletePasskey({
  id: "passkey-id",
});
```

---

## Username Plugin

Add username-based authentication alongside email.

### Server Setup

```typescript
import { betterAuth } from "better-auth";
import { username } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [username()],
});
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/react";
import { usernameClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [usernameClient()],
});
```

### Usage

```typescript
// Sign up with username
await authClient.signUp.email({
  email: "user@example.com",
  password: "password123",
  name: "John Doe",
  username: "johndoe",
});

// Sign in with username
await authClient.signIn.username({
  username: "johndoe",
  password: "password123",
});
```

---

## Magic Link

Passwordless email authentication via magic links.

### Server Setup

```typescript
import { betterAuth } from "better-auth";
import { magicLink } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    magicLink({
      sendMagicLink: async ({ email, url, token }) => {
        // Send email with magic link
        await sendEmail({
          to: email,
          subject: "Sign in to My App",
          html: `<a href="${url}">Click to sign in</a>`,
        });
      },
      expiresIn: 300, // 5 minutes
    }),
  ],
});
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/react";
import { magicLinkClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [magicLinkClient()],
});
```

### Usage

```typescript
// Send magic link
await authClient.signIn.magicLink({
  email: "user@example.com",
  callbackURL: "/dashboard",
});

// User clicks link in email and is automatically signed in
```

---

## Organizations

Multi-tenant support with organizations, members, and roles.

### Server Setup

```typescript
import { betterAuth } from "better-auth";
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    organization({
      allowUserToCreateOrganization: true,
    }),
  ],
});
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/react";
import { organizationClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [organizationClient()],
});
```

### Usage

```typescript
// Create organization
const { data: org } = await authClient.organization.create({
  name: "My Company",
  slug: "my-company",
});

// List user's organizations
const { data: orgs } = await authClient.organization.list();

// Get organization details
const { data: org } = await authClient.organization.get({
  organizationId: "org-id",
});

// Invite member
await authClient.organization.inviteMember({
  organizationId: "org-id",
  email: "newmember@example.com",
  role: "member", // "owner", "admin", "member"
});

// Accept invitation
await authClient.organization.acceptInvitation({
  invitationId: "inv-id",
});

// Update member role
await authClient.organization.updateMemberRole({
  organizationId: "org-id",
  memberId: "member-id",
  role: "admin",
});

// Remove member
await authClient.organization.removeMember({
  organizationId: "org-id",
  memberId: "member-id",
});

// Set active organization (for session)
await authClient.organization.setActive({
  organizationId: "org-id",
});

// Get active organization
const { data } = await authClient.useActiveOrganization();
```

### Database Schema Additions

```sql
-- organization table
CREATE TABLE "organization" (
  "id" TEXT PRIMARY KEY,
  "name" TEXT NOT NULL,
  "slug" TEXT UNIQUE NOT NULL,
  "logo" TEXT,
  "createdAt" TIMESTAMP DEFAULT NOW()
);

-- member table
CREATE TABLE "member" (
  "id" TEXT PRIMARY KEY,
  "organizationId" TEXT NOT NULL REFERENCES "organization"("id"),
  "userId" TEXT NOT NULL REFERENCES "user"("id"),
  "role" TEXT NOT NULL DEFAULT 'member',
  "createdAt" TIMESTAMP DEFAULT NOW()
);

-- invitation table
CREATE TABLE "invitation" (
  "id" TEXT PRIMARY KEY,
  "organizationId" TEXT NOT NULL REFERENCES "organization"("id"),
  "email" TEXT NOT NULL,
  "role" TEXT NOT NULL,
  "status" TEXT DEFAULT 'pending',
  "expiresAt" TIMESTAMP NOT NULL
);
```

---

## Admin Plugin

Administration dashboard and user management.

### Server Setup

```typescript
import { betterAuth } from "better-auth";
import { admin } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    admin({
      defaultRole: "user",
      adminRole: "admin",
    }),
  ],
});
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/react";
import { adminClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [adminClient()],
});
```

### Usage (Admin Only)

```typescript
// List all users
const { data: users } = await authClient.admin.listUsers({
  limit: 10,
  offset: 0,
});

// Get user by ID
const { data: user } = await authClient.admin.getUser({
  userId: "user-id",
});

// Create user
await authClient.admin.createUser({
  email: "newuser@example.com",
  password: "password123",
  name: "New User",
  role: "user",
});

// Update user
await authClient.admin.updateUser({
  userId: "user-id",
  name: "Updated Name",
  role: "admin",
});

// Ban user
await authClient.admin.banUser({
  userId: "user-id",
});

// Unban user
await authClient.admin.unbanUser({
  userId: "user-id",
});

// Delete user
await authClient.admin.deleteUser({
  userId: "user-id",
});

// Impersonate user
await authClient.admin.impersonateUser({
  userId: "user-id",
});

// Stop impersonation
await authClient.admin.stopImpersonation();
```

### Database Schema Addition

Add `role` and `banned` columns to user table:

```sql
ALTER TABLE "user" ADD COLUMN "role" TEXT DEFAULT 'user';
ALTER TABLE "user" ADD COLUMN "banned" BOOLEAN DEFAULT FALSE;
ALTER TABLE "user" ADD COLUMN "banReason" TEXT;
ALTER TABLE "user" ADD COLUMN "banExpires" TIMESTAMP;
```
