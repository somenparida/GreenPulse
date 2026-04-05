package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestTelemetryJSONRoundTrip(t *testing.T) {
	b := Telemetry{
		PlotID:          "p1",
		MoisturePercent: 42.5,
		TemperatureC:    22.1,
		PH:              6.8,
	}
	var buf bytes.Buffer
	if err := json.NewEncoder(&buf).Encode(&b); err != nil {
		t.Fatal(err)
	}
	var got Telemetry
	if err := json.NewDecoder(&buf).Decode(&got); err != nil {
		t.Fatal(err)
	}
	if got.PlotID != b.PlotID || got.MoisturePercent != b.MoisturePercent {
		t.Fatalf("mismatch: %+v vs %+v", got, b)
	}
}

func TestLiveHandler(t *testing.T) {
	s := &Server{}
	req := httptest.NewRequest(http.MethodGet, "/health/live", nil)
	rr := httptest.NewRecorder()
	s.Live(rr, req)
	if rr.Code != http.StatusOK {
		t.Fatalf("status %d", rr.Code)
	}
}
