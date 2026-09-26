(() => {
  const STORAGE_KEY = 'wpm_audio_settings_v1';
  const MANIFEST_URL = '/static/audio/audio-manifest.json';
  const DEFAULTS = {
    music_enabled: true,
    sfx_enabled: true,
    music_volume: 0.62,
    sfx_volume: 0.72,
  };

  const supported = typeof window.Audio === 'function';
  let settings = { ...DEFAULTS };
  try {
    const stored = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || '{}');
    settings = { ...DEFAULTS, ...stored };
  } catch (_error) {
    settings = { ...DEFAULTS };
  }

  const emptyManifest = () => ({
    version: 1,
    music: {
      metal: [],
      lobby: [],
      end: [],
    },
    sfx: {},
  });

  let manifest = emptyManifest();
  let manifestLoaded = false;
  let manifestPromise = null;
  let currentScene = 'splash';
  let currentPool = null;
  let currentTrackId = null;
  let unlockListenersArmed = false;
  const lastTrackIdByPool = new Map();
  const activeSfx = new Set();

  const music = supported ? new Audio() : null;
  if (music) {
    music.preload = 'metadata';
    music.playsInline = true;
    music.volume = settings.music_volume;
  }

  const saveSettings = () => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  };

  const clampVolume = (value, fallback) => {
    const number = Number(value);
    if (!Number.isFinite(number)) return fallback;
    return Math.max(0, Math.min(1, number));
  };

  const normalizeTrack = (row) => {
    if (!row || typeof row !== 'object') return null;
    const id = String(row.id || '').trim();
    const file = String(row.file || '').trim();
    if (!id || !file) return null;
    return {
      id,
      file,
      label: String(row.label || id),
    };
  };

  const normalizeManifest = (data) => {
    const next = emptyManifest();
    next.version = Number(data?.version || 1);
    ['metal', 'lobby', 'end'].forEach((pool) => {
      const rows = Array.isArray(data?.music?.[pool]) ? data.music[pool] : [];
      next.music[pool] = rows.map(normalizeTrack).filter(Boolean);
    });
    next.sfx = (
      data?.sfx
      && typeof data.sfx === 'object'
      && !Array.isArray(data.sfx)
    ) ? { ...data.sfx } : {};
    return next;
  };

  const loadManifest = async ({ force = false } = {}) => {
    if (manifestLoaded && !force) return manifest;
    if (manifestPromise) return manifestPromise;

    manifestPromise = fetch(MANIFEST_URL, {
      cache: 'no-store',
      headers: { Accept: 'application/json' },
    })
      .then((response) => {
        if (!response.ok) throw new Error('audio manifest unavailable');
        return response.json();
      })
      .then((data) => {
        manifest = normalizeManifest(data);
        manifestLoaded = true;
        return manifest;
      })
      .catch(() => manifest)
      .finally(() => {
        manifestPromise = null;
      });

    return manifestPromise;
  };

  const sceneToPool = (scene) => {
    if (['splash', 'auth', 'home', 'setup'].includes(scene)) return 'metal';
    if (scene === 'lobby') return 'lobby';
    if (scene === 'end') return 'end';
    return null;
  };

  const poolTracks = (pool) => {
    if (!pool) return [];
    return Array.isArray(manifest.music?.[pool]) ? manifest.music[pool] : [];
  };

  const resolvedPool = (scene) => {
    const requested = sceneToPool(scene);
    if (requested !== 'end') return requested;
    return poolTracks('end').length ? 'end' : 'metal';
  };

  const pickTrack = (pool) => {
    const rows = poolTracks(pool);
    if (!rows.length) return null;
    if (rows.length === 1) return rows[0];

    const lastId = lastTrackIdByPool.get(pool);
    const eligible = rows.filter(
      (row) => row.id !== lastId && row.id !== currentTrackId
    );
    const choices = eligible.length ? eligible : rows;
    return choices[Math.floor(Math.random() * choices.length)];
  };

  const stopMusic = ({ clearSource = false } = {}) => {
    if (!music) return;
    music.pause();
    try {
      music.currentTime = 0;
    } catch (_error) {
      // Some browsers reject currentTime changes before metadata is loaded.
    }
    currentPool = null;
    currentTrackId = null;
    if (clearSource) {
      music.removeAttribute('src');
      music.load();
    }
  };

  const playTrack = async (track, pool) => {
    if (!music || !track) return false;
    music.pause();
    music.src = track.file;
    music.volume = clampVolume(settings.music_volume, DEFAULTS.music_volume);
    currentPool = pool;
    currentTrackId = track.id;
    lastTrackIdByPool.set(pool, track.id);

    try {
      await music.play();
      return true;
    } catch (_error) {
      currentPool = null;
      currentTrackId = null;
      return false;
    }
  };

  const startPool = async (pool) => {
    const track = pickTrack(pool);
    if (!track) {
      stopMusic();
      return true;
    }
    return playTrack(track, pool);
  };

  const applyScene = async () => {
    if (!supported || !music) return false;
    await loadManifest();

    if (!settings.music_enabled) {
      stopMusic();
      return true;
    }

    const pool = resolvedPool(currentScene);
    if (!pool) {
      stopMusic();
      return true;
    }

    if (!poolTracks(pool).length) {
      stopMusic();
      return true;
    }

    if (
      currentPool === pool
      && currentTrackId
      && !music.paused
    ) {
      return true;
    }

    stopMusic();
    const played = await startPool(pool);
    if (!played) armUnlockListeners();
    return played;
  };

  const setScene = (scene) => {
    currentScene = String(scene || 'home');
    void applyScene();
  };

  const unlock = async () => {
    const ready = await applyScene();
    if (ready) disarmUnlockListeners();
    return ready;
  };

  const setMusicEnabled = (enabled) => {
    settings.music_enabled = Boolean(enabled);
    saveSettings();
    if (!settings.music_enabled) {
      stopMusic();
      return;
    }
    void applyScene();
  };

  const setSfxEnabled = (enabled) => {
    settings.sfx_enabled = Boolean(enabled);
    saveSettings();
  };

  const sfxFile = (name) => {
    const entry = manifest.sfx?.[name];
    if (typeof entry === 'string') return entry;
    if (entry && typeof entry === 'object') return String(entry.file || '');
    return '';
  };

  const playSfx = async (name) => {
    if (!supported || !settings.sfx_enabled) return false;
    await loadManifest();
    const file = sfxFile(name);
    if (!file) return false;

    const player = new Audio(file);
    player.preload = 'auto';
    player.playsInline = true;
    player.volume = clampVolume(settings.sfx_volume, DEFAULTS.sfx_volume);
    activeSfx.add(player);
    const cleanup = () => activeSfx.delete(player);
    player.addEventListener('ended', cleanup, { once: true });
    player.addEventListener('error', cleanup, { once: true });

    try {
      await player.play();
      return true;
    } catch (_error) {
      cleanup();
      armUnlockListeners();
      return false;
    }
  };

  const getSettings = () => ({ ...settings });

  const refreshManifest = async () => {
    await loadManifest({ force: true });
    return applyScene();
  };

  function onAudioGesture() {
    void unlock();
  }

  function armUnlockListeners() {
    if (unlockListenersArmed) return;
    unlockListenersArmed = true;
    window.addEventListener('pointerup', onAudioGesture, true);
    window.addEventListener('touchend', onAudioGesture, true);
    window.addEventListener('click', onAudioGesture, true);
    window.addEventListener('keydown', onAudioGesture, true);
  }

  function disarmUnlockListeners() {
    if (!unlockListenersArmed) return;
    unlockListenersArmed = false;
    window.removeEventListener('pointerup', onAudioGesture, true);
    window.removeEventListener('touchend', onAudioGesture, true);
    window.removeEventListener('click', onAudioGesture, true);
    window.removeEventListener('keydown', onAudioGesture, true);
  }

  music?.addEventListener('ended', () => {
    if (!settings.music_enabled) return;
    const pool = resolvedPool(currentScene);
    if (!pool || pool !== currentPool) return;
    void startPool(pool).then((played) => {
      if (!played) armUnlockListeners();
    });
  });

  music?.addEventListener('error', () => {
    if (!settings.music_enabled) return;
    const pool = resolvedPool(currentScene);
    if (!pool) return;
    window.setTimeout(() => {
      void startPool(pool).then((played) => {
        if (!played) armUnlockListeners();
      });
    }, 250);
  });

  document.addEventListener('visibilitychange', () => {
    if (!music || document.hidden) {
      music?.pause();
      return;
    }
    void applyScene();
  });

  window.WPMAudio = {
    supported,
    unlock,
    setScene,
    getSettings,
    setMusicEnabled,
    setSfxEnabled,
    playSfx,
    refreshManifest,
  };

  armUnlockListeners();
  void loadManifest().then(() => applyScene());
})();
