async function generate() {
    try {
        const response = await fetch('http://localhost:8000/api/llm/blab', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({prompt: 'Test 1, 2, 3, '} ),
        })

        const reader = response.body.getReader();
        const decoder = new TextDecoder()
        let events = ""
		while(true) {
			const {done, value} = await reader.read()
            console.log(value)
            const decoded = decoder.decode(value)
            try {
                const partial = JSON.parse(decoded.replace(/^[,\[\]\n]*/g, '').replace(/[,\[\]\n]*$/g, ''))
                document.getElementById('generated-text').value += partial.generated_text
            } catch (err) {
                console.warn('Not valid json!', decoded, err)
            }
            events += decoded
            if (done) break;

        }
        const full = JSON.parse(events)
        console.log(full)
        document.getElementById('response-section').innerHTML += `<pre><code>${JSON.stringify(full, null, 4)}</code></pre>`
    } catch (error) {
        console.error('Error when starting process:', error)
    }
}
// document.getElementById("btn_generate").addEventListener("click", read);
