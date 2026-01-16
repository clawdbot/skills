package outfmt

import "testing"

func TestFromFlags(t *testing.T) {
	mode, err := FromFlags(false, false)
	if err != nil {
		t.Fatalf("FromFlags(false,false) error: %v", err)
	}
	if mode.JSON || mode.Plain {
		t.Fatalf("FromFlags(false,false) = %+v, want both false", mode)
	}

	mode, err = FromFlags(true, false)
	if err != nil {
		t.Fatalf("FromFlags(true,false) error: %v", err)
	}
	if !mode.JSON || mode.Plain {
		t.Fatalf("FromFlags(true,false) = %+v, want JSON only", mode)
	}

	if _, err = FromFlags(true, true); err == nil {
		t.Fatal("FromFlags(true,true) expected error")
	}
}
