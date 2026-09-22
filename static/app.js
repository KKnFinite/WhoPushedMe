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
  const advanceLiveHole = document.getElementById('advance-live-hole');
  const backToLive = document.getElementById('back-to-live');
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
  const finishIncompletePanel = document.getElementById('finish-incomplete-panel');
  const finishIncompleteCopy = document.getElementById('finish-incomplete-copy');
  const fixScorecardButton = document.getElementById('fix-scorecard-button');
  const finishIncompleteButton = document.getElementById('finish-incomplete-button');
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
  const towelButton = document.getElementById('towel-button');
  const towelPanel = document.getElementById('towel-panel');
  const towelReason = document.getElementById('towel-reason');
  const towelConfirm = document.getElementById('towel-confirm');
  const towelCancel = document.getElementById('towel-cancel');
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
  let viewedRoutePosition = null;
  let currentBagAction = null;
  let finishIncompletePending = false;

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
    viewedRoutePosition = null;
    finishIncompletePending = false;
    if (towelPanel) towelPanel.hidden = true;
    if (towelReason) towelReason.value = '';
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

  const routeEntry = (round, position) => {
    return (round.route || []).find(
      (item) => Number(item.route_position) === Number(position)
    ) || null;
  };

  const routeLength = (round) => {
    const route = round.route || [];
    return route.length || Number(round.hole_count || 0);
  };

  const viewerParticipant = (round) => {
    return (round.participants || []).find(
      (participant) =>
        String(participant.id) === String(round.viewer_participant_id)
    ) || null;
  };

  const viewerIsActivePlayer = (round) => {
    const viewer = viewerParticipant(round);
    return (
      round.viewer_role === 'player'
      && viewer?.participation_state === 'active'
    );
  };

  const findPar = (round, position) => {
    const row = (round.pars || []).find(
      (item) => Number(item.route_position) === Number(position)
    );
    return row ? Number(row.par) : null;
  };

  const findScore = (round, position, participantId = null) => {
    return (round.scores || []).find((score) => {
      if (Number(score.route_position) !== Number(position)) return false;
      if (round.mode === 'scramble') return score.score_scope === 'team';
      return (
        score.score_scope === 'player'
        && String(score.player_participant_id) === String(participantId)
      );
    }) || null;
  };

  const findScoreEvent = (round, position, participantId = null) => {
    return (round.events || []).find((event) => {
      if (!['score_report', 'score_push'].includes(event.event_type)) return false;
      if (Number(event.route_position) !== Number(position)) return false;
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

  const eventReactions = (round, eventId) => {
    return (round.reactions || []).filter(
      (reaction) => String(reaction.event_id) === String(eventId)
    );
  };

  const activeScoreChallenges = (round, scoreEventId) => {
    return (round.score_challenges || []).filter(
      (challenge) =>
        String(challenge.score_event_id) === String(scoreEventId)
        && challenge.status === 'active'
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

  const appendScoreResponsePanel = (
    card,
    round,
    position,
    participantId,
    score
  ) => {
    if (!score) return;

    const scoreEvent = findScoreEvent(round, position, participantId);
    if (!scoreEvent) return;

    const responsePanel = document.createElement('div');
    responsePanel.className = 'score-response-panel';

    const responseHeading = document.createElement('div');
    responseHeading.className = 'score-response-heading';
    responseHeading.textContent = 'RESPOND TO THIS SCORE';

    const responseButtons = document.createElement('div');
    responseButtons.className = 'score-response-buttons';

    const reactions = eventReactions(round, scoreEvent.id);
    const viewerId = String(round.viewer_participant_id || '');
    const viewerReaction = reactions.find(
      (reaction) => String(reaction.actor_participant_id) === viewerId
    );

    [
      ['bullshit', 'BULLSHIT'],
      ['cheater', 'CHEATER'],
      ['lucky', 'LUCKY'],
      ['nice', 'NICE'],
      ['talk_shit', 'TALK SHIT'],
    ].forEach(([kind, labelText]) => {
      const button = document.createElement('button');
      button.type = 'button';
      const count = reactions.filter(
        (reaction) => reaction.reaction_kind === kind
      ).length;
      button.textContent = count ? `${labelText} · ${count}` : labelText;
      if (viewerReaction?.reaction_kind === kind) {
        button.classList.add('is-active');
        button.setAttribute('aria-pressed', 'true');
      } else {
        button.setAttribute('aria-pressed', 'false');
      }

      button.addEventListener('click', async () => {
        button.disabled = true;
        setRoundFlowMessage('');
        try {
          const active = viewerReaction?.reaction_kind === kind;
          await requestJson(
            `/api/rounds/${round.id}/events/${scoreEvent.id}/reaction`,
            active
              ? { method: 'DELETE' }
              : {
                  method: 'PUT',
                  body: { reaction: kind },
                }
          );
          await refreshRound(round.active_code);
        } catch (error) {
          setRoundFlowMessage(error.message);
          button.disabled = false;
        }
      });
      responseButtons.append(button);
    });

    responsePanel.append(responseHeading, responseButtons);

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
      responsePanel.append(blameWrap);
    }

    const canChallenge = (
      String(scoreEvent.actor_participant_id || '') !== viewerId
    );
    if (canChallenge) {
      const existingChallenge = activeScoreChallenges(
        round,
        scoreEvent.id
      ).find(
        (challenge) =>
          String(challenge.challenger_participant_id) === viewerId
      );

      const challengeWrap = document.createElement('div');
      challengeWrap.className = 'score-challenge-controls';

      const proposed = document.createElement('input');
      proposed.type = 'number';
      proposed.min = '1';
      proposed.max = '99';
      proposed.inputMode = 'numeric';
      proposed.placeholder = 'CORRECT SCORE?';
      proposed.value = existingChallenge?.proposed_score
        ? String(existingChallenge.proposed_score)
        : '';

      const comment = document.createElement('input');
      comment.type = 'text';
      comment.maxLength = 280;
      comment.placeholder = 'Why is this bullshit?';
      comment.value = existingChallenge?.comment || '';

      const challengeButton = document.createElement('button');
      challengeButton.type = 'button';
      challengeButton.textContent = existingChallenge
        ? 'UPDATE CHALLENGE'
        : 'CHALLENGE SCORE';
      challengeButton.addEventListener('click', async () => {
        const proposedValue = proposed.value.trim();
        const commentValue = comment.value.trim();
        if (!proposedValue && !commentValue) {
          setRoundFlowMessage('Give a corrected score or say why you are challenging it.');
          return;
        }
        challengeButton.disabled = true;
        try {
          await requestJson(
            `/api/rounds/${round.id}/score-events/${scoreEvent.id}/challenge`,
            {
              method: 'PUT',
              body: {
                proposed_score: proposedValue || null,
                comment: commentValue || null,
              },
            }
          );
          await refreshRound(round.active_code);
        } catch (error) {
          setRoundFlowMessage(error.message);
          challengeButton.disabled = false;
        }
      });

      challengeWrap.append(proposed, comment, challengeButton);

      if (existingChallenge) {
        const withdraw = document.createElement('button');
        withdraw.type = 'button';
        withdraw.textContent = 'WITHDRAW';
        withdraw.className = 'score-challenge-withdraw';
        withdraw.addEventListener('click', async () => {
          withdraw.disabled = true;
          try {
            await requestJson(
              `/api/rounds/${round.id}/score-events/${scoreEvent.id}/challenge`,
              { method: 'DELETE' }
            );
            await refreshRound(round.active_code);
          } catch (error) {
            setRoundFlowMessage(error.message);
            withdraw.disabled = false;
          }
        });
        challengeWrap.append(withdraw);
      }

      const activeChallenges = activeScoreChallenges(round, scoreEvent.id);
      if (activeChallenges.length) {
        const summary = document.createElement('small');
        summary.className = 'score-challenge-summary';
        summary.textContent =
          `${activeChallenges.length} ACTIVE CHALLENGE${activeChallenges.length === 1 ? '' : 'S'}`;
        challengeWrap.append(summary);
      }

      responsePanel.append(challengeWrap);
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
  };

  const renderScoreCard = (round, position) => {
    if (!liveScoreArea) return;
    liveScoreArea.replaceChildren();

    const route = routeEntry(round, position);
    const hole = Number(route?.hole_number || position);
    const par = findPar(round, position);
    const canScore = (
      viewerIsActivePlayer(round)
      && Number(position) <= Number(round.current_route_position)
    );

    const addCard = (label, participantId = null, detail = '') => {
      const score = findScore(round, position, participantId);
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

      const target = participantId
        ? (round.participants || []).find(
            (participant) => String(participant.id) === String(participantId)
          )
        : null;
      const targetCanReceiveScore = (
        round.mode === 'scramble'
        || target?.participation_state === 'active'
        || Number(position) < Number(round.current_route_position)
      );

      if (!canScore || !targetCanReceiveScore) {
        const readonly = document.createElement('div');
        readonly.className = 'live-score-readonly';
        readonly.textContent = score
          ? `${score.strokes} STROKES`
          : 'NO SCORE YET';
        card.append(readonly);
        appendScoreResponsePanel(
          card,
          round,
          position,
          participantId,
          score
        );
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
            `/api/rounds/${round.id}/positions/${position}/score`,
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
        const remove = document.createElement('button');
        remove.type = 'button';
        remove.className = 'live-score-remove';
        remove.textContent = 'REMOVE SCORE';
        remove.addEventListener('click', async () => {
          if (!currentLobbyRound) return;

          remove.disabled = true;
          setRoundFlowMessage('');
          try {
            const body = {};
            if (round.mode === 'individual') {
              body.player_participant_id = participantId;
            }

            await requestJson(
              `/api/rounds/${round.id}/positions/${position}/score`,
              {
                method: 'DELETE',
                body,
              }
            );
            await refreshRound(round.active_code);
          } catch (error) {
            setRoundFlowMessage(error.message);
            remove.disabled = false;
          }
        });
        card.append(remove);
      }

      appendScoreResponsePanel(
        card,
        round,
        position,
        participantId,
        score
      );

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

  const renderScrambleContributions = (round, position) => {
    if (!scrambleContributionPanel || !scrambleContributionList) return;

    const route = routeEntry(round, position);
    const hole = Number(route?.hole_number || position);

    if (round.mode !== 'scramble') {
      scrambleContributionPanel.hidden = true;
      scrambleContributionList.replaceChildren();
      return;
    }

    const teamScore = findScore(round, position);
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
    const canEdit = (
      round.status === 'active'
      && viewerIsActivePlayer(round)
    );

    SCRAMBLE_SHOT_TYPES.forEach(([shotType, labelText]) => {
      const contribution = (round.contributions || []).find(
        (row) =>
          Number(row.route_position) === Number(position)
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
            `/api/rounds/${round.id}/positions/${position}/contributions/${shotType}`,
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
      if (event.event_type === 'score_removed') {
        const actor = (round.participants || []).find(
          (participant) =>
            String(participant.id) === String(event.actor_participant_id)
        );
        const subject = event.data?.scope === 'team'
          ? 'TEAM SCORE'
          : String(event.data?.subject || 'GOLFER').toUpperCase();
        const oldScore = Number(event.old_value);
        title.textContent = event.data?.scope === 'team'
          ? `${String(actor?.display_name || 'SOMEONE').toUpperCase()} REMOVED ${subject} ${oldScore}`
          : `${String(actor?.display_name || 'SOMEONE').toUpperCase()} REMOVED ${subject}'S ${oldScore}`;
      } else {
        title.textContent = (
          presentationText(event)
          || event.content_event_key
          || event.event_type
          || 'Round event'
        );
      }

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
    viewedRoutePosition = null;
    finishIncompletePending = false;

    if (startRoundForm) startRoundForm.hidden = true;
    if (joinRoundForm) joinRoundForm.hidden = true;
    if (lobbyPanel) lobbyPanel.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = true;
    if (roundEndPanel) roundEndPanel.hidden = false;
    if (roundFlowTitle) {
      roundFlowTitle.textContent = round.results?.complete ? 'ROUND COMPLETE' : 'ROUND ENDED';
    }

    if (lobbyRefreshTimer) {
      window.clearInterval(lobbyRefreshTimer);
      lobbyRefreshTimer = null;
    }

    const place = round.course?.name || round.free_play_name || 'Golf';
    const resultsComplete = Boolean(round.results?.complete);
    if (roundEndTitle) {
      roundEndTitle.textContent = resultsComplete
        ? 'THE DAMAGE IS FINAL.'
        : 'INCOMPLETE SCORECARD.';
    }
    if (roundEndResults) roundEndResults.replaceChildren();

    const totalPar = totalParForRound(round);

    if (round.mode === 'scramble') {
      const total = round.results?.team_total;
      const scoreCount = Number(round.results?.score_count || 0);
      const requiredScores = Number(round.results?.required_scores || round.hole_count || 0);
      const missingScores = Number(round.results?.missing_scores || 0);
      const relative = resultsComplete && totalPar && total
        ? scoreRelativeLabel(Number(total), Number(totalPar))
        : '';

      if (roundEndSummary) {
        roundEndSummary.textContent = resultsComplete
          ? [
              place,
              total ? `${total} STROKES` : '',
              relative ? `${relative} TO PAR` : '',
            ].filter(Boolean).join(' • ')
          : `${place} • ${scoreCount} OF ${requiredScores} TEAM SCORES RECORDED`;
      }

      const event = resultsComplete
        ? (round.events || []).find(
            (item) =>
              item.event_type === 'round_end_result'
              && item.content_event_key === 'round.end.scramble.complete'
          )
        : null;

      const card = document.createElement('section');
      card.className = 'round-end-result-card';
      if (resultsComplete) card.classList.add('is-first');

      const rank = document.createElement('div');
      rank.className = 'round-end-result-rank';
      rank.textContent = resultsComplete ? '✓' : 'INC';

      const main = document.createElement('div');
      main.className = 'round-end-result-main';

      const name = document.createElement('strong');
      name.textContent = resultsComplete ? 'WE SUCK TOGETHER' : 'INCOMPLETE ROUND';

      const score = document.createElement('small');
      score.textContent = resultsComplete
        ? (total ? `${total} TOTAL STROKES` : 'ROUND COMPLETE')
        : `${missingScores} TEAM SCORE${missingScores === 1 ? '' : 'S'} MISSING`;

      main.append(name, score);
      card.append(rank, main);
      if (resultsComplete) appendResultPresentation(card, event);
      roundEndResults?.append(card);
    } else {
      if (roundEndSummary) {
        const missing = Number(round.results?.missing_scores || 0);
        roundEndSummary.textContent = resultsComplete || missing === 0
          ? place
          : `${place} • ${missing} REQUIRED SCORE${missing === 1 ? '' : 'S'} MISSING`;
      }

      const players = [...(round.results?.players || [])].sort(
        (a, b) =>
          Number(a.rank || 999) - Number(b.rank || 999)
          || Number(a.total_strokes || 9999) - Number(b.total_strokes || 9999)
      );

      players.forEach((result) => {
        const coverage = String(result.coverage_state || (
          Number(result.missing_scores || 0) > 0 ? 'incomplete' : 'complete'
        ));
        const participation = String(result.participation_state || 'active');
        const official = (
          participation === 'active'
          && coverage === 'complete'
          && result.rank !== null
          && result.rank !== undefined
        );

        const card = document.createElement('section');
        card.className = 'round-end-result-card';
        if (official && Number(result.rank) === 1) card.classList.add('is-first');

        const rank = document.createElement('div');
        rank.className = 'round-end-result-rank';
        if (participation !== 'active') {
          rank.textContent = 'DNF';
        } else if (coverage === 'incomplete') {
          rank.textContent = 'INC';
        } else if (coverage === 'partial' || !official) {
          rank.textContent = 'PART';
        } else {
          const tied = Number(result.tie_count) > 1;
          rank.textContent = tied ? `T${result.rank}` : `#${result.rank}`;
        }

        const main = document.createElement('div');
        main.className = 'round-end-result-main';

        const name = document.createElement('strong');
        name.textContent = result.display_name || 'Golfer';

        const score = document.createElement('small');
        if (!official) {
          const scoreCount = Number(result.score_count || 0);
          const required = Number(result.required_scores || 0);
          if (participation !== 'active') {
            score.textContent = `DNF • ${scoreCount} SCORES RECORDED`;
          } else if (coverage === 'incomplete') {
            score.textContent = `INCOMPLETE • ${scoreCount} OF ${required} SCORES`;
          } else {
            score.textContent = `PARTIAL • ${scoreCount} SCORES RECORDED`;
          }
        } else {
          const relative = totalPar && result.total_strokes
            ? scoreRelativeLabel(
                Number(result.total_strokes),
                Number(totalPar)
              )
            : '';
          score.textContent = [
            `${result.total_strokes} STROKES`,
            relative ? `${relative} TO PAR` : '',
          ].filter(Boolean).join(' • ');
        }

        main.append(name, score);
        card.append(rank, main);
        if (official) {
          appendResultPresentation(
            card,
            roundEndEventForPlayer(round, result.participant_id)
          );
        }
        roundEndResults?.append(card);
      });
    }

    renderReceipts(round);
    setRoundFlowMessage('');
  };

  const renderLiveRound = (round) => {
    const previousRound = currentLobbyRound;
    const previousLivePosition = Number(
      previousRound?.current_route_position
      || previousRound?.current_hole
      || 1
    );
    const livePosition = Number(
      round.current_route_position
      || round.current_hole
      || 1
    );
    const length = routeLength(round);
    const wasFollowingLive = (
      viewedRoutePosition === null
      || !previousRound
      || Number(viewedRoutePosition) === previousLivePosition
    );

    currentLobbyRound = round;

    if (wasFollowingLive) {
      viewedRoutePosition = livePosition;
    } else {
      viewedRoutePosition = Math.max(
        1,
        Math.min(Number(viewedRoutePosition), length)
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

    const viewedRoute = routeEntry(round, viewedRoutePosition);
    const viewedPhysicalHole = Number(
      viewedRoute?.hole_number || viewedRoutePosition
    );
    const liveRoute = routeEntry(round, livePosition);
    const livePhysicalHole = Number(
      liveRoute?.hole_number || round.current_hole || livePosition
    );
    const par = findPar(round, viewedRoutePosition);
    const viewingLive = Number(viewedRoutePosition) === livePosition;
    const viewingPast = Number(viewedRoutePosition) < livePosition;
    const viewingFuture = Number(viewedRoutePosition) > livePosition;

    if (holeNumber) holeNumber.textContent = String(viewedPhysicalHole);
    if (holeParLabel) {
      holeParLabel.textContent = par ? `PAR ${par}` : 'PAR ?';
    }
    if (holeStateLabel) {
      if (viewingLive) {
        holeStateLabel.textContent =
          `LIVE HOLE • ${viewedRoutePosition} OF ${length}`;
      } else if (viewingPast) {
        holeStateLabel.textContent =
          `VIEWING HOLE ${viewedPhysicalHole} • ${viewedRoutePosition} OF ${length} • LIVE ${livePhysicalHole}`;
      } else {
        holeStateLabel.textContent =
          `PREVIEWING HOLE ${viewedPhysicalHole} • ${viewedRoutePosition} OF ${length} • LIVE ${livePhysicalHole}`;
      }
    }

    if (holePrev) {
      holePrev.disabled = Number(viewedRoutePosition) <= 1;
    }
    if (holeNext) {
      holeNext.disabled = Number(viewedRoutePosition) >= length;
    }
    if (backToLive) {
      backToLive.hidden = viewingLive;
    }
    if (advanceLiveHole) {
      const canAdvanceLive = (
        viewerIsActivePlayer(round)
        && round.status === 'active'
        && viewingLive
        && livePosition < length
      );
      advanceLiveHole.hidden = !canAdvanceLive;
      advanceLiveHole.disabled = false;
    }

    const canEditViewedHole = (
      viewerIsActivePlayer(round)
      && !viewingFuture
      && round.status === 'active'
    );
    if (parForm) {
      parForm.hidden = !Boolean(round.par_tracking_enabled);
    }
    if (parInput) {
      parInput.value = par ? String(par) : '';
      parInput.disabled = !canEditViewedHole;
    }
    if (parSubmit) {
      parSubmit.textContent = par ? 'PUSH PAR' : 'REPORT PAR';
      parSubmit.disabled = !canEditViewedHole;
    }

    renderScoreCard(round, viewedRoutePosition);
    renderScrambleContributions(round, viewedRoutePosition);
    renderLatestPresentation(round);
    renderReceipts(round);

    const viewer = viewerParticipant(round);
    const viewerWithdrew = (
      round.viewer_role === 'player'
      && viewer?.participation_state === 'withdrew'
    );
    const canToggleTowel = (
      round.viewer_role === 'player'
      && ['active', 'withdrew'].includes(viewer?.participation_state)
    );
    if (towelButton) {
      towelButton.hidden = !canToggleTowel;
      towelButton.textContent = viewerWithdrew
        ? 'GET BACK IN THIS MESS'
        : 'THROW IN THE TOWEL';
      towelButton.disabled = false;
    }
    if (towelPanel && viewerWithdrew) {
      towelPanel.hidden = true;
    }

    const canFinish = (
      viewerIsActivePlayer(round)
      && viewingLive
      && livePosition === length
    );
    const resultsComplete = Boolean(round.results?.complete);
    if (!canFinish || resultsComplete) {
      finishIncompletePending = false;
    }
    if (finishRoundButton) {
      finishRoundButton.hidden = !canFinish || finishIncompletePending;
      finishRoundButton.disabled = false;
    }
    if (finishIncompletePanel) {
      finishIncompletePanel.hidden = !(
        canFinish
        && finishIncompletePending
        && !resultsComplete
      );
    }
    if (finishIncompleteCopy) {
      const missing = Number(round.results?.missing_scores || 0);
      const noun = round.mode === 'scramble' ? 'TEAM SCORE' : 'REQUIRED SCORE';
      finishIncompleteCopy.textContent =
        `${missing} ${noun}${missing === 1 ? '' : 'S'} `
        + 'ARE STILL MISSING. FINISHING NOW MARKS THE SCORECARD INCOMPLETE. '
        + 'NOTHING GETS INVENTED.';
    }

    if (round.status === 'active') {
      setRoundFlowMessage(
        viewingFuture ? 'Future holes are preview-only.' : ''
      );
    }
  };

  const renderLobby = (round) => {
    currentLobbyRound = round;
    viewedRoutePosition = null;
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

  const changeParticipation = async (state, reason = '') => {
    if (!currentLobbyRound) return;
    setRoundFlowMessage('');
    if (towelButton) towelButton.disabled = true;
    if (towelConfirm) towelConfirm.disabled = true;
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/participation`,
        {
          method: 'PATCH',
          body: {
            state,
            reason: reason || null,
          },
        }
      );
      if (towelPanel) towelPanel.hidden = true;
      if (towelReason) towelReason.value = '';
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      if (towelButton) towelButton.disabled = false;
      if (towelConfirm) towelConfirm.disabled = false;
    }
  };

  towelButton?.addEventListener('click', async () => {
    if (!currentLobbyRound) return;
    const viewer = viewerParticipant(currentLobbyRound);
    if (viewer?.participation_state === 'withdrew') {
      await changeParticipation('active');
      return;
    }
    if (towelPanel) towelPanel.hidden = false;
    towelReason?.focus();
  });

  towelCancel?.addEventListener('click', () => {
    if (towelPanel) towelPanel.hidden = true;
    if (towelReason) towelReason.value = '';
  });

  towelConfirm?.addEventListener('click', async () => {
    await changeParticipation('withdrew', towelReason?.value.trim() || '');
  });

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

  const completeRound = async (finishIncomplete = false) => {
    if (!currentLobbyRound || currentLobbyRound.viewer_role !== 'player') return;

    if (finishRoundButton) finishRoundButton.disabled = true;
    if (finishIncompleteButton) finishIncompleteButton.disabled = true;
    setRoundFlowMessage('');

    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/status`,
        {
          method: 'PATCH',
          body: {
            status: 'completed',
            finish_incomplete: Boolean(finishIncomplete),
          },
        }
      );
      finishIncompletePending = false;
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      if (finishRoundButton) finishRoundButton.disabled = false;
      if (finishIncompleteButton) finishIncompleteButton.disabled = false;
    }
  };

  finishRoundButton?.addEventListener('click', async () => {
    if (!currentLobbyRound || currentLobbyRound.viewer_role !== 'player') return;

    if (!currentLobbyRound.results?.complete) {
      finishIncompletePending = true;
      renderLiveRound(currentLobbyRound);
      return;
    }

    await completeRound(false);
  });

  fixScorecardButton?.addEventListener('click', () => {
    finishIncompletePending = false;
    if (finishIncompletePanel) finishIncompletePanel.hidden = true;
    if (finishRoundButton) finishRoundButton.hidden = false;
    setRoundFlowMessage('Use the hole arrows to fix the missing scores, then come back here.');
  });

  finishIncompleteButton?.addEventListener('click', async () => {
    await completeRound(true);
  });

  holePrev?.addEventListener('click', () => {
    if (!currentLobbyRound || viewedRoutePosition === null) return;
    if (Number(viewedRoutePosition) <= 1) return;
    viewedRoutePosition = Number(viewedRoutePosition) - 1;
    renderLiveRound(currentLobbyRound);
  });

  backToLive?.addEventListener('click', () => {
    if (!currentLobbyRound) return;
    viewedRoutePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    renderLiveRound(currentLobbyRound);
  });

  holeNext?.addEventListener('click', () => {
    if (!currentLobbyRound || viewedRoutePosition === null) return;
    const length = routeLength(currentLobbyRound);
    const viewed = Number(viewedRoutePosition);
    if (viewed >= length) return;

    viewedRoutePosition = viewed + 1;
    renderLiveRound(currentLobbyRound);
  });

  advanceLiveHole?.addEventListener('click', async () => {
    if (!currentLobbyRound || currentLobbyRound.viewer_role !== 'player') return;

    const length = routeLength(currentLobbyRound);
    const livePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    if (livePosition >= length) return;

    advanceLiveHole.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/current-hole`,
        {
          method: 'PATCH',
          body: { route_position: livePosition + 1 },
        }
      );
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      advanceLiveHole.disabled = false;
    }
  });

  parForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!currentLobbyRound || viewedRoutePosition === null) return;
    if (currentLobbyRound.viewer_role !== 'player') return;

    const livePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    if (Number(viewedRoutePosition) > livePosition) {
      setRoundFlowMessage('Future holes are preview-only.');
      return;
    }

    const par = Number(parInput?.value);
    if (!Number.isInteger(par) || par < 2 || par > 7) {
      setRoundFlowMessage('Par must be between 2 and 7.');
      return;
    }

    if (parSubmit) parSubmit.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/positions/${viewedRoutePosition}/par`,
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
