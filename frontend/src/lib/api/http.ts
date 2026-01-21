type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(status: number, message: string, detail?: unknown) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL as string | undefined;

function getBaseUrl(): string {
  if (!BASE_URL) {
    throw new Error("VITE_API_BASE_URL is not set. Create frontend/.env");
  }
  return BASE_URL.replace(/\/$/, "");
}

export async function apiRequest<T>(
  path: string,
  options: {
    method?: HttpMethod;
    body?: unknown;
    signal?: AbortSignal;
  } = {}
): Promise<T> {
  const url = `${getBaseUrl()}${path.startsWith("/") ? "" : "/"}${path}`;

  const res = await fetch(url, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
    },
    body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
    signal: options.signal,
  });

  const contentType = res.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");

  const payload = isJson ? await res.json().catch(() => null) : await res.text().catch(() => "");

  if (!res.ok) {
    const detail = (payload && (payload.detail ?? payload)) ?? payload;
    throw new ApiError(res.status, `Request failed: ${res.status}`, detail);
  }

  return payload as T;
}
