package cmd

import (
	"fmt"
	"io"
	"os"
	"strings"

	"github.com/johntheyoung/roadrunner/internal/errfmt"
)

func readFileOrStdin(path string) ([]byte, error) {
	if path == "-" {
		data, err := io.ReadAll(os.Stdin)
		if err != nil {
			return nil, fmt.Errorf("read stdin: %w", err)
		}
		return data, nil
	}

	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read file %s: %w", path, err)
	}
	return data, nil
}

func resolveTextInput(text, file string, stdin bool, required bool, label, fileFlag, stdinFlag string) (string, error) {
	sources := 0
	if text != "" {
		sources++
	}
	if file != "" {
		sources++
	}
	if stdin {
		sources++
	}

	if sources == 0 {
		if required {
			return "", errfmt.UsageError("%s is required", label)
		}
		return "", nil
	}
	if sources > 1 {
		choices := []string{label}
		if fileFlag != "" {
			choices = append(choices, fileFlag)
		}
		if stdinFlag != "" {
			choices = append(choices, stdinFlag)
		}
		return "", errfmt.UsageError("use only one of %s", strings.Join(choices, ", "))
	}

	if file != "" {
		data, err := readFileOrStdin(file)
		if err != nil {
			return "", err
		}
		text = string(data)
	} else if stdin {
		data, err := readFileOrStdin("-")
		if err != nil {
			return "", err
		}
		text = string(data)
	}

	if required && strings.TrimSpace(text) == "" {
		return "", errfmt.UsageError("%s is required", label)
	}

	return text, nil
}
