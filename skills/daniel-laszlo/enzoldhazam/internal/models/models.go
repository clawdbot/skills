package models

// Thermostat represents a single thermostat/room in the ICON system
type Thermostat struct {
	ID    string  `json:"ID"`
	Title string  `json:"title"`
	Temp  float64 `json:"TEMP"` // Current temperature
	Req   float64 `json:"REQ"`  // Target/requested temperature
	RH    float64 `json:"RH"`   // Relative humidity %
	TMin  float64 `json:"TMIN"` // Minimum allowed temperature
	TMax  float64 `json:"TMAX"` // Maximum allowed temperature
}

// Icon represents the ICON device data
type Icon struct {
	SNR    string       `json:"SNR"`    // Serial number
	Name   string       `json:"NAME"`   // Device name
	Online int          `json:"ONLINE"` // Online status (1 = online)
	WTemp  float64      `json:"WTEMP"`  // Water temperature
	ETemp  float64      `json:"ETEMP"`  // External temperature
	Pump   int          `json:"PUMP"`   // Pump status
	DP     []Thermostat `json:"DP"`     // Thermostats array
}

// DeviceResponse represents the full response from iconByID
type DeviceResponse struct {
	Token string `json:"token"`
	User  string `json:"user"`
	ICON  Icon   `json:"ICON"`
}

// DeviceListResponse represents the response from iconList
type DeviceListResponse struct {
	Token     string          `json:"token"`
	User      string          `json:"user"`
	IconCodes []string        `json:"ICON_code"`
	Icons     map[string]Icon `json:"ICONS"`
}

// WriteStatus represents the WRITE part of set response
type WriteStatus struct {
	Status int     `json:"status"`
	Data   float64 `json:"data"`
}

// SetInfo represents the SET part of set response
type SetInfo struct {
	SNR   string  `json:"SNR"`
	Term  string  `json:"TERM"`
	Attr  string  `json:"attr"`
	Value float64 `json:"value"`
}

// SetResponse represents the response from setThermostat
type SetResponse struct {
	Write WriteStatus `json:"WRITE"`
	Set   SetInfo     `json:"SET"`
}

