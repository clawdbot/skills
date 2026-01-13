#!/usr/bin/env bash
# Gamma.app API CLI
# Generate presentations, documents, and social posts

set -euo pipefail

API_BASE="https://public-api.gamma.app/v1.0"

# Check for API key
if [[ -z "${GAMMA_API_KEY:-}" ]]; then
    echo "Error: GAMMA_API_KEY environment variable not set" >&2
    exit 1
fi

usage() {
    cat << 'EOF'
Usage: gamma.sh <command> [options]

Commands:
  generate <content>    Generate a new presentation/document/social post
  status <id>          Check generation status
  help                 Show this help

Generate Options:
  --format <type>       presentation|document|social (default: presentation)
  --cards <num>         Number of cards/slides (default: 10)
  --instructions <str>  Additional styling instructions
  --amount <type>       concise|detailed (default: detailed)
  --tone <str>          e.g., "professional", "casual"
  --audience <str>      e.g., "investors", "developers"
  --image-source <type> aiGenerated|web|none (default: aiGenerated)
  --image-style <type>  illustration|photo (default: illustration)
  --dimensions <type>   fluid|16x9|4x3|1x1|4x5|9x16 (default: fluid)
  --wait                Wait for completion and return URL
  --poll-interval <sec> Seconds between status checks (default: 10)
  --max-wait <sec>      Maximum wait time in seconds (default: 300)

Examples:
  gamma.sh generate "AI automation trends" --wait
  gamma.sh generate "$(cat content.md)" --format presentation --cards 12 --wait
  gamma.sh status abc123xyz
EOF
}

# API request helper
api_request() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    
    local url="${API_BASE}${endpoint}"
    local args=(
        -s
        -X "$method"
        -H "X-API-KEY: ${GAMMA_API_KEY}"
        -H "Content-Type: application/json"
    )
    
    if [[ -n "$data" ]]; then
        args+=(-d "$data")
    fi
    
    curl "${args[@]}" "$url"
}

# Generate command
cmd_generate() {
    local content=""
    local format="presentation"
    local cards=10
    local instructions=""
    local amount="detailed"
    local tone=""
    local audience=""
    local image_source="aiGenerated"
    local image_style="illustration"
    local dimensions="fluid"
    local wait_for_completion=false
    local poll_interval=10
    local max_wait=300
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --format)
                format="$2"
                shift 2
                ;;
            --cards)
                cards="$2"
                shift 2
                ;;
            --instructions)
                instructions="$2"
                shift 2
                ;;
            --amount)
                amount="$2"
                shift 2
                ;;
            --tone)
                tone="$2"
                shift 2
                ;;
            --audience)
                audience="$2"
                shift 2
                ;;
            --image-source)
                image_source="$2"
                shift 2
                ;;
            --image-style)
                image_style="$2"
                shift 2
                ;;
            --dimensions)
                dimensions="$2"
                shift 2
                ;;
            --wait)
                wait_for_completion=true
                shift
                ;;
            --poll-interval)
                poll_interval="$2"
                shift 2
                ;;
            --max-wait)
                max_wait="$2"
                shift 2
                ;;
            -*)
                echo "Unknown option: $1" >&2
                exit 1
                ;;
            *)
                if [[ -z "$content" ]]; then
                    content="$1"
                fi
                shift
                ;;
        esac
    done
    
    if [[ -z "$content" ]]; then
        echo "Error: Content is required" >&2
        echo "Usage: gamma.sh generate <content> [options]" >&2
        exit 1
    fi
    
    # Build request JSON
    local json_content
    json_content=$(printf '%s' "$content" | jq -Rs .)
    
    local body
    body=$(jq -n \
        --argjson inputText "$json_content" \
        --arg format "$format" \
        --argjson numCards "$cards" \
        --arg amount "$amount" \
        --arg imageSource "$image_source" \
        --arg imageStyle "$image_style" \
        --arg dimensions "$dimensions" \
        '{
            inputText: $inputText,
            textMode: "generate",
            format: $format,
            numCards: $numCards,
            textOptions: {
                amount: $amount
            },
            imageOptions: {
                source: $imageSource,
                model: "flux-kontext-pro",
                style: $imageStyle
            },
            cardOptions: {
                dimensions: $dimensions
            }
        }')
    
    # Add optional fields
    if [[ -n "$instructions" ]]; then
        body=$(echo "$body" | jq --arg v "$instructions" '. + {additionalInstructions: $v}')
    fi
    if [[ -n "$tone" ]]; then
        body=$(echo "$body" | jq --arg v "$tone" '.textOptions.tone = $v')
    fi
    if [[ -n "$audience" ]]; then
        body=$(echo "$body" | jq --arg v "$audience" '.textOptions.audience = $v')
    fi
    
    # Make request
    local response
    response=$(api_request POST "/generations" "$body")
    
    local generation_id
    generation_id=$(echo "$response" | jq -r '.generationId // empty')
    
    if [[ -z "$generation_id" ]]; then
        echo "Error creating generation:" >&2
        echo "$response" >&2
        exit 1
    fi
    
    echo "Generation started: $generation_id"
    
    if [[ "$wait_for_completion" == true ]]; then
        echo "Waiting for completion..."
        local elapsed=0
        local status=""
        
        while [[ $elapsed -lt $max_wait ]]; do
            sleep "$poll_interval"
            elapsed=$((elapsed + poll_interval))
            
            response=$(api_request GET "/generations/${generation_id}")
            status=$(echo "$response" | jq -r '.status // empty')
            
            echo "  Status: $status (${elapsed}s elapsed)"
            
            if [[ "$status" == "completed" ]]; then
                local url
                url=$(echo "$response" | jq -r '.gammaUrl // empty')
                local credits_used
                credits_used=$(echo "$response" | jq -r '.credits.deducted // "unknown"')
                local credits_remaining
                credits_remaining=$(echo "$response" | jq -r '.credits.remaining // "unknown"')
                
                echo ""
                echo "✅ Generation complete!"
                echo "URL: $url"
                echo "Credits used: $credits_used"
                echo "Credits remaining: $credits_remaining"
                exit 0
            elif [[ "$status" == "failed" ]]; then
                echo "❌ Generation failed" >&2
                echo "$response" >&2
                exit 1
            fi
        done
        
        echo "⏱️ Timeout waiting for generation (${max_wait}s)" >&2
        echo "Check status manually: gamma.sh status $generation_id" >&2
        exit 1
    else
        echo "Use 'gamma.sh status $generation_id' to check progress"
        echo "Or add --wait to wait for completion"
    fi
}

# Status command
cmd_status() {
    local generation_id="${1:-}"
    
    if [[ -z "$generation_id" ]]; then
        echo "Error: Generation ID required" >&2
        echo "Usage: gamma.sh status <generationId>" >&2
        exit 1
    fi
    
    local response
    response=$(api_request GET "/generations/${generation_id}")
    
    local status
    status=$(echo "$response" | jq -r '.status // empty')
    
    if [[ -z "$status" ]]; then
        echo "Error checking status:" >&2
        echo "$response" >&2
        exit 1
    fi
    
    echo "Generation: $generation_id"
    echo "Status: $status"
    
    if [[ "$status" == "completed" ]]; then
        local url
        url=$(echo "$response" | jq -r '.gammaUrl // empty')
        local credits_used
        credits_used=$(echo "$response" | jq -r '.credits.deducted // "unknown"')
        
        echo "URL: $url"
        echo "Credits used: $credits_used"
    fi
}

# Main
case "${1:-help}" in
    generate)
        shift
        cmd_generate "$@"
        ;;
    status)
        shift
        cmd_status "$@"
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo "Unknown command: $1" >&2
        usage
        exit 1
        ;;
esac
