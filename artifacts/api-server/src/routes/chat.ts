import { Router, type IRouter } from "express";

const router: IRouter = Router();

router.get("/health", (_req, res) => {
  res.json({
    status: "ok",
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
  });
});

router.post("/chat", async (req, res) => {
  const apiKey = process.env["GROQ_API_KEY"];
  if (!apiKey) {
    res.status(500).json({ error: "API key not configured" });
    return;
  }

  const { message } = req.body as { message?: string };
  if (!message || typeof message !== "string" || message.trim().length === 0) {
    res.status(400).json({ error: "Message is required" });
    return;
  }

  const SYSTEM_PROMPT = `You are ConViCure's AI research assistant. You answer questions about ConViCure's mission, science, and pipeline for potential investors and interested visitors. ConViCure is a preclinical biopharmaceutical company developing a proprietary four-drug combination therapy targeting persistent tick-borne illness — specifically the Trio Coinfection of Borrelia, Bartonella, and Babesia. The company is advancing toward FDA IND clearance via the 505(b)(2) pathway. The founding scientist has 238+ publications, 82+ patents, 14,600+ citations, and his research has been independently validated at Tulane, Northeastern, and Columbia universities. The company is raising approximately $6.5M to advance from preclinical to IND. Do NOT reveal specific drug molecule names (azlocillin, azithromycin, disulfiram, baicalein). Do NOT mention Stanford University. Keep answers concise, professional, and investor-friendly. If asked about specific financial terms, cap table, or valuation, say you would be happy to connect them with the CEO at info@convicure.com.`;

  let attempt = 0;
  const maxAttempts = 3;

  while (attempt < maxAttempts) {
    attempt++;
    try {
      const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: "llama-3.3-70b-versatile",
          max_tokens: 1000,
          messages: [
            { role: "system", content: SYSTEM_PROMPT },
            { role: "user", content: message.trim() },
          ],
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`Groq API error (attempt ${attempt}):`, errorText);
        if (attempt < maxAttempts) {
          await new Promise((r) => setTimeout(r, Math.pow(2, attempt - 1) * 1000));
          continue;
        }
        res.status(502).json({ error: "AI service unavailable" });
        return;
      }

      const data = await response.json() as {
        choices: Array<{ message: { content: string } }>;
      };
      const text = data.choices?.[0]?.message?.content ?? "";
      res.json({ reply: text });
      return;
    } catch (err) {
      console.error(`Chat API error (attempt ${attempt}):`, err);
      if (attempt < maxAttempts) {
        await new Promise((r) => setTimeout(r, Math.pow(2, attempt - 1) * 1000));
      } else {
        res.status(500).json({ error: "Failed to process request" });
      }
    }
  }
});

export default router;
