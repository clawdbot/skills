# Challenge 6: Compressed NFTs

> Millions of NFTs for the cost of hundreds.

## Goal

Create compressed NFTs (cNFTs) using state compression. Understand Merkle trees and the cost savings.

## The Problem

Regular NFTs cost ~0.012 SOL each in rent. 1 million NFTs = 12,000 SOL (~$1M+).

## The Solution

Compressed NFTs store data in a Merkle tree. Only the tree root is on-chain.

Cost comparison for 1 million NFTs:
- Regular NFTs: ~12,000 SOL
- Compressed NFTs: ~5 SOL

## How It Works

```
Regular NFT:
  Mint Account (on-chain) + Metadata Account (on-chain)

Compressed NFT:
  Merkle Tree Root (on-chain) + Leaf Data (off-chain/indexed)
```

The Merkle tree proves ownership without storing each NFT on-chain.

## Setup

```bash
# Install Metaplex Bubblegum CLI
npm install -g @metaplex-foundation/mpl-bubblegum
```

## Create a Merkle Tree

```typescript
import { createTree } from '@metaplex-foundation/mpl-bubblegum';
import { generateSigner } from '@metaplex-foundation/umi';

// Tree size determines max NFTs
// maxDepth=14, maxBufferSize=64 = ~16,000 NFTs
const merkleTree = generateSigner(umi);

await createTree(umi, {
  merkleTree,
  maxDepth: 14,
  maxBufferSize: 64,
  public: false,
}).sendAndConfirm(umi);
```

## Tree Sizing

| Max Depth | Max NFTs | Approx Cost |
|-----------|----------|-------------|
| 14 | 16,384 | 0.15 SOL |
| 20 | 1,048,576 | 1.5 SOL |
| 24 | 16,777,216 | 6 SOL |
| 30 | 1,073,741,824 | 50 SOL |

## Mint Compressed NFT

```typescript
import { mintV1 } from '@metaplex-foundation/mpl-bubblegum';

await mintV1(umi, {
  leafOwner: recipientPublicKey,
  merkleTree: merkleTree.publicKey,
  metadata: {
    name: 'My cNFT',
    symbol: 'CNFT',
    uri: 'https://arweave.net/...',
    sellerFeeBasisPoints: 500,
    collection: null,
    creators: [
      { address: creatorPublicKey, verified: false, share: 100 },
    ],
  },
}).sendAndConfirm(umi);
```

## Reading Compressed NFTs

cNFTs are NOT queryable from on-chain accounts. You need an indexer:

```typescript
// Using Helius DAS API
const response = await fetch(
  `https://mainnet.helius-rpc.com/?api-key=${API_KEY}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 'my-id',
      method: 'getAssetsByOwner',
      params: {
        ownerAddress: walletAddress,
        page: 1,
        limit: 100,
      },
    }),
  }
);
```

## Transferring cNFTs

Transfers require a proof from the Merkle tree:

```typescript
import { transfer } from '@metaplex-foundation/mpl-bubblegum';

// Get asset proof from indexer
const proof = await getAssetProof(assetId);

await transfer(umi, {
  leafOwner: currentOwner,
  newLeafOwner: newOwner,
  merkleTree: merkleTree.publicKey,
  root: proof.root,
  dataHash: proof.dataHash,
  creatorHash: proof.creatorHash,
  nonce: proof.nonce,
  index: proof.index,
  proof: proof.proof,
}).sendAndConfirm(umi);
```

## Key Programs

```
Bubblegum:           BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY
Account Compression: cmtDvXumGCrqC1Age74AVPhSRVXJMd8PJS91L8KbNCK
Noop:                noopb9bkMVfRPU8AsbpTUg8AQkHtKwMYZiFUjNRtMmV
```

## Indexers

cNFTs require indexers to query:
- Helius DAS API
- Triton
- SimpleHash
- Hello Moon

## Gotchas

1. Cannot query cNFTs from on-chain - need indexer
2. Transfers need Merkle proofs
3. Tree size is fixed at creation
4. Concurrent mints need buffer space
5. Tree authority controls minting

## When to Use

Use compressed NFTs for:
- Large collections (10k+)
- Gaming assets
- Loyalty/reward programs
- Any high-volume NFT use case

Use regular NFTs for:
- Small collections
- When on-chain queryability matters
- Maximum marketplace compatibility

## Next

Challenge 7: Oracle (Pyth)
