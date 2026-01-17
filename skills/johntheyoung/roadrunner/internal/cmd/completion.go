package cmd

import (
	"fmt"
	"os"
)

// CompletionCmd generates shell completions.
type CompletionCmd struct {
	Shell string `arg:"" enum:"bash,zsh,fish" help:"Shell type (bash, zsh, fish)"`
}

// Run executes the completion command.
func (c *CompletionCmd) Run() error {
	switch c.Shell {
	case "bash":
		fmt.Print(bashCompletion)
	case "zsh":
		fmt.Print(zshCompletion)
	case "fish":
		fmt.Print(fishCompletion)
	default:
		fmt.Fprintf(os.Stderr, "Unknown shell: %s\n", c.Shell)
		return fmt.Errorf("unknown shell: %s", c.Shell)
	}
	return nil
}

const bashCompletion = `# rr bash completion
_rr_completions() {
    local cur prev commands
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    commands="auth accounts chats messages reminders search focus doctor version completion"
    auth_cmds="set status clear"
    accounts_cmds="list"
    chats_cmds="list search get archive"
    messages_cmds="list search send"
    reminders_cmds="set clear"

    case "${prev}" in
        rr)
            COMPREPLY=( $(compgen -W "${commands}" -- "${cur}") )
            return 0
            ;;
        auth)
            COMPREPLY=( $(compgen -W "${auth_cmds}" -- "${cur}") )
            return 0
            ;;
        accounts)
            COMPREPLY=( $(compgen -W "${accounts_cmds}" -- "${cur}") )
            return 0
            ;;
        chats)
            COMPREPLY=( $(compgen -W "${chats_cmds}" -- "${cur}") )
            return 0
            ;;
        messages)
            COMPREPLY=( $(compgen -W "${messages_cmds}" -- "${cur}") )
            return 0
            ;;
        reminders)
            COMPREPLY=( $(compgen -W "${reminders_cmds}" -- "${cur}") )
            return 0
            ;;
        completion)
            COMPREPLY=( $(compgen -W "bash zsh fish" -- "${cur}") )
            return 0
            ;;
    esac

    COMPREPLY=( $(compgen -W "${commands}" -- "${cur}") )
}
complete -F _rr_completions rr
`

const zshCompletion = `#compdef rr

_rr() {
    local -a commands
    commands=(
        'auth:Manage authentication'
        'accounts:Manage messaging accounts'
        'chats:Manage chats'
        'messages:Manage messages'
        'reminders:Manage chat reminders'
        'search:Global search across chats and messages'
        'focus:Focus Beeper Desktop app'
        'doctor:Diagnose configuration and connectivity'
        'version:Show version information'
        'completion:Generate shell completions'
    )

    local -a auth_cmds
    auth_cmds=(
        'set:Store API token'
        'status:Show authentication status'
        'clear:Remove stored token'
    )

    local -a accounts_cmds
    accounts_cmds=(
        'list:List connected messaging accounts'
    )

    local -a chats_cmds
    chats_cmds=(
        'list:List chats'
        'search:Search chats'
        'get:Get chat details'
        'archive:Archive or unarchive a chat'
    )

    local -a messages_cmds
    messages_cmds=(
        'list:List messages in a chat'
        'search:Search messages'
        'send:Send a message to a chat'
    )

    local -a reminders_cmds
    reminders_cmds=(
        'set:Set a reminder for a chat'
        'clear:Clear a reminder from a chat'
    )

    local -a completion_cmds
    completion_cmds=(
        'bash:Generate bash completions'
        'zsh:Generate zsh completions'
        'fish:Generate fish completions'
    )

    _arguments -C \
        '1: :->command' \
        '2: :->subcommand' \
        '*::arg:->args'

    case "$state" in
        command)
            _describe -t commands 'rr commands' commands
            ;;
        subcommand)
            case "$words[1]" in
                auth)
                    _describe -t commands 'auth commands' auth_cmds
                    ;;
                accounts)
                    _describe -t commands 'accounts commands' accounts_cmds
                    ;;
                chats)
                    _describe -t commands 'chats commands' chats_cmds
                    ;;
                messages)
                    _describe -t commands 'messages commands' messages_cmds
                    ;;
                reminders)
                    _describe -t commands 'reminders commands' reminders_cmds
                    ;;
                completion)
                    _describe -t commands 'completion commands' completion_cmds
                    ;;
            esac
            ;;
    esac
}

_rr "$@"
`

const fishCompletion = `# rr fish completion

# Disable file completion by default
complete -c rr -f

# Top-level commands
complete -c rr -n '__fish_use_subcommand' -a 'auth' -d 'Manage authentication'
complete -c rr -n '__fish_use_subcommand' -a 'accounts' -d 'Manage messaging accounts'
complete -c rr -n '__fish_use_subcommand' -a 'chats' -d 'Manage chats'
complete -c rr -n '__fish_use_subcommand' -a 'messages' -d 'Manage messages'
complete -c rr -n '__fish_use_subcommand' -a 'reminders' -d 'Manage chat reminders'
complete -c rr -n '__fish_use_subcommand' -a 'search' -d 'Global search across chats and messages'
complete -c rr -n '__fish_use_subcommand' -a 'focus' -d 'Focus Beeper Desktop app'
complete -c rr -n '__fish_use_subcommand' -a 'doctor' -d 'Diagnose configuration and connectivity'
complete -c rr -n '__fish_use_subcommand' -a 'version' -d 'Show version information'
complete -c rr -n '__fish_use_subcommand' -a 'completion' -d 'Generate shell completions'

# auth subcommands
complete -c rr -n '__fish_seen_subcommand_from auth' -a 'set' -d 'Store API token'
complete -c rr -n '__fish_seen_subcommand_from auth' -a 'status' -d 'Show authentication status'
complete -c rr -n '__fish_seen_subcommand_from auth' -a 'clear' -d 'Remove stored token'

# accounts subcommands
complete -c rr -n '__fish_seen_subcommand_from accounts' -a 'list' -d 'List connected messaging accounts'

# chats subcommands
complete -c rr -n '__fish_seen_subcommand_from chats' -a 'list' -d 'List chats'
complete -c rr -n '__fish_seen_subcommand_from chats' -a 'search' -d 'Search chats'
complete -c rr -n '__fish_seen_subcommand_from chats' -a 'get' -d 'Get chat details'
complete -c rr -n '__fish_seen_subcommand_from chats' -a 'archive' -d 'Archive or unarchive a chat'

# messages subcommands
complete -c rr -n '__fish_seen_subcommand_from messages' -a 'list' -d 'List messages in a chat'
complete -c rr -n '__fish_seen_subcommand_from messages' -a 'search' -d 'Search messages'
complete -c rr -n '__fish_seen_subcommand_from messages' -a 'send' -d 'Send a message to a chat'

# reminders subcommands
complete -c rr -n '__fish_seen_subcommand_from reminders' -a 'set' -d 'Set a reminder for a chat'
complete -c rr -n '__fish_seen_subcommand_from reminders' -a 'clear' -d 'Clear a reminder from a chat'

# completion subcommands
complete -c rr -n '__fish_seen_subcommand_from completion' -a 'bash' -d 'Generate bash completions'
complete -c rr -n '__fish_seen_subcommand_from completion' -a 'zsh' -d 'Generate zsh completions'
complete -c rr -n '__fish_seen_subcommand_from completion' -a 'fish' -d 'Generate fish completions'

# Global flags
complete -c rr -l help -s h -d 'Show help'
complete -c rr -l json -d 'Output JSON to stdout'
complete -c rr -l plain -d 'Output stable TSV to stdout'
complete -c rr -l verbose -s v -d 'Enable debug logging'
complete -c rr -l force -s f -d 'Skip confirmations'
complete -c rr -l timeout -d 'Timeout for API calls in seconds'
complete -c rr -l base-url -d 'API base URL'
complete -c rr -l version -d 'Show version and exit'
`
