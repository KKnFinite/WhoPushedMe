(() => {
  const SESSION_KEY = 'wpm_session_token';

  const splash = document.getElementById('launch-splash');
  const authShell = document.getElementById('auth-shell');
  const appShell = document.getElementById('app-shell');
  const authMessage = document.getElementById('auth-message');
  const authTabs = document.querySelector('.auth-tabs');
  const authViewButtons = document.querySelectorAll('[data-auth-view]');
  const authPanels = document.querySelectorAll('[data-auth-panel]');
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const recoverForm = document.getElementById('recover-form');
  const recoveryCard = document.getElementById('recovery-key-card');
  const recoveryKeyValue = document.getElementById('recovery-key-value');
  const recoveryKeyCopy = document.getElementById('copy-recovery-key');
  const recoveryKeyContinue = document.getElementById('recovery-key-continue');
  const logoutButton = document.getElementById('logout-button');
  const welcomeKicker = document.getElementById('home-welcome-kicker');
  const settingsButton = document.getElementById('settings-button');
  const settingsModal = document.getElementById('settings-modal');
  const settingsClose = document.getElementById('settings-close');
  const settingsForm = document.getElementById('settings-form');
  const settingsMessage = document.getElementById('settings-message');
  const startRoundButton = document.getElementById('start-round-button');
  const joinRoundButton = document.getElementById('join-round-button');
  const roundFlowModal = document.getElementById('round-flow-modal');
  const roundFlowClose = document.getElementById('round-flow-close');
  const roundFlowTitle = document.getElementById('round-flow-title');
  const roundFlowMessage = document.getElementById('round-flow-message');
  const startRoundForm = document.getElementById('start-round-form');
  const joinRoundForm = document.getElementById('join-round-form');
  const lobbyPanel = document.getElementById('lobby-panel');
  const lobbyCode = document.getElementById('lobby-code');
  const lobbySummary = document.getElementById('lobby-summary');
  const lobbyParticipants = document.getElementById('lobby-participants');
  const lobbyStart = document.getElementById('lobby-start');
  const lobbyHome = document.getElementById('lobby-home');
  const courseSearchPanel = document.getElementById('course-search-panel');
  const freePlayField = document.getElementById('free-play-field');
  const courseSearchInput = document.getElementById('course-search-input');
  const courseSearchButton = document.getElementById('course-search-button');
  const courseResults = document.getElementById('course-results');
  const selectedCourseBox = document.getElementById('selected-course');
  const selectedCourseName = document.getElementById('selected-course-name');
  const selectedCourseLocation = document.getElementById('selected-course-location');
  const startTeeField = document.getElementById('start-tee-field');
  const startTeeSelect = document.getElementById('start-tee-select');
  const lobbyTeePanel = document.getElementById('lobby-tee-panel');
  const lobbyTeeSelect = document.getElementById('lobby-tee-select');
  const lobbyTeeSave = document.getElementById('lobby-tee-save');
  const liveRoundPanel = document.getElementById('live-round-panel');
  const liveRoundPlace = document.getElementById('live-round-place');
  const liveRoundCode = document.getElementById('live-round-code');
  const holePrev = document.getElementById('hole-prev');
  const holeNext = document.getElementById('hole-next');
  const holeStateLabel = document.getElementById('hole-state-label');
  const holeNumber = document.getElementById('hole-number');
  const holeParLabel = document.getElementById('hole-par-label');
  const parForm = document.getElementById('par-form');
  const parInput = document.getElementById('par-input');
  const parSubmit = document.getElementById('par-submit');
  const liveScoreArea = document.getElementById('live-score-area');
  const latestPresentation = document.getElementById('latest-presentation');
  const latestMascot = document.getElementById('latest-mascot');
  const latestBanter = document.getElementById('latest-banter');
  const latestFallback = document.getElementById('latest-fallback');
  const liveRoundHome = document.getElementById('live-round-home');

  const modal = document.getElementById('construction-modal');
  const modalClose = document.getElementById('construction-close');
  const underConstructionButtons = document.querySelectorAll('[data-under-construction]');

  let pendingAccount = null;
  let currentLobbyRound = null;
  let selectedCourse = null;
  let lobbyRefreshTimer = null;
  let viewedHole = null;

  const sessionToken = () => window.localStorage.getItem(SESSION_KEY) || '';

  const saveSession = (token) => {
    window.localStorage.setItem(SESSION_KEY, token);
  };

  const clearSession = () => {
    window.localStorage.removeItem(SESSION_KEY);
  };

  const setAuthMessage = (message = '') => {
    if (!authMessage) return;
    authMessage.textContent = message;
    authMessage.hidden = !message;
  };

  const setFormBusy = (form, busy) => {
    form?.querySelectorAll('button, input, select').forEach((control) => {
      control.disabled = busy;
    });
  };

  const setSettingsMessage = (message = '') => {
    if (!settingsMessage) return;
    settingsMessage.textContent = message;
    settingsMessage.hidden = !message;
  };

  const populateSettings = (preferences) => {
    if (!settingsForm) return;
    settingsForm.elements.mini_mascots_enabled.checked =
      Boolean(preferences?.mini_mascots_enabled);
    settingsForm.elements.trash_talk_enabled.checked =
      Boolean(preferences?.trash_talk_enabled);
    settingsForm.elements.drinking.checked =
      Boolean(preferences?.themes?.drinking);
    settingsForm.elements.wife.checked =
      Boolean(preferences?.themes?.wife);

    const vulgarity = String(preferences?.max_vulgarity || 'normal');
    const radio = settingsForm.querySelector(
      `input[name="max_vulgarity"][value="${vulgarity}"]`
    );
    if (radio) radio.checked = true;
  };

  const requestJson = async (path, options = {}) => {
    const {
      method = 'GET',
      body,
      authenticated = true,
    } = options;

    const headers = { Accept: 'application/json' };
    if (body !== undefined) headers['Content-Type'] = 'application/json';

    if (authenticated) {
      const token = sessionToken();
      if (token) headers.Authorization = `Bearer ${token}`;
    }

    let response;
    try {
      response = await fetch(path, {
        method,
        headers,
        body: body === undefined ? undefined : JSON.stringify(body),
      });
    } catch (_error) {
      throw new Error('Could not reach the server.');
    }

    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(payload.error || `Request failed (${response.status})`);
    }
    return payload;
  };

  const switchAuthView = (view) => {
    setAuthMessage('');
    pendingAccount = null;
    if (recoveryCard) recoveryCard.hidden = true;
    if (authTabs) authTabs.hidden = false;

    authViewButtons.forEach((button) => {
      button.classList.toggle('is-active', button.dataset.authView === view);
    });
    authPanels.forEach((panel) => {
      panel.hidden = panel.dataset.authPanel !== view;
    });
  };

  const showAuth = (view = 'login') => {
    document.body.classList.remove('app-ready');
    if (appShell) appShell.setAttribute('aria-hidden', 'true');
    if (authShell) authShell.hidden = false;
    switchAuthView(view);
  };

  const showApp = (account) => {
    pendingAccount = null;
    if (authShell) authShell.hidden = true;
    if (appShell) appShell.removeAttribute('aria-hidden');
    if (welcomeKicker) {
      const name = String(account?.display_name || '').trim();
      welcomeKicker.textContent = name
        ? `WELCOME BACK, ${name.toUpperCase()}`
        : 'WELCOME BACK';
    }
    document.body.classList.add('app-ready');
  };

  const showRecoveryKey = (result) => {
    pendingAccount = result.account || null;
    if (authTabs) authTabs.hidden = true;
    authPanels.forEach((panel) => {
      panel.hidden = true;
    });
    setAuthMessage('');
    if (recoveryKeyValue) recoveryKeyValue.textContent = result.recovery_key || '';
    if (recoveryKeyCopy) recoveryKeyCopy.textContent = 'COPY KEY';
    if (recoveryCard) recoveryCard.hidden = false;
  };

  const acceptAuthResult = (result, { showRecovery = false } = {}) => {
    const token = result?.session?.token;
    if (!token) throw new Error('Server did not return a session token.');
    saveSession(token);

    if (showRecovery) {
      showRecoveryKey(result);
      return;
    }
    showApp(result.account);
  };

  const bootSession = async () => {
    const token = sessionToken();
    if (!token) {
      showAuth('login');
      return;
    }

    try {
      const account = await requestJson('/api/auth/me');
      showApp(account);
    } catch (_error) {
      clearSession();
      showAuth('login');
    }
  };

  const revealShell = async () => {
    if (splash) splash.classList.add('splash-leaving');
    window.setTimeout(async () => {
      if (splash) splash.hidden = true;
      await bootSession();
    }, 260);
  };

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.setTimeout(revealShell, prefersReducedMotion ? 350 : 1450);

  authViewButtons.forEach((button) => {
    button.addEventListener('click', () => switchAuthView(button.dataset.authView));
  });

  loginForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setAuthMessage('');
    setFormBusy(loginForm, true);
    const values = new FormData(loginForm);

    try {
      const result = await requestJson('/api/auth/login', {
        method: 'POST',
        authenticated: false,
        body: {
          username: values.get('username'),
          password: values.get('password'),
        },
      });
      acceptAuthResult(result);
      loginForm.reset();
    } catch (error) {
      setAuthMessage(error.message);
    } finally {
      setFormBusy(loginForm, false);
    }
  });

  registerForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setAuthMessage('');
    setFormBusy(registerForm, true);
    const values = new FormData(registerForm);

    try {
      const result = await requestJson('/api/auth/register', {
        method: 'POST',
        authenticated: false,
        body: {
          display_name: values.get('display_name'),
          username: values.get('username'),
          password: values.get('password'),
        },
      });
      acceptAuthResult(result, { showRecovery: true });
      registerForm.reset();
    } catch (error) {
      setAuthMessage(error.message);
    } finally {
      setFormBusy(registerForm, false);
    }
  });

  recoverForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setAuthMessage('');
    setFormBusy(recoverForm, true);
    const values = new FormData(recoverForm);

    try {
      const result = await requestJson('/api/auth/recover', {
        method: 'POST',
        authenticated: false,
        body: {
          recovery_key: values.get('recovery_key'),
          new_password: values.get('new_password'),
        },
      });
      acceptAuthResult(result, { showRecovery: true });
      recoverForm.reset();
    } catch (error) {
      setAuthMessage(error.message);
    } finally {
      setFormBusy(recoverForm, false);
    }
  });

  recoveryKeyCopy?.addEventListener('click', async () => {
    const key = recoveryKeyValue?.textContent || '';
    if (!key) return;

    try {
      await navigator.clipboard.writeText(key);
      recoveryKeyCopy.textContent = 'COPIED';
    } catch (_error) {
      recoveryKeyCopy.textContent = 'SELECT + COPY';
      window.getSelection()?.selectAllChildren(recoveryKeyValue);
    }
  });

  recoveryKeyContinue?.addEventListener('click', () => {
    if (pendingAccount) {
      showApp(pendingAccount);
    } else {
      showAuth('login');
    }
  });

  logoutButton?.addEventListener('click', async () => {
    const token = sessionToken();
    if (token) {
      try {
        await requestJson('/api/auth/logout', { method: 'POST' });
      } catch (_error) {
        // Local logout still wins if the session already expired or the network is down.
      }
    }
    clearSession();
    showAuth('login');
  });

  const teeOptionLabel = (tee) => {
    const yardage = tee?.total_yardage ? ` • ${tee.total_yardage} YDS` : '';
    return `${tee?.tee_name || 'Tee'}${yardage}`;
  };

  const fillTeeSelect = (select, tees, selected = '') => {
    if (!select) return;
    select.replaceChildren();

    (tees || []).forEach((tee) => {
      const option = document.createElement('option');
      option.value = tee.tee_name;
      option.textContent = teeOptionLabel(tee);
      option.selected = tee.tee_name === selected;
      select.append(option);
    });
  };

  const clearSelectedCourse = () => {
    selectedCourse = null;
    if (selectedCourseBox) selectedCourseBox.hidden = true;
    if (selectedCourseName) selectedCourseName.textContent = '';
    if (selectedCourseLocation) selectedCourseLocation.textContent = '';
    if (startTeeField) startTeeField.hidden = true;
    if (startTeeSelect) startTeeSelect.replaceChildren();
  };

  const setCourseMode = (mode) => {
    const useCourse = mode === 'course';
    if (courseSearchPanel) courseSearchPanel.hidden = !useCourse;
    if (freePlayField) freePlayField.hidden = useCourse;
    if (!useCourse) {
      clearSelectedCourse();
      if (courseResults) courseResults.replaceChildren();
    }
  };

  const selectCourseResult = async (result) => {
    setRoundFlowMessage('Loading course...');
    const body = result.course_id
      ? { course_id: result.course_id }
      : { external_course_id: result.external_course_id };

    try {
      const course = await requestJson('/api/courses/select', {
        method: 'POST',
        body,
      });
      selectedCourse = course;

      if (selectedCourseName) selectedCourseName.textContent = course.name || 'Selected course';
      if (selectedCourseLocation) {
        const pieces = [result.city, result.state, result.country].filter(Boolean);
        selectedCourseLocation.textContent = pieces.join(', ');
      }
      if (selectedCourseBox) selectedCourseBox.hidden = false;

      const tees = course.tees || [];
      fillTeeSelect(startTeeSelect, tees);
      if (startTeeField) startTeeField.hidden = tees.length === 0;
      if (courseResults) courseResults.replaceChildren();
      setRoundFlowMessage('');
    } catch (error) {
      setRoundFlowMessage(error.message);
    }
  };

  const renderCourseResults = (results) => {
    if (!courseResults) return;
    courseResults.replaceChildren();

    if (!results.length) {
      const empty = document.createElement('div');
      empty.className = 'selected-course';
      empty.textContent = 'No course found. Try another search or use Free Play.';
      courseResults.append(empty);
      return;
    }

    results.forEach((result) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'course-result';

      const name = document.createElement('strong');
      name.textContent = result.name;

      const details = document.createElement('small');
      const location = [result.city, result.state, result.country].filter(Boolean);
      const source = result.source === 'cache' ? 'SAVED COURSE' : 'COURSE SEARCH';
      details.textContent = location.length
        ? `${location.join(', ')} • ${source}`
        : source;

      button.append(name, details);
      button.addEventListener('click', () => selectCourseResult(result));
      courseResults.append(button);
    });
  };

  const searchCourses = async () => {
    const query = String(courseSearchInput?.value || '').trim();
    if (query.length < 2) {
      setRoundFlowMessage('Type at least 2 characters to search courses.');
      return;
    }

    setRoundFlowMessage('Searching courses...');
    if (courseSearchButton) courseSearchButton.disabled = true;
    try {
      const payload = await requestJson(
        `/api/courses/search?q=${encodeURIComponent(query)}&limit=10`
      );
      renderCourseResults(payload.results || []);
      setRoundFlowMessage('');
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      if (courseSearchButton) courseSearchButton.disabled = false;
    }
  };

  const setRoundFlowMessage = (message = '') => {
    if (!roundFlowMessage) return;
    roundFlowMessage.textContent = message;
    roundFlowMessage.hidden = !message;
  };

  const closeRoundFlow = () => {
    if (!roundFlowModal) return;
    roundFlowModal.hidden = true;
    document.body.classList.remove('modal-open');
    setRoundFlowMessage('');
    currentLobbyRound = null;
    viewedHole = null;
    clearSelectedCourse();
    if (lobbyRefreshTimer) {
      window.clearInterval(lobbyRefreshTimer);
      lobbyRefreshTimer = null;
    }
  };

  const showRoundPanel = (panel) => {
    if (!roundFlowModal) return;
    roundFlowModal.hidden = false;
    document.body.classList.add('modal-open');
    setRoundFlowMessage('');
    currentLobbyRound = null;

    if (startRoundForm) startRoundForm.hidden = panel !== 'start';
    if (joinRoundForm) joinRoundForm.hidden = panel !== 'join';
    if (lobbyPanel) lobbyPanel.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = true;
    if (roundFlowTitle) {
      roundFlowTitle.textContent = panel === 'start' ? 'START A ROUND' : 'JOIN A ROUND';
    }
    if (panel === 'start') {
      clearSelectedCourse();
      setCourseMode(
        startRoundForm?.querySelector('input[name="course_mode"]:checked')?.value
        || 'course'
      );
    }
    roundFlowClose?.focus();
  };

  const renderLobby = (round) => {
    currentLobbyRound = round;
    if (startRoundForm) startRoundForm.hidden = true;
    if (joinRoundForm) joinRoundForm.hidden = true;
    if (lobbyPanel) lobbyPanel.hidden = false;
    if (roundFlowTitle) roundFlowTitle.textContent = 'LOBBY';
    if (lobbyCode) lobbyCode.textContent = round.active_code || '----';

    const modeLabel =
      round.mode === 'scramble' ? 'WE SUCK TOGETHER' : 'EVERY ASSHOLE FOR THEMSELVES';
    const place = round.course?.name || round.free_play_name || 'Course round';
    if (lobbySummary) {
      lobbySummary.textContent = `${modeLabel} • ${round.hole_count} HOLES • ${place}`;
    }

    if (lobbyParticipants) {
      lobbyParticipants.replaceChildren();
      (round.participants || []).forEach((participant) => {
        const row = document.createElement('div');
        row.className = 'lobby-person';

        const name = document.createElement('span');
        name.textContent = participant.display_name || 'Unknown golfer';

        const role = document.createElement('small');
        const tee = participant.tee_name ? ` • ${participant.tee_name} TEE` : '';
        role.textContent = `${participant.role || 'player'}${tee}`;

        row.append(name, role);
        lobbyParticipants.append(row);
      });
    }

    const tees = round.available_tees || [];
    const viewer = (round.participants || []).find(
      (participant) => String(participant.id) === String(round.viewer_participant_id)
    );
    const canChooseTee =
      round.viewer_role === 'player'
      && round.status === 'setup'
      && tees.length > 0;

    if (lobbyTeePanel) lobbyTeePanel.hidden = !canChooseTee;
    if (canChooseTee) {
      fillTeeSelect(lobbyTeeSelect, tees, viewer?.tee_name || '');
    }

    if (lobbyStart) {
      const canStart = round.viewer_role === 'player' && round.status === 'setup';
      const missingTee = tees.length > 0 && (round.participants || []).some(
        (participant) => participant.role === 'player' && !participant.tee_name
      );
      lobbyStart.hidden = !canStart;
      lobbyStart.disabled = missingTee;
      if (canStart && missingTee) {
        setRoundFlowMessage('Every player needs to pick a tee before the round starts.');
      }
    }

    if (round.status === 'active') {
      setRoundFlowMessage('Round is live. The scorecard view is the next build step.');
    } else {
      setRoundFlowMessage('');
    }
  };

  const refreshLobby = async (code) => {
    const round = await requestJson(`/api/rounds/code/${encodeURIComponent(code)}`);
    renderLobby(round);
    return round;
  };

  const startLobbyPolling = (code) => {
    if (lobbyRefreshTimer) window.clearInterval(lobbyRefreshTimer);
    lobbyRefreshTimer = window.setInterval(async () => {
      if (!roundFlowModal || roundFlowModal.hidden || !currentLobbyRound) return;
      try {
        await refreshLobby(code);
      } catch (_error) {
        // A manual action will surface useful errors. Polling stays quiet.
      }
    }, 3000);
  };

  startRoundButton?.addEventListener('click', () => showRoundPanel('start'));
  joinRoundButton?.addEventListener('click', () => showRoundPanel('join'));
  roundFlowClose?.addEventListener('click', closeRoundFlow);
  lobbyHome?.addEventListener('click', closeRoundFlow);
  roundFlowModal?.addEventListener('click', (event) => {
    if (event.target === roundFlowModal) closeRoundFlow();
  });

  startRoundForm?.querySelectorAll('input[name="course_mode"]').forEach((radio) => {
    radio.addEventListener('change', () => setCourseMode(radio.value));
  });

  courseSearchButton?.addEventListener('click', searchCourses);
  courseSearchInput?.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter') return;
    event.preventDefault();
    searchCourses();
  });

  startRoundForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setRoundFlowMessage('');
    setFormBusy(startRoundForm, true);
    const values = new FormData(startRoundForm);

    try {
      const courseMode = values.get('course_mode');
      if (courseMode === 'course' && !selectedCourse?.id) {
        throw new Error('Pick a course first, or switch to Free Play.');
      }

      const body = {
        mode: values.get('mode'),
        holes: Number(values.get('holes')),
      };

      if (courseMode === 'course') {
        body.course_id = selectedCourse.id;
        if (startTeeSelect?.value) body.tee_name = startTeeSelect.value;
      } else {
        body.free_play_name =
          String(values.get('free_play_name') || '').trim() || 'Free Play';
      }

      const created = await requestJson('/api/rounds', {
        method: 'POST',
        body,
      });
      await refreshLobby(created.active_code);
      startLobbyPolling(created.active_code);
      startRoundForm.reset();
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      setFormBusy(startRoundForm, false);
    }
  });

  joinRoundForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setRoundFlowMessage('');
    setFormBusy(joinRoundForm, true);
    const values = new FormData(joinRoundForm);
    const code = String(values.get('code') || '').trim();

    try {
      await requestJson('/api/rounds/join', {
        method: 'POST',
        body: {
          code,
          role: values.get('role'),
        },
      });
      await refreshLobby(code);
      startLobbyPolling(code);
      joinRoundForm.reset();
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      setFormBusy(joinRoundForm, false);
    }
  });

  lobbyTeeSave?.addEventListener('click', async () => {
    if (!currentLobbyRound || !lobbyTeeSelect?.value) return;
    lobbyTeeSave.disabled = true;
    setRoundFlowMessage('');

    try {
      await requestJson(`/api/rounds/${currentLobbyRound.id}/tee`, {
        method: 'PATCH',
        body: { tee_name: lobbyTeeSelect.value },
      });
      await refreshLobby(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      lobbyTeeSave.disabled = false;
    }
  });

  lobbyStart?.addEventListener('click', async () => {
    if (!currentLobbyRound) return;
    lobbyStart.disabled = true;
    setRoundFlowMessage('');

    try {
      await requestJson(`/api/rounds/${currentLobbyRound.id}/status`, {
        method: 'PATCH',
        body: { status: 'active' },
      });
      await refreshLobby(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      lobbyStart.disabled = false;
    }
  });

  const openSettings = async () => {
    if (!settingsModal || !settingsForm) return;
    setSettingsMessage('');
    settingsModal.hidden = false;
    document.body.classList.add('modal-open');

    try {
      const preferences = await requestJson('/api/preferences');
      populateSettings(preferences);
      settingsClose?.focus();
    } catch (error) {
      setSettingsMessage(error.message);
    }
  };

  const closeSettings = () => {
    if (!settingsModal) return;
    settingsModal.hidden = true;
    document.body.classList.remove('modal-open');
  };

  settingsButton?.addEventListener('click', openSettings);
  settingsClose?.addEventListener('click', closeSettings);
  settingsModal?.addEventListener('click', (event) => {
    if (event.target === settingsModal) closeSettings();
  });

  settingsForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setSettingsMessage('');
    setFormBusy(settingsForm, true);

    const checkedVulgarity = settingsForm.querySelector(
      'input[name="max_vulgarity"]:checked'
    );

    try {
      const preferences = await requestJson('/api/preferences', {
        method: 'PATCH',
        body: {
          mini_mascots_enabled:
            settingsForm.elements.mini_mascots_enabled.checked,
          trash_talk_enabled:
            settingsForm.elements.trash_talk_enabled.checked,
          max_vulgarity: checkedVulgarity?.value || 'normal',
          themes: {
            drinking: settingsForm.elements.drinking.checked,
            wife: settingsForm.elements.wife.checked,
          },
        },
      });
      populateSettings(preferences);
      setSettingsMessage('Saved. Your bad decisions are now personalized.');
    } catch (error) {
      setSettingsMessage(error.message);
    } finally {
      setFormBusy(settingsForm, false);
    }
  });

  const openConstruction = () => {
    if (!modal) return;
    modal.hidden = false;
    document.body.classList.add('modal-open');
    modalClose?.focus();
  };

  const closeConstruction = () => {
    if (!modal) return;
    modal.hidden = true;
    document.body.classList.remove('modal-open');
  };

  underConstructionButtons.forEach((button) => {
    button.addEventListener('click', openConstruction);
  });

  modalClose?.addEventListener('click', closeConstruction);
  modal?.addEventListener('click', (event) => {
    if (event.target === modal) closeConstruction();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    if (roundFlowModal && !roundFlowModal.hidden) {
      closeRoundFlow();
      return;
    }
    if (settingsModal && !settingsModal.hidden) {
      closeSettings();
      return;
    }
    if (modal && !modal.hidden) closeConstruction();
  });

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/service-worker.js').catch(() => {
        // The shell still works normally if service-worker registration fails.
      });
    });
  }
})();
