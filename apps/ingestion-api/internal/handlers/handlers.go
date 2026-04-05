package handlers

import (
	"context"
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

type Telemetry struct {
	PlotID          string  `json:"plot_id"`
	MoisturePercent float64 `json:"moisture_percent"`
	TemperatureC    float64 `json:"temperature_c"`
	PH              float64 `json:"ph"`
}

type Server struct {
	Pool *pgxpool.Pool
}

func (s *Server) Live(w http.ResponseWriter, _ *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("ok"))
}

func (s *Server) Ready(w http.ResponseWriter, r *http.Request) {
	ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
	defer cancel()
	if err := s.Pool.Ping(ctx); err != nil {
		http.Error(w, "db not ready", http.StatusServiceUnavailable)
		return
	}
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("ok"))
}

func (s *Server) Ingest(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	var body Telemetry
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, "invalid json", http.StatusBadRequest)
		return
	}
	if body.PlotID == "" {
		http.Error(w, "plot_id required", http.StatusBadRequest)
		return
	}
	ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
	defer cancel()
	_, err := s.Pool.Exec(ctx,
		`INSERT INTO telemetry_readings (plot_id, moisture_percent, temperature_c, ph) VALUES ($1,$2,$3,$4)`,
		body.PlotID, body.MoisturePercent, body.TemperatureC, body.PH,
	)
	if err != nil {
		http.Error(w, "persist failed", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusCreated)
	_, _ = w.Write([]byte(`{"status":"created"}`))
}

func (s *Server) Readings(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	limit := int64(50)
	if q := r.URL.Query().Get("limit"); q != "" {
		if n, err := strconv.ParseInt(q, 10, 64); err == nil && n > 0 && n <= 500 {
			limit = n
		}
	}
	ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
	defer cancel()
	rows, err := s.Pool.Query(ctx,
		`SELECT id, plot_id, moisture_percent, temperature_c, ph, created_at
		 FROM telemetry_readings ORDER BY created_at DESC LIMIT $1`, limit,
	)
	if err != nil {
		http.Error(w, "query failed", http.StatusInternalServerError)
		return
	}
	defer rows.Close()
	type row struct {
		ID              int64     `json:"id"`
		PlotID          string    `json:"plot_id"`
		MoisturePercent float64   `json:"moisture_percent"`
		TemperatureC    float64   `json:"temperature_c"`
		PH              float64   `json:"ph"`
		CreatedAt       time.Time `json:"created_at"`
	}
	var out []row
	for rows.Next() {
		var rec row
		if err := rows.Scan(&rec.ID, &rec.PlotID, &rec.MoisturePercent, &rec.TemperatureC, &rec.PH, &rec.CreatedAt); err != nil {
			http.Error(w, "scan failed", http.StatusInternalServerError)
			return
		}
		out = append(out, rec)
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(out)
}
