# Challenge 9: Blinks and Actions

> Shareable, executable transaction links.

## Goal

Create Solana Actions that can be shared as Blinks - URLs that unfurl into executable transactions.

## What Are Blinks?

Blinks (Blockchain Links) are URLs that:
1. Unfurl into a preview (like link cards)
2. Allow signing transactions directly
3. Work in Twitter, Discord, wallets, etc.

## How It Works

```
URL: https://yourapp.com/api/action/donate

1. Client fetches GET /api/action/donate
   -> Returns metadata (title, description, icon)

2. User clicks "Execute"
   -> Client POSTs with wallet pubkey
   -> Server returns unsigned transaction
   -> User signs and submits
```

## Actions API Spec

### GET Request (Metadata)

```typescript
// GET /api/action/donate
export async function GET(request: Request) {
  const payload: ActionGetResponse = {
    title: "Donate to the Forest",
    icon: "https://yourapp.com/icon.png",
    description: "Send SOL to support reforestation",
    label: "Donate",
    // Optional: multiple actions
    links: {
      actions: [
        { label: "0.1 SOL", href: "/api/action/donate?amount=0.1" },
        { label: "0.5 SOL", href: "/api/action/donate?amount=0.5" },
        { label: "1 SOL", href: "/api/action/donate?amount=1" },
      ],
    },
  };

  return Response.json(payload, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    },
  });
}
```

### POST Request (Transaction)

```typescript
// POST /api/action/donate
import { 
  Connection, 
  PublicKey, 
  Transaction, 
  SystemProgram,
  LAMPORTS_PER_SOL 
} from "@solana/web3.js";

export async function POST(request: Request) {
  const body = await request.json();
  const account = new PublicKey(body.account);
  
  const url = new URL(request.url);
  const amount = parseFloat(url.searchParams.get("amount") || "0.1");

  const connection = new Connection(process.env.RPC_URL!);

  const transaction = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: account,
      toPubkey: new PublicKey("RECIPIENT_ADDRESS"),
      lamports: amount * LAMPORTS_PER_SOL,
    })
  );

  transaction.feePayer = account;
  transaction.recentBlockhash = (
    await connection.getLatestBlockhash()
  ).blockhash;

  const payload: ActionPostResponse = {
    transaction: transaction
      .serialize({ requireAllSignatures: false })
      .toString("base64"),
    message: `Donating ${amount} SOL`,
  };

  return Response.json(payload, {
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  });
}
```

### OPTIONS (CORS)

```typescript
export async function OPTIONS() {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}
```

## actions.json

Host at your domain root to declare supported actions:

```json
// https://yourapp.com/actions.json
{
  "rules": [
    {
      "pathPattern": "/api/action/*",
      "apiPath": "/api/action/*"
    }
  ]
}
```

## Creating Blinks

Convert action URLs to blinks:
```
Action URL:  https://yourapp.com/api/action/donate
Blink URL:   https://dial.to/?action=solana-action:https://yourapp.com/api/action/donate
```

## Full Example: NFT Mint Action

```typescript
// GET /api/action/mint
export async function GET() {
  return Response.json({
    title: "Mint Forest NFT",
    icon: "https://yourapp.com/nft-preview.png",
    description: "Mint a unique forest-themed NFT",
    label: "Mint NFT",
  });
}

// POST /api/action/mint
export async function POST(request: Request) {
  const { account } = await request.json();
  const minter = new PublicKey(account);

  const connection = new Connection(process.env.RPC_URL!);
  
  // Build mint transaction
  // (simplified - real implementation would include Metaplex instructions)
  const transaction = new Transaction();
  
  // Add your mint instructions here
  // transaction.add(...)

  transaction.feePayer = minter;
  transaction.recentBlockhash = (
    await connection.getLatestBlockhash()
  ).blockhash;

  return Response.json({
    transaction: transaction
      .serialize({ requireAllSignatures: false })
      .toString("base64"),
    message: "Minting your Forest NFT",
  });
}
```

## Input Fields

Actions can request user input:

```typescript
// GET response with input
{
  title: "Send Tokens",
  description: "Send tokens to any address",
  label: "Send",
  links: {
    actions: [
      {
        label: "Send",
        href: "/api/action/send?to={to}&amount={amount}",
        parameters: [
          {
            name: "to",
            label: "Recipient Address",
            required: true,
          },
          {
            name: "amount",
            label: "Amount",
            required: true,
          },
        ],
      },
    ],
  },
}
```

## Security Considerations

1. Validate all input parameters
2. Set reasonable limits (max amounts, etc.)
3. Use allowlists for recipient addresses if applicable
4. Rate limit your endpoints
5. Don't trust client-provided data

## Testing

```bash
# Test GET
curl https://yourapp.com/api/action/donate

# Test POST
curl -X POST https://yourapp.com/api/action/donate \
  -H "Content-Type: application/json" \
  -d '{"account": "YOUR_WALLET_ADDRESS"}'
```

## Gotchas

1. CORS headers are required
2. Transaction must be serialized with `requireAllSignatures: false`
3. actions.json must be at domain root
4. Icons should be square, ideally 256x256
5. Keep descriptions concise for unfurl previews

## Resources

- Solana Actions Spec: https://solana.com/docs/advanced/actions
- Dialect Blinks: https://dial.to
- Actions SDK: @solana/actions
