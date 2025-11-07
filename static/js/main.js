// Main JavaScript for YouTube Video Summarizer

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('summarizeForm');
    const videoUrlInput = document.getElementById('videoUrl');
    const submitBtn = document.getElementById('submitBtn');
    const errorMessage = document.getElementById('errorMessage');
    const statusMessage = document.getElementById('statusMessage');
    const statusText = statusMessage.querySelector('.status-text');
    const resultCard = document.getElementById('resultCard');
    const summaryContent = document.getElementById('summaryContent');
    const transcriptInfo = document.getElementById('transcriptInfo');
    const transcriptLength = document.getElementById('transcriptLength');
    const transcriptPreview = document.getElementById('transcriptPreview');
    const transcriptText = document.getElementById('transcriptText');
    const closeResultBtn = document.getElementById('closeResult');

    // Close result card
    closeResultBtn.addEventListener('click', function() {
        resultCard.style.display = 'none';
        videoUrlInput.value = '';
        errorMessage.style.display = 'none';
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const url = videoUrlInput.value.trim();
        
        if (!url) {
            showError('Please enter a YouTube URL');
            return;
        }

        // Validate YouTube URL
        if (!isValidYouTubeUrl(url)) {
            showError('Please enter a valid YouTube URL');
            return;
        }

        // Reset UI
        hideError();
        hideResult();
        setLoading(true);
        showStatus('Extracting transcript...');

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();

            if (data.success) {
                showStatus('Generating summary...');
                // Small delay for UX
                await new Promise(resolve => setTimeout(resolve, 500));
                showResult(data);
            } else {
                showError(data.error || 'An error occurred');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        } finally {
            setLoading(false);
            hideStatus();
        }
    });

    function isValidYouTubeUrl(url) {
        const patterns = [
            /^https?:\/\/(www\.)?(youtube\.com|youtu\.be)\/.+$/,
            /^https?:\/\/youtube\.com\/embed\/.+$/,
            /^https?:\/\/youtu\.be\/.+$/
        ];
        return patterns.some(pattern => pattern.test(url));
    }

    function setLoading(loading) {
        if (loading) {
            submitBtn.disabled = true;
            submitBtn.querySelector('.btn-text').style.display = 'none';
            submitBtn.querySelector('.btn-loader').style.display = 'flex';
            videoUrlInput.disabled = true;
        } else {
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').style.display = 'inline';
            submitBtn.querySelector('.btn-loader').style.display = 'none';
            videoUrlInput.disabled = false;
        }
    }

    function showStatus(message) {
        statusText.textContent = message;
        statusMessage.style.display = 'block';
    }

    function hideStatus() {
        statusMessage.style.display = 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }

    function showResult(data) {
        summaryContent.textContent = data.summary;
        
        if (data.transcript_length) {
            transcriptLength.textContent = data.transcript_length.toLocaleString();
            transcriptInfo.style.display = 'block';
        }

        if (data.transcript_preview) {
            transcriptText.textContent = data.transcript_preview;
            transcriptPreview.style.display = 'block';
        }

        resultCard.style.display = 'block';
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideResult() {
        resultCard.style.display = 'none';
        summaryContent.textContent = '';
        transcriptInfo.style.display = 'none';
        transcriptPreview.style.display = 'none';
    }

    // Check API health on load
    checkHealth();

    async function checkHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (!data.api_key_configured) {
                showError('Warning: OpenAI API key not configured. Please check your .env file.');
            }
        } catch (error) {
            console.error('Health check failed:', error);
        }
    }
});

