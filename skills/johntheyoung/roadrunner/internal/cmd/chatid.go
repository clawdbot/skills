package cmd

// normalizeChatID strips any leading backslashes before a Matrix-style chat ID.
// This protects against shell history expansion artifacts like "\\!room".
func normalizeChatID(id string) string {
	if id == "" {
		return id
	}

	i := 0
	for i < len(id) && id[i] == '\\' {
		i++
	}

	if i > 0 && i < len(id) && id[i] == '!' {
		return id[i:]
	}

	return id
}

func normalizeChatIDs(ids []string) []string {
	if len(ids) == 0 {
		return ids
	}

	out := make([]string, len(ids))
	for i, id := range ids {
		out[i] = normalizeChatID(id)
	}
	return out
}
