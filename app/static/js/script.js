async function playTone1000(event) {
    const form = document.getElementById('toneForm');
    const channel = form.channel.value;
    const amplitude = parseFloat(event.target.value);

    const response = await fetch('/generate_tone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: 1.0,
            frequency: 1000,
            amplitude: amplitude,
            phase: 0.0,
            channel: channel
        }),
    });

    if (response.ok) {
        const arrayBuffer = await response.arrayBuffer();
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

        const source = audioCtx.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioCtx.destination);
        source.start();
    } else {
        console.error('Failed to fetch audio data');
    }
}




async function playTone2000(event) {
    const form = document.getElementById('toneForm');
    const channel = form.channel.value;
    const amplitude = parseFloat(event.target.value);

    const response = await fetch('/generate_tone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: 1.0,
            frequency: 2000,
            amplitude: amplitude,
            phase: 0.0,
            channel: channel
        }),
    });

    if (response.ok) {
        const arrayBuffer = await response.arrayBuffer();
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

        const source = audioCtx.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioCtx.destination);
        source.start();
    } else {
        console.error('Failed to fetch audio data');
    }
}






async function playTone4000(event) {
    const form = document.getElementById('toneForm');
    const channel = form.channel.value;
    const amplitude = parseFloat(event.target.value);

    const response = await fetch('/generate_tone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: 1.0,
            frequency: 4000,
            amplitude: amplitude,
            phase: 0.0,
            channel: channel
        }),
    });

    if (response.ok) {
        const arrayBuffer = await response.arrayBuffer();
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

        const source = audioCtx.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioCtx.destination);
        source.start();
    } else {
        console.error('Failed to fetch audio data');
    }
}






async function playTone8000(event) {
    const form = document.getElementById('toneForm');
    const channel = form.channel.value;
    const amplitude = parseFloat(event.target.value);

    const response = await fetch('/generate_tone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: 1.0,
            frequency: 8000,
            amplitude: amplitude,
            phase: 0.0,
            channel: channel
        }),
    });

    if (response.ok) {
        const arrayBuffer = await response.arrayBuffer();
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

        const source = audioCtx.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioCtx.destination);
        source.start();
    } else {
        console.error('Failed to fetch audio data');
    }
}










async function playTone500(event) {
    const form = document.getElementById('toneForm');
    const channel = form.channel.value;
    const amplitude = parseFloat(event.target.value);

    const response = await fetch('/generate_tone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: 1.0,
            frequency: 500,
            amplitude: amplitude,
            phase: 0.0,
            channel: channel
        }),
    });

    if (response.ok) {
        const arrayBuffer = await response.arrayBuffer();
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

        const source = audioCtx.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioCtx.destination);
        source.start();
    } else {
        console.error('Failed to fetch audio data');
    }
}




async function playTone250(event) {
    const form = document.getElementById('toneForm');
    const channel = form.channel.value;
    const amplitude = parseFloat(event.target.value);

    const response = await fetch('/generate_tone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: 1.0,
            frequency: 250,
            amplitude: amplitude,
            phase: 0.0,
            channel: channel
        }),
    });

    if (response.ok) {
        const arrayBuffer = await response.arrayBuffer();
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

        const source = audioCtx.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioCtx.destination);
        source.start();
    } else {
        console.error('Failed to fetch audio data');
    }
}