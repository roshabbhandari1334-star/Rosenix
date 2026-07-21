/**
 * J.A.R.V.I.S. Voice Engine (Speech Recognition & TTS Synthesizer)
 */
class JarvisVoiceEngine {
    constructor(onSpeechRecognized, onTranscriptUpdate, onStateChange) {
        self = this;
        this.onSpeechRecognized = onSpeechRecognized;
        this.onTranscriptUpdate = onTranscriptUpdate;
        this.onStateChange = onStateChange;

        this.recognition = null;
        this.isListening = false;
        this.ttsEnabled = true;
        this.synth = window.speechSynthesis;

        this.initRecognition();
    }

    initRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.warn("[JARVIS Voice] Web Speech Recognition API not supported in this browser environment.");
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';

        this.recognition.onstart = () => {
            this.isListening = true;
            if (this.onStateChange) this.onStateChange('LISTENING');
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            const currentText = finalTranscript || interimTranscript;
            if (this.onTranscriptUpdate) this.onTranscriptUpdate(currentText);

            if (finalTranscript.trim()) {
                this.stopListening();
                if (this.onSpeechRecognized) this.onSpeechRecognized(finalTranscript.trim());
            }
        };

        this.recognition.onerror = (event) => {
            console.error("[JARVIS Voice Error]", event.error);
            this.stopListening();
        };

        this.recognition.onend = () => {
            this.isListening = false;
            if (this.onStateChange) this.onStateChange('IDLE');
        };
    }

    toggleListening() {
        if (!this.recognition) {
            alert("Voice Recognition is not supported in this browser engine. Please use Chrome/Edge or standard Desktop PyWebView.");
            return;
        }

        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    startListening() {
        if (this.recognition && !this.isListening) {
            try {
                this.recognition.start();
            } catch (e) {
                console.error("Mic start error", e);
            }
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            try {
                this.recognition.stop();
            } catch (e) {}
            this.isListening = false;
            if (this.onStateChange) this.onStateChange('IDLE');
        }
    }

    speak(text) {
        if (!this.ttsEnabled || !this.synth) return;

        // Cancel previous speech
        this.synth.cancel();

        const cleanText = text.replace(/[*#`_]/g, ''); // Strip markdown symbols
        const utterance = new SpeechSynthesisUtterance(cleanText);

        utterance.rate = 1.0;
        utterance.pitch = 0.95; // Slightly lower calm frequency

        // Try to pick an English voice (preferably UK/Natural)
        const voices = this.synth.getVoices();
        const jarvisVoice = voices.find(v => v.lang.includes('en-GB') || v.name.includes('Natural') || v.name.includes('Google UK English Male')) || voices.find(v => v.lang.includes('en'));
        if (jarvisVoice) {
            utterance.voice = jarvisVoice;
        }

        utterance.onstart = () => {
            if (this.onStateChange) this.onStateChange('SPEAKING');
        };

        utterance.onend = () => {
            if (this.onStateChange) this.onStateChange('IDLE');
        };

        this.synth.speak(utterance);
    }
}
