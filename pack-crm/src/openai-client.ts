/**
 * OpenAI Client
 * 
 * Minimal wrapper for OpenAI API calls.
 * Reads API key from process.env.OPENAI_API_KEY
 */

/**
 * Calls OpenAI API with a prompt and returns the markdown response
 * 
 * @param prompt The prompt to send to OpenAI
 * @param model Optional model name (default: "gpt-4")
 * @returns Promise<string> The markdown response
 */
export async function callOpenAI(
  prompt: string,
  model: string = 'gpt-4'
): Promise<string> {
  const apiKey = process.env.OPENAI_API_KEY;
  
  if (!apiKey) {
    throw new Error(
      'OPENAI_API_KEY environment variable is not set. ' +
      'Please set it before running research scripts.'
    );
  }

  const apiUrl = 'https://api.openai.com/v1/chat/completions';

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: [
          {
            role: 'system',
            content: 'You are a research assistant helping to create comprehensive compliance and readiness documentation. Provide detailed, accurate, and well-structured markdown output.',
          },
          {
            role: 'user',
            content: prompt,
          },
        ],
        temperature: 0.7,
        max_tokens: 4000,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        `OpenAI API error: ${response.status} ${response.statusText}. ` +
        `Details: ${JSON.stringify(errorData)}`
      );
    }

    const data = await response.json();
    
    if (!data.choices || !data.choices[0] || !data.choices[0].message) {
      throw new Error('Invalid response format from OpenAI API');
    }

    return data.choices[0].message.content;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error(`Failed to call OpenAI API: ${String(error)}`);
  }
}

