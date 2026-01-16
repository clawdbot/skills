package main

import (
	"os"

	"github.com/johntheyoung/roadrunner/internal/cmd"
)

func main() {
	os.Exit(cmd.Execute())
}
