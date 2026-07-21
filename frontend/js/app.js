/**
 * J.A.R.V.I.S. Autonomous Agentic Controller
 */
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatFeed = document.getElementById('chat-feed');
    const commandInput = document.getElementById('command-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const attachBtn = document.getElementById('attach-btn');
    const fileInput = document.getElementById('file-input');
    const dropzone = document.getElementById('dropzone');
    const dropzoneTrigger = document.getElementById('dropzone-trigger');
    const uploadedFilesList = document.getElementById('uploaded-files-list');
    const reactorStateText = document.getElementById('reactor-state');
    const reactorContainer = document.querySelector('.arc-container');
    const liveClock = document.getElementById('live-clock');
    const voiceTranscriptBanner = document.getElementById('voice-transcript-banner');
    const liveSpeechText = document.getElementById('live-speech-text');
    const ttsToggleBtn = document.getElementById('tts-toggle');
    const ttsStatusVal = document.getElementById('tts-status-val');
    const agentSelect = document.getElementById('agent-select');

    // Telemetry Elements
    const valCpu = document.getElementById('val-cpu');
    const fillCpu = document.getElementById('fill-cpu');
    const valRam = document.getElementById('val-ram');
    const fillRam = document.getElementById('fill-ram');
    const valDisk = document.getElementById('val-disk');
    const fillDisk = document.getElementById('fill-disk');
    const valShortMem = document.getElementById('val-short-mem');
    const valEpMem = document.getElementById('val-ep-mem');

    let attachedFiles = [];

    // Initialize Voice Engine
    const voiceEngine = new JarvisVoiceEngine(
        (finalSpeech) => {
            voiceTranscriptBanner.style.display = 'none';
            commandInput.value = finalSpeech;
            submitAgenticGoal(finalSpeech, true);
        },
        (interimSpeech) => {
            voiceTranscriptBanner.style.display = 'block';
            liveSpeechText.textContent = interimSpeech || "Listening...";
        },
        (state) => {
            updateReactorState(state);
            if (state === 'LISTENING') {
                micBtn.classList.add('active');
                voiceTranscriptBanner.style.display = 'block';
            } else {
                micBtn.classList.remove('active');
                if (state !== 'LISTENING') voiceTranscriptBanner.style.display = 'none';
            }
        }
    );

    // Live Clock Update
    setInterval(() => {
        liveClock.textContent = new Date().toLocaleTimeString();
    }, 1000);

    // Poll Hardware & Memory Telemetry
    async function fetchTelemetry() {
        try {
            const res = await fetch('/api/v1/system/stats');
            if (res.ok) {
                const stats = await res.json();
                valCpu.textContent = `${stats.cpu_usage}%`;
                fillCpu.style.width = `${Math.min(stats.cpu_usage, 100)}%`;

                valRam.textContent = `${stats.memory_used_gb} / ${stats.memory_total_gb} GB`;
                fillRam.style.width = `${Math.min(stats.memory_percent, 100)}%`;

                valDisk.textContent = `${stats.disk_percent}%`;
                fillDisk.style.width = `${Math.min(stats.disk_percent, 100)}%`;
            }

            const memRes = await fetch('/api/v1/agentic/memory/stats');
            if (memRes.ok) {
                const mStats = await memRes.json();
                valShortMem.textContent = mStats.short_term_entries;
                valEpMem.textContent = mStats.episodic_episodes;
            }
        } catch (e) {
            console.warn("Telemetry fetch error:", e);
        }
    }
    fetchTelemetry();
    setInterval(fetchTelemetry, 3000);

    function updateReactorState(state) {
        reactorStateText.textContent = `STATE: ${state}`;
        reactorContainer.className = `arc-container ${state.toLowerCase()}`;
    }

    ttsToggleBtn.addEventListener('click', () => {
        voiceEngine.ttsEnabled = !voiceEngine.ttsEnabled;
        ttsStatusVal.textContent = voiceEngine.ttsEnabled ? "ON" : "OFF";
        ttsToggleBtn.style.borderColor = voiceEngine.ttsEnabled ? "var(--accent-cyan)" : "rgba(255,255,255,0.2)";
    });

    micBtn.addEventListener('click', () => voiceEngine.toggleListening());

    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const cmd = chip.getAttribute('data-cmd');
            if (cmd) {
                commandInput.value = cmd;
                submitAgenticGoal(cmd);
            }
        });
    });

    sendBtn.addEventListener('click', () => {
        const goal = commandInput.value.trim();
        if (goal) submitAgenticGoal(goal);
    });

    commandInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const goal = commandInput.value.trim();
            if (goal) submitAgenticGoal(goal);
        }
    });

    attachBtn.addEventListener('click', () => fileInput.click());
    dropzoneTrigger.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFiles(e.target.files);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        if (dt.files.length) handleFiles(dt.files);
    });

    async function handleFiles(files) {
        for (let file of files) {
            const formData = new FormData();
            formData.append('file', file);
            try {
                const res = await fetch('/api/v1/upload', { method: 'POST', body: formData });
                if (res.ok) {
                    const data = await res.json();
                    attachedFiles.push(data.file);
                    renderFilePill(data.file);
                    appendMessageCard("J.A.R.V.I.S. SYSTEM", `File \`${data.file.filename}\` uploaded successfully. Ready for agentic analysis.`, "jarvis");
                }
            } catch (err) {
                console.error("Upload error:", err);
            }
        }
    }

    function renderFilePill(fileData) {
        const pill = document.createElement('div');
        pill.className = 'file-pill';
        pill.innerHTML = `<i class="fa-solid fa-file"></i> ${fileData.filename}`;
        uploadedFilesList.appendChild(pill);
    }

    // Submit Autonomous Goal
    async function submitAgenticGoal(goalText, isVoice = false) {
        commandInput.value = '';
        const selectedRole = agentSelect.value;
        appendMessageCard("COMMANDER", goalText, "user");
        updateReactorState('PROCESSING');

        try {
            const response = await fetch('/api/v1/agentic/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    goal: goalText,
                    agent_role: selectedRole
                })
            });

            if (response.ok) {
                const data = await response.json();
                appendMessageCard(`ROSENIX (${data.agent.toUpperCase()})`, data.formatted_response, "jarvis");

                if (data.voice_response) {
                    voiceEngine.speak(data.voice_response);
                } else {
                    updateReactorState('IDLE');
                }
            } else {
                appendMessageCard("ROSENIX ALERT", "Autonomous goal execution failed.", "jarvis");
                updateReactorState('IDLE');
            }
        } catch (e) {
            console.error("Agentic submit error:", e);
            appendMessageCard("ROSENIX ALERT", "Autonomous Communication Link Offline.", "jarvis");
            updateReactorState('IDLE');
        }
    }

    function appendMessageCard(sender, text, type = "jarvis") {
        const card = document.createElement('div');
        card.className = `message-card ${type}`;

        const header = document.createElement('div');
        header.className = 'msg-header';
        header.innerHTML = `<span>${sender}</span> <span>${new Date().toLocaleTimeString()}</span>`;

        const content = document.createElement('div');
        content.className = 'msg-content';

        let formatted = text
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');

        content.innerHTML = formatted;

        card.appendChild(header);
        card.appendChild(content);

        chatFeed.appendChild(card);
        chatFeed.scrollTop = chatFeed.scrollHeight;
    }
});
