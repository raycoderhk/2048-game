/**
 * Serverless function to proxy Aliyun Qwen API requests
 * This avoids CORS issues by calling from server-side
 */

export default async function handler(req, res) {
    // Only allow POST requests
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { word } = req.body;

    if (!word) {
        return res.status(400).json({ error: 'Word is required' });
    }

    try {
        const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer sk-92b75e89aa404648b08741885f191e6b',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'qwen-plus',
                input: {
                    messages: [{
                        role: 'system',
                        content: 'You are an ESL English teacher. Explain vocabulary words with etymology, technical usage, related words, and examples. Provide bilingual (English + Traditional Chinese) explanations. Use HTML formatting with <br>, <strong>, <em> tags. Keep explanations concise but informative.'
                    }, {
                        role: 'user',
                        content: `Explain the word "${word}" in detail. Include: 1) Word Origin/Etymology, 2) Technical/Academic Usage, 3) Related Words (synonyms, word family), 4) Example from National Geographic article. Provide both English and Traditional Chinese (Cantonese-friendly) explanations. Format with HTML tags.`
                    }]
                },
                parameters: {
                    temperature: 0.7,
                    max_tokens: 500
                }
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Aliyun API error: ${response.status} - ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        
        // Return the AI response
        res.status(200).json({
            success: true,
            explanation: data.output.text,
            word: word
        });

    } catch (error) {
        console.error('AI Proxy Error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
}
