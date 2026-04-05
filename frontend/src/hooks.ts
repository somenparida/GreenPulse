/**
 * Custom hooks for GreenPulse
 */

import { useState, useEffect, useCallback } from 'react'
import axios, { AxiosError } from 'axios'

interface UseFetchOptions {
  interval?: number
  enabled?: boolean
}

export function useFetch<T>(
  url: string,
  options: UseFetchOptions = {}
) {
  const { interval = 5000, enabled = true } = options
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const fetchData = useCallback(async () => {
    if (!enabled) return

    try {
      const response = await axios.get<T>(`${apiUrl}${url}`)
      setData(response.data)
      setError(null)
    } catch (err) {
      const errorMessage =
        err instanceof AxiosError
          ? err.response?.data?.message || err.message
          : 'An error occurred'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }, [url, enabled, apiUrl])

  useEffect(() => {
    fetchData()
    const intervalId = setInterval(fetchData, interval)
    return () => clearInterval(intervalId)
  }, [fetchData, interval])

  return { data, error, loading, refetch: fetchData }
}
