package cmd

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"

	"golang.org/x/term"

	"github.com/johntheyoung/roadrunner/internal/errfmt"
)

func confirmDestructive(flags *RootFlags, action string) error {
	if flags.Force {
		return nil
	}

	if flags.NoInput || !term.IsTerminal(int(os.Stdin.Fd())) {
		return errfmt.UsageError("refusing to %s without --force (non-interactive)", action)
	}

	_, _ = fmt.Fprintf(os.Stderr, "Proceed to %s? [y/N]: ", action)
	reader := bufio.NewReader(os.Stdin)
	line, err := reader.ReadString('\n')
	if err != nil && !errors.Is(err, io.EOF) {
		return fmt.Errorf("read confirmation: %w", err)
	}

	ans := strings.TrimSpace(strings.ToLower(line))
	if ans == "y" || ans == "yes" {
		return nil
	}

	return errfmt.WithCode(errors.New("cancelled"), errfmt.ExitFailure)
}
