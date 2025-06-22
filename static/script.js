// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    // Get references to all the HTML elements we'll be using
    const videoInput = document.getElementById('video-input');
    const uploadBtn = document.getElementById('upload-btn');
    const summarizeBtn = document.getElementById('summarize-btn');
    const statusDiv = document.getElementById('status');
    const resultsSection = document.getElementById('results-section');
    const transcriptText = document.getElementById('transcript-text');
    const summaryContainer = document.getElementById('summary-container');
    const summaryText = document.getElementById('summary-text');

    // --- Event Listener for the Transcribe Button ---
    uploadBtn.addEventListener('click', async () => {
        const file = videoInput.files[0];
        if (!file) {
            statusDiv.textContent = 'Please select a video file first.';
            return;
        }

        // Prepare for API call
        const formData = new FormData();
        formData.append('video', file);

        // Update UI to show processing state
        statusDiv.textContent = 'Uploading and transcribing... This may take a while for long videos.';
        uploadBtn.disabled = true;
        resultsSection.classList.add('hidden'); // Hide previous results

        try {
            // Call the backend /transcribe endpoint
            const response = await fetch('/transcribe', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to transcribe video.');
            }

            const data = await response.json();
            
            // --- Success: Display the transcript ---
            transcriptText.value = data.transcript;
            resultsSection.classList.remove('hidden'); // Show the results section
            summarizeBtn.classList.remove('hidden'); // IMPORTANT: Show the summarize button
            summaryContainer.classList.add('hidden'); // Ensure summary is hidden initially
            statusDiv.textContent = 'Transcription successful!';

        } catch (error) {
            statusDiv.textContent = `Error: ${error.message}`;
            console.error('Transcription error:', error);
        } finally {
            // Re-enable the upload button
            uploadBtn.disabled = false;
        }
    });

    // --- Event Listener for the Summarize Button ---
    summarizeBtn.addEventListener('click', async () => {
        const textToSummarize = transcriptText.value;
        if (!textToSummarize) {
            statusDiv.textContent = 'No transcript available to summarize.';
            return;
        }

        // Update UI to show processing state
        statusDiv.textContent = 'Summarizing...';
        summarizeBtn.disabled = true;

        try {
            // Call the backend /summarize endpoint
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: textToSummarize }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to summarize text.');
            }

            const data = await response.json();
            
            // --- Success: Display the summary ---
            summaryText.value = data.summary;
            summaryContainer.classList.remove('hidden'); // Show the summary box
            statusDiv.textContent = 'Summarization successful!';

        } catch (error) {
            statusDiv.textContent = `Error: ${error.message}`;
            console.error('Summarization error:', error);
        } finally {
            // Re-enable the summarize button
            summarizeBtn.disabled = false;
        }
    });
});