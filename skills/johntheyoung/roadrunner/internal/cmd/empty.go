package cmd

import (
	"fmt"

	"github.com/johntheyoung/roadrunner/internal/errfmt"
)

func failIfEmpty(enabled bool, count int, subject string) error {
	if !enabled || count > 0 {
		return nil
	}
	return errfmt.WithCode(fmt.Errorf("no %s found", subject), errfmt.ExitFailure)
}
