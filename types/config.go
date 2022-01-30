package types

type (
	Global struct {
		Interval uint64
	}

	Config struct {
		Global   Global
		Provider interface{}
	}
)
