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
  const scrambleContributionPanel = document.getElementById('scramble-contribution-panel');
  const scrambleContributionList = document.getElementById('scramble-contribution-list');
  const finishRoundButton = document.getElementById('finish-round-button');
  const liveRoundHome = document.getElementById('live-round-home');
  const roundEndPanel = document.getElementById('round-end-panel');
  const roundEndTitle = document.getElementById('round-end-title');
  const roundEndSummary = document.getElementById('round-end-summary');
  const roundEndResults = document.getElementById('round-end-results');
  const downloadReportButton = document.getElementById('download-report-button');
  const roundEndHome = document.getElementById('round-end-home');
  const receiptsPanel = document.getElementById('receipts-panel');
  const receiptsList = document.getElementById('receipts-list');
  const bagButton = document.getElementById('bag-of-bullshit-button');
  const bagModal = document.getElementById('bag-modal');
  const bagClose = document.getElementById('bag-close');
  const bagMessage = document.getElementById('bag-message');
  const bagActions = document.getElementById('bag-actions');
  const bagActionButtons = document.querySelectorAll('[data-bag-action]');
  const bagForm = document.getElementById('bag-form');
  const bagFormTitle = document.getElementById('bag-form-title');
  const bagFormCancel = document.getElementById('bag-form-cancel');
  const bagTargetField = document.getElementById('bag-target-field');
  const bagTargetSelect = document.getElementById('bag-target-select');
  const bagSituationField = document.getElementById('bag-situation-field');
  const bagSituationSelect = document.getElementById('bag-situation-select');
  const bagShotField = document.getElementById('bag-shot-field');
  const bagShotSelect = document.getElementById('bag-shot-select');
  const bagExcuseField = document.getElementById('bag-excuse-field');
  const bagExcuseSelect = document.getElementById('bag-excuse-select');
  const bagTextField = document.getElementById('bag-text-field');
  const bagTextLabel = document.getElementById('bag-text-label');
  const bagTextInput = document.getElementById('bag-text-input');
  const bagSubmit = document.getElementById('bag-submit');
  const bagReactionButtons = document.querySelectorAll('[data-reaction]');

  const modal = document.getElementById('construction-modal');
  const modalClose = document.getElementById('construction-close');
  const underConstructionButtons = document.querySelectorAll('[data-under-construction]');

  let pendingAccount = null;
  let currentLobbyRound = null;
  let selectedCourse = null;
  let lobbyRefreshTimer = null;
  let viewedHole = null;
  let currentBagAction = null;

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
    if (bagModal) bagModal.hidden = true;
    currentBagAction = null;
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
    if (roundEndPanel) roundEndPanel.hidden = true;
    if (receiptsPanel) receiptsPanel.hidden = true;
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

  const findPar = (round, hole) => {
    const row = (round.pars || []).find(
      (item) => Number(item.hole_number) === Number(hole)
    );
    return row ? Number(row.par) : null;
  };

  const findScore = (round, hole, participantId = null) => {
    return (round.scores || []).find((score) => {
      if (Number(score.hole_number) !== Number(hole)) return false;
      if (round.mode === 'scramble') return score.score_scope === 'team';
      return (
        score.score_scope === 'player'
        && String(score.player_participant_id) === String(participantId)
      );
    }) || null;
  };

  const findScoreEvent = (round, hole, participantId = null) => {
    return (round.events || []).find((event) => {
      if (!['score_report', 'score_push'].includes(event.event_type)) return false;
      if (Number(event.hole_number) !== Number(hole)) return false;
      const data = event.data || {};
      if (round.mode === 'scramble') return data.scope === 'team';
      return (
        data.scope === 'player'
        && String(data.player_participant_id) === String(participantId)
      );
    }) || null;
  };

  const scoreResponses = (round, scoreEventId) => {
    if (!scoreEventId) return [];
    return (round.events || []).filter(
      (event) =>
        event.event_type === 'score_response'
        && String(event.reply_to_event_id || '') === String(scoreEventId)
    );
  };

  const scoreRelativeLabel = (strokes, par) => {
    if (!Number.isFinite(strokes) || !Number.isFinite(par)) return '';
    const delta = strokes - par;
    if (delta === 0) return 'E';
    return delta > 0 ? `+${delta}` : String(delta);
  };

  const assetUrl = (path) => {
    const value = String(path || '').trim();
    if (!value) return '';
    if (value.startsWith('/')) return value;
    return `/${value}`;
  };

  const renderLatestPresentation = (round) => {
    if (!latestPresentation) return;

    const event = (round.events || []).find((item) => {
      const presentation = item.presentation || {};
      return (
        presentation.event_key
        || presentation.banter
        || presentation.mascot
        || presentation.fallback?.text
      );
    });

    if (!event) {
      latestPresentation.hidden = true;
      return;
    }

    const presentation = event.presentation || {};
    const eventMessage = String(event.data?.message || '').trim();
    const presentationText = presentation.banter?.text
      || presentation.mascot?.copy
      || presentation.fallback?.text
      || '';
    const banterText = eventMessage || presentationText;
    const fallbackText = eventMessage
      ? presentationText
      : (presentation.fallback?.text || '');

    if (latestBanter) latestBanter.textContent = banterText;
    if (latestFallback) {
      latestFallback.textContent =
        fallbackText && fallbackText !== banterText ? fallbackText : '';
    }

    const mascotPath = assetUrl(presentation.mascot?.production);
    if (latestMascot) {
      if (mascotPath) {
        latestMascot.src = mascotPath;
        latestMascot.alt = presentation.mascot?.copy || 'Who Pushed Me mascot';
        latestMascot.hidden = false;
      } else {
        latestMascot.removeAttribute('src');
        latestMascot.alt = '';
        latestMascot.hidden = true;
      }
    }

    latestPresentation.hidden = !banterText && !mascotPath;
  };

  const renderScoreCard = (round, hole) => {
    if (!liveScoreArea) return;
    liveScoreArea.replaceChildren();

    const par = findPar(round, hole);
    const canScore = round.viewer_role === 'player';

    const addCard = (label, participantId = null, detail = '') => {
      const score = findScore(round, hole, participantId);
      const card = document.createElement('section');
      card.className = 'live-score-card';

      const header = document.createElement('div');
      header.className = 'live-score-card-header';

      const name = document.createElement('strong');
      name.textContent = label;

      const status = document.createElement('small');
      const relative = score && par
        ? scoreRelativeLabel(Number(score.strokes), Number(par))
        : '';
      const pieces = [];
      if (detail) pieces.push(detail);
      if (relative) pieces.push(relative);
      status.textContent = pieces.join(' • ');

      header.append(name, status);
      card.append(header);

      if (!canScore) {
        const readonly = document.createElement('div');
        readonly.className = 'live-score-readonly';
        readonly.textContent = score
          ? `${score.strokes} STROKES`
          : 'NO SCORE YET';
        card.append(readonly);
        liveScoreArea.append(card);
        return;
      }

      const controls = document.createElement('div');
      controls.className = 'live-score-controls';

      const input = document.createElement('input');
      input.className = 'live-score-input';
      input.type = 'number';
      input.min = '1';
      input.max = '99';
      input.inputMode = 'numeric';
      input.value = score ? String(score.strokes) : '';
      input.placeholder = par ? String(par) : 'STROKES';
      input.setAttribute('aria-label', `${label} strokes for hole ${hole}`);

      const submit = document.createElement('button');
      submit.type = 'button';
      submit.className = 'live-score-submit';
      submit.textContent = score ? 'PUSH' : 'REPORT';

      submit.addEventListener('click', async () => {
        if (!currentLobbyRound) return;

        const strokes = Number(input.value);
        if (!Number.isInteger(strokes) || strokes < 1 || strokes > 99) {
          setRoundFlowMessage('Strokes must be between 1 and 99.');
          return;
        }

        submit.disabled = true;
        setRoundFlowMessage('');
        try {
          const body = { strokes };
          if (round.mode === 'individual') {
            body.player_participant_id = participantId;
          }

          await requestJson(
            `/api/rounds/${round.id}/holes/${hole}/score`,
            {
              method: 'PUT',
              body,
            }
          );
          await refreshRound(round.active_code);
        } catch (error) {
          setRoundFlowMessage(error.message);
        } finally {
          submit.disabled = false;
        }
      });

      controls.append(input, submit);
      card.append(controls);

      if (score) {
        const scoreEvent = findScoreEvent(round, hole, participantId);
        if (scoreEvent) {
          const responsePanel = document.createElement('div');
          responsePanel.className = 'score-response-panel';

          const responseHeading = document.createElement('div');
          responseHeading.className = 'score-response-heading';
          responseHeading.textContent = 'RESPOND TO THIS SCORE';

          const responseButtons = document.createElement('div');
          responseButtons.className = 'score-response-buttons';

          const sendResponse = async (
            responseKind,
            {
              message = '',
              targetParticipantId = null,
            } = {}
          ) => {
            setRoundFlowMessage('');
            try {
              await requestJson(
                `/api/rounds/${round.id}/score-events/${scoreEvent.id}/responses`,
                {
                  method: 'POST',
                  body: {
                    response_kind: responseKind,
                    message: message || null,
                    target_participant_id: targetParticipantId,
                  },
                }
              );
              await refreshRound(round.active_code);
            } catch (error) {
              setRoundFlowMessage(error.message);
            }
          };

          [
            ['bullshit', 'BULLSHIT'],
            ['cheater', 'CHEATER'],
            ['lucky', 'LUCKY'],
            ['nice', 'NICE'],
            ['random', 'TALK SHIT'],
          ].forEach(([kind, labelText]) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.textContent = labelText;
            button.addEventListener('click', async () => {
              button.disabled = true;
              await sendResponse(kind);
              button.disabled = false;
            });
            responseButtons.append(button);
          });

          if (round.mode === 'scramble') {
            const blameWrap = document.createElement('div');
            blameWrap.className = 'score-response-blame';

            const blameSelect = document.createElement('select');
            const blank = document.createElement('option');
            blank.value = '';
            blank.textContent = 'WHO SCREWED IT UP?';
            blameSelect.append(blank);

            (round.participants || [])
              .filter((participant) => participant.role === 'player')
              .forEach((participant) => {
                const option = document.createElement('option');
                option.value = participant.id;
                option.textContent = participant.display_name || 'Golfer';
                blameSelect.append(option);
              });

            const blameButton = document.createElement('button');
            blameButton.type = 'button';
            blameButton.textContent = 'BLAME THEM';
            blameButton.addEventListener('click', async () => {
              if (!blameSelect.value) {
                setRoundFlowMessage('Pick who screwed it up first.');
                return;
              }
              blameButton.disabled = true;
              await sendResponse('blame', {
                targetParticipantId: blameSelect.value,
              });
              blameButton.disabled = false;
            });

            blameWrap.append(blameSelect, blameButton);
            responsePanel.append(responseHeading, responseButtons, blameWrap);
          } else {
            responsePanel.append(responseHeading, responseButtons);
          }

          const customWrap = document.createElement('div');
          customWrap.className = 'score-response-custom';

          const customInput = document.createElement('input');
          customInput.type = 'text';
          customInput.maxLength = 280;
          customInput.placeholder = 'Say something about this score...';

          const customButton = document.createElement('button');
          customButton.type = 'button';
          customButton.textContent = 'SEND';
          customButton.addEventListener('click', async () => {
            const message = customInput.value.trim();
            if (!message) return;
            customButton.disabled = true;
            await sendResponse('custom', { message });
            customButton.disabled = false;
          });

          customWrap.append(customInput, customButton);
          responsePanel.append(customWrap);

          const replies = scoreResponses(round, scoreEvent.id);
          if (replies.length) {
            const replyList = document.createElement('div');
            replyList.className = 'score-response-list';

            replies.slice().reverse().forEach((reply) => {
              const actor = (round.participants || []).find(
                (participant) =>
                  String(participant.id) === String(reply.actor_participant_id)
              );
              const line = document.createElement('div');
              line.className = 'score-response-line';

              const actorName = actor?.display_name || 'Someone';
              const text = presentationText(reply)
                || String(reply.data?.response_kind || 'responded').toUpperCase();
              line.textContent = `${actorName}: ${text}`;
              replyList.append(line);
            });

            responsePanel.append(replyList);
          }

          card.append(responsePanel);
        }
      }

      liveScoreArea.append(card);
    };

    if (round.mode === 'scramble') {
      addCard('TEAM SCORE', null, 'SCRAMBLE');
      return;
    }

    (round.participants || [])
      .filter((participant) => participant.role === 'player')
      .forEach((participant) => {
        addCard(
          participant.display_name || 'Golfer',
          participant.id,
          participant.tee_name ? `${participant.tee_name} TEE` : ''
        );
      });
  };

  const SCRAMBLE_SHOT_TYPES = [
    ['drive', 'DRIVE'],
    ['second', 'SECOND SHOT'],
    ['approach', 'APPROACH'],
    ['recovery', 'RECOVERY'],
    ['bunker', 'BUNKER'],
    ['putt', 'PUTT'],
    ['other', 'OTHER'],
  ];

  const renderScrambleContributions = (round, hole) => {
    if (!scrambleContributionPanel || !scrambleContributionList) return;

    if (round.mode !== 'scramble') {
      scrambleContributionPanel.hidden = true;
      scrambleContributionList.replaceChildren();
      return;
    }

    const teamScore = findScore(round, hole);
    if (!teamScore) {
      scrambleContributionPanel.hidden = true;
      scrambleContributionList.replaceChildren();
      return;
    }

    scrambleContributionPanel.hidden = false;
    scrambleContributionList.replaceChildren();

    const players = (round.participants || []).filter(
      (participant) => participant.role === 'player'
    );
    const canEdit = round.status === 'active';

    SCRAMBLE_SHOT_TYPES.forEach(([shotType, labelText]) => {
      const contribution = (round.contributions || []).find(
        (row) =>
          Number(row.hole_number) === Number(hole)
          && row.shot_type === shotType
      );

      const row = document.createElement('div');
      row.className = 'scramble-contribution-row';

      const label = document.createElement('label');
      label.textContent = labelText;
      row.append(label);

      if (!canEdit) {
        const readonly = document.createElement('div');
        readonly.className = 'scramble-contribution-readonly';
        const player = players.find(
          (candidate) =>
            String(candidate.id) === String(contribution?.player_participant_id)
        );
        readonly.textContent = player?.display_name || 'NOT CLAIMED';
        row.append(readonly);
        scrambleContributionList.append(row);
        return;
      }

      const select = document.createElement('select');
      select.setAttribute('aria-label', `${labelText} contribution`);

      const blank = document.createElement('option');
      blank.value = '';
      blank.textContent = 'NOT CLAIMED';
      select.append(blank);

      players.forEach((player) => {
        const option = document.createElement('option');
        option.value = player.id;
        option.textContent = player.display_name || 'Golfer';
        option.selected = (
          String(player.id) === String(contribution?.player_participant_id)
        );
        select.append(option);
      });

      select.addEventListener('change', async () => {
        if (!currentLobbyRound) return;
        select.disabled = true;
        setRoundFlowMessage('');

        try {
          await requestJson(
            `/api/rounds/${round.id}/holes/${hole}/contributions/${shotType}`,
            {
              method: 'PUT',
              body: {
                player_participant_id: select.value || null,
              },
            }
          );
          await refreshRound(round.active_code);
        } catch (error) {
          setRoundFlowMessage(error.message);
        } finally {
          select.disabled = false;
        }
      });

      row.append(select);
      scrambleContributionList.append(row);
    });
  };

  const presentationText = (event) => {
    const presentation = event?.presentation || {};
    const eventMessage = String(event?.data?.message || '').trim();
    return (
      eventMessage
      || presentation.banter?.text
      || presentation.mascot?.copy
      || presentation.fallback?.text
      || ''
    );
  };

  const renderReceipts = (round) => {
    if (!receiptsPanel || !receiptsList) return;

    const events = round.events || [];
    receiptsPanel.hidden = events.length === 0;
    receiptsList.replaceChildren();

    events.slice(0, 40).forEach((event) => {
      const row = document.createElement('div');
      row.className = 'receipt-row';

      const title = document.createElement('strong');
      title.textContent = (
        presentationText(event)
        || event.content_event_key
        || event.event_type
        || 'Round event'
      );

      const meta = document.createElement('small');
      const pieces = [];
      if (event.hole_number) pieces.push(`HOLE ${event.hole_number}`);
      if (event.content_event_key) pieces.push(event.content_event_key);
      if (event.created_at) {
        const date = new Date(event.created_at);
        if (!Number.isNaN(date.getTime())) {
          pieces.push(
            date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
          );
        }
      }
      meta.textContent = pieces.join(' • ');

      row.append(title, meta);
      receiptsList.append(row);
    });
  };

  const totalParForRound = (round) => {
    const pars = round.pars || [];
    if (pars.length < Number(round.hole_count)) return null;
    return pars.reduce((total, row) => total + Number(row.par || 0), 0);
  };

  const roundEndEventForPlayer = (round, participantId) => {
    return (round.events || []).find(
      (event) =>
        event.event_type === 'round_end_result'
        && String(event.data?.player_participant_id || '') === String(participantId)
    ) || null;
  };

  const appendResultPresentation = (card, event) => {
    if (!event) return;
    const presentation = event.presentation || {};
    const text = presentationText(event);
    const mascotPath = assetUrl(presentation.mascot?.production);
    if (!text && !mascotPath) return;

    const wrap = document.createElement('div');
    wrap.className = 'round-end-result-presentation';

    if (mascotPath) {
      const image = document.createElement('img');
      image.src = mascotPath;
      image.alt = presentation.mascot?.copy || 'Who Pushed Me mascot';
      wrap.append(image);
    }

    const copy = document.createElement('span');
    copy.textContent = text;
    wrap.append(copy);
    card.append(wrap);
  };

  const renderRoundEnd = (round) => {
    currentLobbyRound = round;
    viewedHole = null;

    if (startRoundForm) startRoundForm.hidden = true;
    if (joinRoundForm) joinRoundForm.hidden = true;
    if (lobbyPanel) lobbyPanel.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = true;
    if (roundEndPanel) roundEndPanel.hidden = false;
    if (roundFlowTitle) roundFlowTitle.textContent = 'ROUND COMPLETE';

    if (lobbyRefreshTimer) {
      window.clearInterval(lobbyRefreshTimer);
      lobbyRefreshTimer = null;
    }

    const place = round.course?.name || round.free_play_name || 'Golf';
    if (roundEndTitle) roundEndTitle.textContent = 'THE DAMAGE IS FINAL.';
    if (roundEndResults) roundEndResults.replaceChildren();

    const totalPar = totalParForRound(round);

    if (round.mode === 'scramble') {
      const total = round.results?.team_total;
      const relative = totalPar && total
        ? scoreRelativeLabel(Number(total), Number(totalPar))
        : '';

      if (roundEndSummary) {
        roundEndSummary.textContent = [
          place,
          total ? `${total} STROKES` : '',
          relative ? `${relative} TO PAR` : '',
        ].filter(Boolean).join(' • ');
      }

      const event = (round.events || []).find(
        (item) =>
          item.event_type === 'round_end_result'
          && item.content_event_key === 'round.end.scramble.complete'
      );

      const card = document.createElement('section');
      card.className = 'round-end-result-card is-first';

      const rank = document.createElement('div');
      rank.className = 'round-end-result-rank';
      rank.textContent = '✓';

      const main = document.createElement('div');
      main.className = 'round-end-result-main';

      const name = document.createElement('strong');
      name.textContent = 'WE SUCK TOGETHER';

      const score = document.createElement('small');
      score.textContent = total ? `${total} TOTAL STROKES` : 'ROUND COMPLETE';

      main.append(name, score);
      card.append(rank, main);
      appendResultPresentation(card, event);
      roundEndResults?.append(card);
    } else {
      if (roundEndSummary) {
        roundEndSummary.textContent = place;
      }

      const players = [...(round.results?.players || [])].sort(
        (a, b) =>
          Number(a.rank || 999) - Number(b.rank || 999)
          || Number(a.total_strokes || 9999) - Number(b.total_strokes || 9999)
      );

      players.forEach((result) => {
        const card = document.createElement('section');
        card.className = 'round-end-result-card';
        if (Number(result.rank) === 1) card.classList.add('is-first');

        const rank = document.createElement('div');
        rank.className = 'round-end-result-rank';
        const tied = Number(result.tie_count) > 1;
        rank.textContent = tied ? `T${result.rank}` : `#${result.rank}`;

        const main = document.createElement('div');
        main.className = 'round-end-result-main';

        const name = document.createElement('strong');
        name.textContent = result.display_name || 'Golfer';

        const relative = totalPar && result.total_strokes
          ? scoreRelativeLabel(
              Number(result.total_strokes),
              Number(totalPar)
            )
          : '';
        const score = document.createElement('small');
        score.textContent = [
          `${result.total_strokes} STROKES`,
          relative ? `${relative} TO PAR` : '',
        ].filter(Boolean).join(' • ');

        main.append(name, score);
        card.append(rank, main);
        appendResultPresentation(
          card,
          roundEndEventForPlayer(round, result.participant_id)
        );
        roundEndResults?.append(card);
      });
    }

    renderReceipts(round);
    setRoundFlowMessage('');
  };

  const renderLiveRound = (round) => {
    const previousRound = currentLobbyRound;
    const wasFollowingLive = (
      viewedHole === null
      || !previousRound
      || Number(viewedHole) === Number(previousRound.current_hole)
    );

    currentLobbyRound = round;

    if (wasFollowingLive) {
      viewedHole = Number(round.current_hole);
    } else {
      viewedHole = Math.min(
        Number(viewedHole),
        Number(round.current_hole)
      );
    }

    if (startRoundForm) startRoundForm.hidden = true;
    if (joinRoundForm) joinRoundForm.hidden = true;
    if (lobbyPanel) lobbyPanel.hidden = true;
    if (roundEndPanel) roundEndPanel.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = false;
    if (roundFlowTitle) roundFlowTitle.textContent = 'LIVE ROUND';

    const place = round.course?.name || round.free_play_name || 'Golf';
    if (liveRoundPlace) liveRoundPlace.textContent = place;
    if (liveRoundCode) liveRoundCode.textContent = round.active_code || '----';

    const par = findPar(round, viewedHole);
    const viewingLive = Number(viewedHole) === Number(round.current_hole);

    if (holeNumber) holeNumber.textContent = String(viewedHole);
    if (holeParLabel) {
      holeParLabel.textContent = par ? `PAR ${par}` : 'PAR ?';
    }
    if (holeStateLabel) {
      holeStateLabel.textContent = viewingLive
        ? 'LIVE HOLE'
        : `OLD HOLE • LIVE ${round.current_hole}`;
    }

    if (holePrev) {
      holePrev.disabled = Number(viewedHole) <= 1;
    }
    if (holeNext) {
      const canBrowseForward = Number(viewedHole) < Number(round.current_hole);
      const canAdvanceLive = (
        viewingLive
        && round.viewer_role === 'player'
        && Number(round.current_hole) < Number(round.hole_count)
      );
      holeNext.disabled = !canBrowseForward && !canAdvanceLive;
    }

    if (parInput) {
      parInput.value = par ? String(par) : '';
      parInput.disabled = round.viewer_role !== 'player';
    }
    if (parSubmit) {
      parSubmit.textContent = par ? 'PUSH PAR' : 'REPORT PAR';
      parSubmit.disabled = round.viewer_role !== 'player';
    }

    renderScoreCard(round, viewedHole);
    renderScrambleContributions(round, viewedHole);
    renderLatestPresentation(round);
    renderReceipts(round);

    if (finishRoundButton) {
      const canFinish = (
        round.viewer_role === 'player'
        && viewingLive
        && Number(round.current_hole) === Number(round.hole_count)
      );
      finishRoundButton.hidden = !canFinish;
      finishRoundButton.disabled = false;
    }

    if (round.status === 'active') {
      setRoundFlowMessage('');
    }
  };

  const renderLobby = (round) => {
    currentLobbyRound = round;
    viewedHole = null;
    if (startRoundForm) startRoundForm.hidden = true;
    if (joinRoundForm) joinRoundForm.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = true;
    if (roundEndPanel) roundEndPanel.hidden = true;
    if (receiptsPanel) receiptsPanel.hidden = true;
    if (scrambleContributionPanel) scrambleContributionPanel.hidden = true;
    if (finishRoundButton) finishRoundButton.hidden = true;
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
      } else {
        setRoundFlowMessage('');
      }
    }
  };

  const renderRoundState = (round) => {
    if (round.status === 'completed') {
      renderRoundEnd(round);
    } else if (round.status === 'active') {
      renderLiveRound(round);
    } else {
      renderLobby(round);
    }
  };

  const refreshRound = async (code) => {
    const round = await requestJson(`/api/rounds/code/${encodeURIComponent(code)}`);
    renderRoundState(round);
    return round;
  };

  const refreshLobby = refreshRound;

  const startLobbyPolling = (code) => {
    if (lobbyRefreshTimer) window.clearInterval(lobbyRefreshTimer);
    lobbyRefreshTimer = window.setInterval(async () => {
      if (!roundFlowModal || roundFlowModal.hidden || !currentLobbyRound) return;
      try {
        await refreshRound(code);
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

  liveRoundHome?.addEventListener('click', closeRoundFlow);
  roundEndHome?.addEventListener('click', closeRoundFlow);

  downloadReportButton?.addEventListener('click', async () => {
    if (!currentLobbyRound || currentLobbyRound.status !== 'completed') return;

    downloadReportButton.disabled = true;
    setRoundFlowMessage('');

    try {
      const token = sessionToken();
      const response = await fetch(
        `/api/rounds/${encodeURIComponent(currentLobbyRound.id)}/report.pdf`,
        {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        }
      );

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(
          payload.error || `Report download failed (${response.status})`
        );
      }

      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = objectUrl;
      link.download =
        `who-pushed-me-${currentLobbyRound.active_code}-final-damage-report.pdf`;
      document.body.append(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1500);
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      downloadReportButton.disabled = false;
    }
  });

  finishRoundButton?.addEventListener('click', async () => {
    if (!currentLobbyRound || currentLobbyRound.viewer_role !== 'player') return;

    finishRoundButton.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/status`,
        {
          method: 'PATCH',
          body: { status: 'completed' },
        }
      );
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      finishRoundButton.disabled = false;
    }
  });

  holePrev?.addEventListener('click', () => {
    if (!currentLobbyRound || viewedHole === null) return;
    if (Number(viewedHole) <= 1) return;
    viewedHole = Number(viewedHole) - 1;
    renderLiveRound(currentLobbyRound);
  });

  holeNext?.addEventListener('click', async () => {
    if (!currentLobbyRound || viewedHole === null) return;

    if (Number(viewedHole) < Number(currentLobbyRound.current_hole)) {
      viewedHole = Number(viewedHole) + 1;
      renderLiveRound(currentLobbyRound);
      return;
    }

    if (
      currentLobbyRound.viewer_role !== 'player'
      || Number(currentLobbyRound.current_hole) >= Number(currentLobbyRound.hole_count)
    ) {
      return;
    }

    holeNext.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/current-hole`,
        {
          method: 'PATCH',
          body: { hole: Number(currentLobbyRound.current_hole) + 1 },
        }
      );
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      holeNext.disabled = false;
    }
  });

  parForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!currentLobbyRound || viewedHole === null) return;
    if (currentLobbyRound.viewer_role !== 'player') return;

    const par = Number(parInput?.value);
    if (!Number.isInteger(par) || par < 2 || par > 7) {
      setRoundFlowMessage('Par must be between 2 and 7.');
      return;
    }

    if (parSubmit) parSubmit.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/holes/${viewedHole}/par`,
        {
          method: 'PUT',
          body: { par },
        }
      );
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      if (parSubmit) parSubmit.disabled = false;
    }
  });

  const setBagMessage = (message = '') => {
    if (!bagMessage) return;
    bagMessage.textContent = message;
    bagMessage.hidden = !message;
  };

  const populateBagTargets = () => {
    if (!bagTargetSelect || !currentLobbyRound) return;
    bagTargetSelect.replaceChildren();

    (currentLobbyRound.participants || [])
      .filter(
        (participant) =>
          String(participant.id) !== String(currentLobbyRound.viewer_participant_id)
      )
      .forEach((participant) => {
        const option = document.createElement('option');
        option.value = participant.id;
        option.textContent = participant.display_name || 'Unknown golfer';
        bagTargetSelect.append(option);
      });
  };

  const resetBagComposer = () => {
    currentBagAction = null;
    if (bagForm) bagForm.hidden = true;
    if (bagActions) bagActions.hidden = false;
    if (bagTargetField) bagTargetField.hidden = true;
    if (bagSituationField) bagSituationField.hidden = true;
    if (bagShotField) bagShotField.hidden = true;
    if (bagExcuseField) bagExcuseField.hidden = true;
    if (bagTextField) bagTextField.hidden = false;
    if (bagTextInput) {
      bagTextInput.value = '';
      bagTextInput.placeholder = 'Optional details';
    }
    if (bagSituationSelect) bagSituationSelect.value = '';
    if (bagShotSelect) bagShotSelect.value = '';
    if (bagExcuseSelect) bagExcuseSelect.value = '';
    setBagMessage('');
  };

  const openBag = () => {
    if (!bagModal || !currentLobbyRound || currentLobbyRound.status !== 'active') {
      return;
    }

    resetBagComposer();
    populateBagTargets();

    const spectator = currentLobbyRound.viewer_role === 'spectator';
    bagActionButtons.forEach((button) => {
      const action = button.dataset.bagAction;
      button.hidden = spectator && action !== 'open_mic';
    });

    bagModal.hidden = false;
    document.body.classList.add('modal-open');
    bagClose?.focus();
  };

  const closeBag = () => {
    if (!bagModal) return;
    bagModal.hidden = true;
    resetBagComposer();
  };

  const configureBagAction = (action) => {
    if (!bagForm || !bagActions) return;
    currentBagAction = action;
    bagActions.hidden = true;
    bagForm.hidden = false;
    setBagMessage('');

    const config = {
      callout: {
        title: 'CALL SOMEONE OUT',
        submit: 'CALL THEM OUT',
        target: true,
        situation: true,
        textLabel: 'ADD DETAILS',
        placeholder: 'Optional. Make it personal.',
        requiredText: false,
      },
      praise: {
        title: 'NICE FUCKING SHOT',
        submit: 'GIVE CREDIT',
        target: true,
        shot: true,
        textLabel: 'ADD DETAILS',
        placeholder: 'Optional. Try not to sound sincere.',
        requiredText: false,
      },
      shot_call: {
        title: 'CALL YOUR SHOT',
        submit: 'PUT IT ON THE RECORD',
        target: false,
        textLabel: 'WHAT ARE YOU CALLING?',
        placeholder: 'Example: I am carrying the bunker.',
        requiredText: true,
      },
      challenge: {
        title: "YOU WON'T",
        submit: 'ISSUE THE CHALLENGE',
        target: true,
        textLabel: "WHAT WON'T THEY DO?",
        placeholder: "Example: You won't go for the green.",
        requiredText: true,
      },
      excuse: {
        title: 'EXCUSE DEPARTMENT',
        submit: 'FILE THE EXCUSE',
        target: false,
        excuse: true,
        textLabel: 'YOUR OFFICIAL STATEMENT',
        placeholder: 'Optional additional bullshit.',
        requiredText: false,
      },
      open_mic: {
        title: 'OPEN MIC',
        submit: 'SAY IT',
        target: false,
        textLabel: 'MESSAGE',
        placeholder: 'Up to 280 characters.',
        requiredText: true,
      },
    }[action];

    if (!config) return;

    if (bagFormTitle) bagFormTitle.textContent = config.title;
    if (bagSubmit) bagSubmit.textContent = config.submit;
    if (bagTargetField) bagTargetField.hidden = !config.target;
    if (bagSituationField) bagSituationField.hidden = !config.situation;
    if (bagShotField) bagShotField.hidden = !config.shot;
    if (bagExcuseField) bagExcuseField.hidden = !config.excuse;
    if (bagTextLabel) bagTextLabel.textContent = config.textLabel;
    if (bagTextInput) {
      bagTextInput.value = '';
      bagTextInput.placeholder = config.placeholder;
      bagTextInput.required = Boolean(config.requiredText);
      bagTextInput.focus();
    }

    if (config.target && !bagTargetSelect?.options.length) {
      setBagMessage('Nobody else is here to target.');
      if (bagSubmit) bagSubmit.disabled = true;
    } else if (bagSubmit) {
      bagSubmit.disabled = false;
    }
  };

  const sendSocialEvent = async (type, data = {}) => {
    if (!currentLobbyRound) return;
    return requestJson(
      `/api/rounds/${currentLobbyRound.id}/events`,
      {
        method: 'POST',
        body: {
          type,
          hole: currentLobbyRound.current_hole,
          data,
        },
      }
    );
  };

  bagButton?.addEventListener('click', openBag);
  bagClose?.addEventListener('click', closeBag);
  bagModal?.addEventListener('click', (event) => {
    if (event.target === bagModal) closeBag();
  });
  bagFormCancel?.addEventListener('click', resetBagComposer);

  bagActionButtons.forEach((button) => {
    button.addEventListener('click', () => {
      configureBagAction(button.dataset.bagAction);
    });
  });

  bagForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!currentLobbyRound || !currentBagAction) return;

    const message = String(bagTextInput?.value || '').trim();
    if (bagTextInput?.required && !message) {
      setBagMessage('You opened your mouth. Finish the thought.');
      return;
    }

    const data = {};
    if (!bagTargetField?.hidden && bagTargetSelect?.value) {
      data.target_participant_id = bagTargetSelect.value;
    }
    if (!bagSituationField?.hidden && bagSituationSelect?.value) {
      data.situation = bagSituationSelect.value;
    }
    if (!bagShotField?.hidden && bagShotSelect?.value) {
      data.shot_type = bagShotSelect.value;
    }
    if (!bagExcuseField?.hidden && bagExcuseSelect?.value) {
      data.reason = bagExcuseSelect.value;
    }
    if (message) data.message = message;

    if (bagSubmit) bagSubmit.disabled = true;
    setBagMessage('');

    try {
      await sendSocialEvent(currentBagAction, data);
      closeBag();
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setBagMessage(error.message);
      if (bagSubmit) bagSubmit.disabled = false;
    }
  });

  bagReactionButtons.forEach((button) => {
    button.addEventListener('click', async () => {
      if (!currentLobbyRound) return;
      button.disabled = true;
      setBagMessage('');
      try {
        await sendSocialEvent('reaction', {
          reaction: button.dataset.reaction,
        });
        closeBag();
        await refreshRound(currentLobbyRound.active_code);
      } catch (error) {
        setBagMessage(error.message);
      } finally {
        button.disabled = false;
      }
    });
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
    if (bagModal && !bagModal.hidden) {
      closeBag();
      return;
    }
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
