(() => {
  const STORAGE_KEY = 'wpm_audio_settings_v1';
  const DEFAULTS = {
    music_enabled: true,
    sfx_enabled: true,
    music_volume: 0.52,
    sfx_volume: 0.58,
  };

  const AudioContextCtor = window.AudioContext || window.webkitAudioContext;
  const supported = Boolean(AudioContextCtor);

  let settings = { ...DEFAULTS };
  try {
    const stored = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || '{}');
    settings = {
      ...DEFAULTS,
      ...stored,
    };
  } catch (_error) {
    settings = { ...DEFAULTS };
  }

  let context = null;
  let musicMaster = null;
  let sfxMaster = null;
  let currentScene = 'splash';
  let currentMode = null;
  let musicTimer = null;
  let sequenceStep = 0;
  let unlocked = false;
  let noiseBuffer = null;

  const sceneToMode = (scene) => {
    if (['splash', 'home', 'setup', 'end'].includes(scene)) return 'metal';
    if (scene === 'lobby') return 'lounge';
    return null;
  };

  const saveSettings = () => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  };

  const ensureContext = () => {
    if (!supported) return null;
    if (context) return context;

    context = new AudioContextCtor();
    musicMaster = context.createGain();
    sfxMaster = context.createGain();
    musicMaster.gain.value = settings.music_volume;
    sfxMaster.gain.value = settings.sfx_volume;
    musicMaster.connect(context.destination);
    sfxMaster.connect(context.destination);

    const length = Math.max(1, Math.floor(context.sampleRate * 0.5));
    noiseBuffer = context.createBuffer(1, length, context.sampleRate);
    const data = noiseBuffer.getChannelData(0);
    for (let index = 0; index < data.length; index += 1) {
      data[index] = (Math.random() * 2) - 1;
    }

    return context;
  };

  const resumeContext = async () => {
    const audio = ensureContext();
    if (!audio) return false;
    if (audio.state === 'suspended') {
      try {
        await audio.resume();
      } catch (_error) {
        return false;
      }
    }
    unlocked = audio.state === 'running';
    if (!unlocked) armUnlockListeners?.();
    return unlocked;
  };

  const stopMusic = () => {
    if (musicTimer) {
      window.clearInterval(musicTimer);
      musicTimer = null;
    }
    currentMode = null;
    sequenceStep = 0;
  };

  const makeDistortionCurve = (amount = 36) => {
    const samples = 256;
    const curve = new Float32Array(samples);
    const deg = Math.PI / 180;
    for (let index = 0; index < samples; index += 1) {
      const x = (index * 2 / samples) - 1;
      curve[index] = (
        (3 + amount) * x * 20 * deg
      ) / (
        Math.PI + amount * Math.abs(x)
      );
    }
    return curve;
  };

  const envelope = (
    node,
    {
      when,
      attack = 0.003,
      sustain = 0.04,
      release = 0.08,
      peak = 0.08,
    }
  ) => {
    const start = when;
    const hold = start + attack + sustain;
    const end = hold + release;
    node.gain.cancelScheduledValues(start);
    node.gain.setValueAtTime(0.0001, start);
    node.gain.exponentialRampToValueAtTime(
      Math.max(0.0002, peak),
      start + attack
    );
    node.gain.setValueAtTime(Math.max(0.0002, peak), hold);
    node.gain.exponentialRampToValueAtTime(0.0001, end);
    return end;
  };

  const tone = ({
    frequency,
    when,
    duration = 0.12,
    type = 'sawtooth',
    gain = 0.05,
    detune = 0,
    destination = musicMaster,
    filterFrequency = null,
    distortion = 0,
  }) => {
    const audio = ensureContext();
    if (!audio || !destination) return;

    const oscillator = audio.createOscillator();
    const amp = audio.createGain();
    oscillator.type = type;
    oscillator.frequency.setValueAtTime(frequency, when);
    oscillator.detune.setValueAtTime(detune, when);

    let sourceEnd = amp;
    if (distortion > 0) {
      const shaper = audio.createWaveShaper();
      shaper.curve = makeDistortionCurve(distortion);
      shaper.oversample = '4x';
      amp.connect(shaper);
      sourceEnd = shaper;
    }

    if (filterFrequency) {
      const filter = audio.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(filterFrequency, when);
      sourceEnd.connect(filter);
      filter.connect(destination);
    } else {
      sourceEnd.connect(destination);
    }

    const end = envelope(amp, {
      when,
      sustain: Math.max(0.01, duration * 0.45),
      release: Math.max(0.03, duration * 0.4),
      peak: gain,
    });

    oscillator.connect(amp);
    oscillator.start(when);
    oscillator.stop(end + 0.02);
  };

  const kick = (when, destination = musicMaster, gain = 0.12) => {
    const audio = ensureContext();
    if (!audio || !destination) return;
    const oscillator = audio.createOscillator();
    const amp = audio.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(130, when);
    oscillator.frequency.exponentialRampToValueAtTime(44, when + 0.11);
    amp.gain.setValueAtTime(gain, when);
    amp.gain.exponentialRampToValueAtTime(0.0001, when + 0.13);
    oscillator.connect(amp);
    amp.connect(destination);
    oscillator.start(when);
    oscillator.stop(when + 0.14);
  };

  const noiseHit = ({
    when,
    destination = musicMaster,
    gain = 0.04,
    duration = 0.08,
    highpass = 1500,
  }) => {
    const audio = ensureContext();
    if (!audio || !destination || !noiseBuffer) return;
    const source = audio.createBufferSource();
    source.buffer = noiseBuffer;
    const filter = audio.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.setValueAtTime(highpass, when);
    const amp = audio.createGain();
    amp.gain.setValueAtTime(gain, when);
    amp.gain.exponentialRampToValueAtTime(0.0001, when + duration);
    source.connect(filter);
    filter.connect(amp);
    amp.connect(destination);
    source.start(when);
    source.stop(when + duration);
  };

  const semitone = (root, offset) => root * Math.pow(2, offset / 12);

  const metalStep = () => {
    if (!context || !musicMaster) return;
    const now = context.currentTime + 0.015;
    const pattern = [0, 0, 3, 0, 5, 3, 0, 7, 0, 0, 10, 7, 5, 3, 0, -2];
    const step = sequenceStep % pattern.length;
    const root = 82.41;
    const note = semitone(root, pattern[step]);

    tone({
      frequency: note,
      when: now,
      duration: step % 4 === 0 ? 0.18 : 0.10,
      type: 'sawtooth',
      gain: 0.12,
      filterFrequency: 1600,
      distortion: 42,
    });
    tone({
      frequency: note * 2,
      when: now,
      duration: 0.08,
      type: 'square',
      gain: 0.035,
      filterFrequency: 2200,
      distortion: 26,
    });

    if ([0, 4, 8, 12].includes(step)) kick(now, musicMaster, 0.19);
    if ([4, 12].includes(step)) {
      noiseHit({
        when: now,
        gain: 0.085,
        duration: 0.12,
        highpass: 900,
      });
    }
    if (step % 2 === 0) {
      noiseHit({
        when: now,
        gain: 0.03,
        duration: 0.035,
        highpass: 4800,
      });
    }

    sequenceStep += 1;
  };

  const loungeStep = () => {
    if (!context || !musicMaster) return;
    const now = context.currentTime + 0.015;
    const step = sequenceStep % 16;
    const bassPattern = [0, null, 0, 3, 5, null, 3, null, 7, null, 5, 3, 0, null, -2, null];
    const chordRoots = [130.81, 146.83, 164.81, 146.83];

    if (bassPattern[step] !== null) {
      tone({
        frequency: semitone(65.41, bassPattern[step]),
        when: now,
        duration: 0.13,
        type: 'triangle',
        gain: 0.085,
        filterFrequency: 620,
      });
    }

    if (step % 4 === 0) {
      const root = chordRoots[(step / 4) % chordRoots.length];
      [0, 4, 7, 10].forEach((offset, index) => {
        tone({
          frequency: semitone(root, offset),
          when: now,
          duration: 0.33,
          type: index % 2 ? 'sine' : 'triangle',
          gain: 0.027,
          filterFrequency: 1500,
        });
      });
    }

    if ([0, 8].includes(step)) kick(now, musicMaster, 0.11);
    if ([4, 12].includes(step)) {
      noiseHit({
        when: now,
        gain: 0.05,
        duration: 0.08,
        highpass: 1200,
      });
    }
    if (step % 2 === 1) {
      noiseHit({
        when: now,
        gain: 0.025,
        duration: 0.025,
        highpass: 5200,
      });
    }

    sequenceStep += 1;
  };

  const startMode = async (mode) => {
    stopMusic();
    if (!settings.music_enabled || !mode) return;
    if (!(await resumeContext())) return;

    currentMode = mode;
    sequenceStep = 0;

    if (mode === 'metal') {
      metalStep();
      musicTimer = window.setInterval(metalStep, 104);
    } else if (mode === 'lounge') {
      loungeStep();
      musicTimer = window.setInterval(loungeStep, 144);
    }
  };

  const applyScene = () => {
    const mode = sceneToMode(currentScene);
    if (!settings.music_enabled || !mode || !unlocked) {
      stopMusic();
      return;
    }
    if (currentMode === mode && musicTimer) return;
    void startMode(mode);
  };

  const setScene = (scene) => {
    currentScene = String(scene || 'home');
    applyScene();
  };

  const unlock = async () => {
    const ready = await resumeContext();
    if (!ready) return false;
    applyScene();
    return true;
  };

  const setMusicEnabled = (enabled) => {
    settings.music_enabled = Boolean(enabled);
    saveSettings();
    if (musicMaster) {
      musicMaster.gain.setTargetAtTime(
        settings.music_enabled ? settings.music_volume : 0.0001,
        context.currentTime,
        0.03
      );
    }
    if (settings.music_enabled) {
      void unlock();
    } else {
      stopMusic();
    }
  };

  const setSfxEnabled = (enabled) => {
    settings.sfx_enabled = Boolean(enabled);
    saveSettings();
  };

  const playSfx = async (name) => {
    if (!settings.sfx_enabled) return;
    if (!(await resumeContext()) || !context || !sfxMaster) return;
    const now = context.currentTime + 0.01;

    if (name === 'score') {
      tone({
        frequency: 523.25,
        when: now,
        duration: 0.08,
        type: 'square',
        gain: 0.045,
        destination: sfxMaster,
      });
      tone({
        frequency: 659.25,
        when: now + 0.06,
        duration: 0.10,
        type: 'square',
        gain: 0.038,
        destination: sfxMaster,
      });
      return;
    }

    if (name === 'nextHole') {
      tone({
        frequency: 110,
        when: now,
        duration: 0.16,
        type: 'sawtooth',
        gain: 0.06,
        destination: sfxMaster,
        distortion: 30,
      });
      tone({
        frequency: 164.81,
        when: now + 0.07,
        duration: 0.18,
        type: 'sawtooth',
        gain: 0.045,
        destination: sfxMaster,
        distortion: 30,
      });
      return;
    }

    if (name === 'banter') {
      tone({
        frequency: 220,
        when: now,
        duration: 0.06,
        type: 'square',
        gain: 0.04,
        destination: sfxMaster,
      });
      tone({
        frequency: 174.61,
        when: now + 0.05,
        duration: 0.09,
        type: 'square',
        gain: 0.035,
        destination: sfxMaster,
      });
      return;
    }

    if (name === 'roundStart') {
      kick(now, sfxMaster, 0.11);
      noiseHit({
        when: now,
        destination: sfxMaster,
        gain: 0.05,
        duration: 0.18,
        highpass: 850,
      });
      tone({
        frequency: 82.41,
        when: now,
        duration: 0.22,
        type: 'sawtooth',
        gain: 0.055,
        destination: sfxMaster,
        distortion: 40,
      });
      return;
    }

    if (name === 'join') {
      tone({
        frequency: 392,
        when: now,
        duration: 0.08,
        type: 'sine',
        gain: 0.035,
        destination: sfxMaster,
      });
      tone({
        frequency: 523.25,
        when: now + 0.08,
        duration: 0.10,
        type: 'sine',
        gain: 0.032,
        destination: sfxMaster,
      });
    }
  };

  const getSettings = () => ({ ...settings });

  let unlockListenersArmed = false;

  const disarmUnlockListeners = () => {
    if (!unlockListenersArmed) return;
    unlockListenersArmed = false;
    window.removeEventListener('pointerup', onAudioGesture, true);
    window.removeEventListener('touchend', onAudioGesture, true);
    window.removeEventListener('click', onAudioGesture, true);
    window.removeEventListener('keydown', onAudioGesture, true);
  };

  const armUnlockListeners = () => {
    if (unlockListenersArmed) return;
    unlockListenersArmed = true;
    window.addEventListener('pointerup', onAudioGesture, true);
    window.addEventListener('touchend', onAudioGesture, true);
    window.addEventListener('click', onAudioGesture, true);
    window.addEventListener('keydown', onAudioGesture, true);
  };

  function onAudioGesture() {
    void unlock().then((ready) => {
      if (ready) disarmUnlockListeners();
    });
  }

  armUnlockListeners();

  document.addEventListener('visibilitychange', () => {
    if (!context) return;
    if (document.hidden) {
      void context.suspend();
      return;
    }
    if (unlocked) {
      void context.resume()
        .then(() => {
          unlocked = context.state === 'running';
          if (unlocked) applyScene();
          else armUnlockListeners();
        })
        .catch(() => {
          unlocked = false;
          armUnlockListeners();
        });
    } else {
      armUnlockListeners();
    }
  });

  window.WPMAudio = {
    supported,
    unlock,
    setScene,
    getSettings,
    setMusicEnabled,
    setSfxEnabled,
    playSfx,
  };

  setScene('splash');
})();
