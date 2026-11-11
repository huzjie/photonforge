// TypeScript SDK：HTTP 客户端
export interface GenerateRequest {
  prompt: string;
  reference_images?: number[][][];
  ref_weights?: number[];
  steps?: number;
  guidance?: number;
  width?: number;
  height?: number;
}

export interface GenerateResponse {
  status: string;
  image: number[][][];
  elapsed: number;
}

export class PhotonforgeClient {
  constructor(private baseUrl = "http://127.0.0.1:8000", private token?: string) {}

  private headers(): Record<string, string> {
    const h: Record<string, string> = { "Content-Type": "application/json" };
    if (this.token) h["Authorization"] = `Bearer ${this.token}`;
    return h;
  }

  async health(): Promise<{ status: string }> {
    const res = await fetch(`${this.baseUrl}/health`);
    return res.json();
  }

  async generate(req: GenerateRequest): Promise<GenerateResponse> {
    const res = await fetch(`${this.baseUrl}/generate`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(req),
    });
    return res.json();
  }

  async edit(instruction: string, image: number[][][], strength = 0.75) {
    const res = await fetch(`${this.baseUrl}/edit`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify({ instruction, image, strength }),
    });
    return res.json();
  }
}
