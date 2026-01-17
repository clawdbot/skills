package ui

import (
	"context"
	"fmt"
	"io"
	"os"
	"strings"
	"text/tabwriter"

	"github.com/muesli/termenv"
)

// Options configures UI output.
type Options struct {
	Stdout io.Writer
	Stderr io.Writer
	Color  string // auto|always|never
}

const colorNever = "never"

// UI provides formatted output to stdout and stderr.
type UI struct {
	out *Printer
	err *Printer
}

// ParseError is returned for invalid color option.
type ParseError struct {
	Msg string
}

func (e *ParseError) Error() string { return e.Msg }

// New creates a UI with the given options.
func New(opts Options) (*UI, error) {
	if opts.Stdout == nil {
		opts.Stdout = os.Stdout
	}

	if opts.Stderr == nil {
		opts.Stderr = os.Stderr
	}

	colorMode := strings.ToLower(strings.TrimSpace(opts.Color))
	if colorMode == "" {
		colorMode = "auto"
	}

	if colorMode != "auto" && colorMode != "always" && colorMode != colorNever {
		return nil, &ParseError{Msg: "invalid --color (expected auto|always|never)"}
	}

	out := termenv.NewOutput(opts.Stdout, termenv.WithProfile(termenv.EnvColorProfile()))
	errOut := termenv.NewOutput(opts.Stderr, termenv.WithProfile(termenv.EnvColorProfile()))

	outProfile := chooseProfile(out.Profile, colorMode)
	errProfile := chooseProfile(errOut.Profile, colorMode)

	return &UI{
		out: newPrinter(out, outProfile),
		err: newPrinter(errOut, errProfile),
	}, nil
}

func chooseProfile(detected termenv.Profile, mode string) termenv.Profile {
	if termenv.EnvNoColor() {
		return termenv.Ascii
	}

	switch mode {
	case colorNever:
		return termenv.Ascii
	case "always":
		return termenv.TrueColor
	default:
		return detected
	}
}

// Out returns the stdout printer.
func (u *UI) Out() *Printer { return u.out }

// Err returns the stderr printer.
func (u *UI) Err() *Printer { return u.err }

// Printer handles formatted output to a stream.
type Printer struct {
	o       *termenv.Output
	profile termenv.Profile
}

func newPrinter(o *termenv.Output, profile termenv.Profile) *Printer {
	return &Printer{o: o, profile: profile}
}

// ColorEnabled returns true if colors are enabled.
func (p *Printer) ColorEnabled() bool { return p.profile != termenv.Ascii }

func (p *Printer) line(s string) {
	_, _ = io.WriteString(p.o, s+"\n")
}

// Print writes a string without newline.
func (p *Printer) Print(msg string) {
	_, _ = io.WriteString(p.o, msg)
}

// Println writes a line.
func (p *Printer) Println(msg string) {
	p.line(msg)
}

// Printf writes a formatted line.
func (p *Printer) Printf(format string, args ...any) {
	p.line(fmt.Sprintf(format, args...))
}

// Success writes a green success message.
func (p *Printer) Success(msg string) {
	if p.ColorEnabled() {
		msg = termenv.String(msg).Foreground(p.profile.Color("#22c55e")).String()
	}
	p.line(msg)
}

// Successf writes a formatted green success message.
func (p *Printer) Successf(format string, args ...any) {
	p.Success(fmt.Sprintf(format, args...))
}

// Error writes a red error message.
func (p *Printer) Error(msg string) {
	if p.ColorEnabled() {
		msg = termenv.String(msg).Foreground(p.profile.Color("#ef4444")).String()
	}
	p.line(msg)
}

// Errorf writes a formatted red error message.
func (p *Printer) Errorf(format string, args ...any) {
	p.Error(fmt.Sprintf(format, args...))
}

// Warn writes a yellow warning message.
func (p *Printer) Warn(msg string) {
	if p.ColorEnabled() {
		msg = termenv.String(msg).Foreground(p.profile.Color("#eab308")).String()
	}
	p.line(msg)
}

// Warnf writes a formatted yellow warning message.
func (p *Printer) Warnf(format string, args ...any) {
	p.Warn(fmt.Sprintf(format, args...))
}

// Dim writes a dimmed message.
func (p *Printer) Dim(msg string) {
	if p.ColorEnabled() {
		msg = termenv.String(msg).Faint().String()
	}
	p.line(msg)
}

// Bold writes a bold message.
func (p *Printer) Bold(msg string) {
	if p.ColorEnabled() {
		msg = termenv.String(msg).Bold().String()
	}
	p.line(msg)
}

// Writer returns the underlying writer for use with tabwriter etc.
func (p *Printer) Writer() io.Writer {
	return p.o
}

// Table returns a new tabwriter for aligned output.
func (p *Printer) Table() *tabwriter.Writer {
	return tabwriter.NewWriter(p.o, 0, 0, 2, ' ', 0)
}

// Truncate shortens a string to maxLen, adding "..." if truncated.
func Truncate(s string, maxLen int) string {
	s = strings.ReplaceAll(s, "\n", " ")
	s = strings.TrimSpace(s)
	if len(s) <= maxLen {
		return s
	}
	if maxLen <= 3 {
		return s[:maxLen]
	}
	return s[:maxLen-3] + "..."
}

type ctxKey struct{}

// WithUI attaches UI to context.
func WithUI(ctx context.Context, u *UI) context.Context {
	return context.WithValue(ctx, ctxKey{}, u)
}

// FromContext retrieves UI from context.
func FromContext(ctx context.Context) *UI {
	v := ctx.Value(ctxKey{})
	if v == nil {
		return nil
	}
	u, _ := v.(*UI)
	return u
}
