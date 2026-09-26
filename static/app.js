(() => {
  const SESSION_KEY = 'wpm_session_token';
  const PAR_SETUP_NOW_KEY = 'wpm_par_setup_now_round';
  const HOME_HERO_SESSION_KEY = 'wpm_home_hero_asset';

  const splash = document.getElementById('launch-splash');
  const splashMini = document.getElementById('launch-splash-mini');
  const authShell = document.getElementById('auth-shell');
  const appShell = document.getElementById('app-shell');
  const homeHeroArt = document.getElementById('home-hero-art');
  const authMessage = document.getElementById('auth-message');
  const authHeckle = document.getElementById('auth-heckle');
  const authHeckleText = document.getElementById('auth-heckle-text');
  const authTabs = document.querySelector('.auth-tabs');
  const authViewButtons = document.querySelectorAll('[data-auth-view]');
  const authPanels = document.querySelectorAll('[data-auth-panel]');
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const recoverForm = document.getElementById('recover-form');
  const recoveryCard = document.getElementById('recovery-key-card');
  const recoveryKeyValue = document.getElementById('recovery-key-value');
  const recoveryKeyStatus = document.getElementById('recovery-key-status');
  const recoveryKeyInstruction = document.getElementById('recovery-key-instruction');
  const recoveryKeySnark = document.getElementById('recovery-key-snark');
  const recoveryKeyCopy = document.getElementById('copy-recovery-key');
  const recoveryKeyContinue = document.getElementById('recovery-key-continue');
  const logoutButton = document.getElementById('logout-button');
  const welcomeName = document.getElementById('home-welcome-name');
  const homeHeckle = document.getElementById('home-heckle');
  const homeHeckleText = document.getElementById('home-heckle-text');
  const settingsOpenButtons = document.querySelectorAll('[data-settings-open]');
  const settingsModal = document.getElementById('settings-modal');
  const settingsClose = document.getElementById('settings-close');
  const settingsForm = document.getElementById('settings-form');
  const settingsMessage = document.getElementById('settings-message');
  const settingsHandicapIndex = document.getElementById('settings-handicap-index');
  const colorThemeTease = document.getElementById('color-theme-tease');
  const installOnboardingModal = document.getElementById('install-onboarding-modal');
  const installOnboardingMascot = document.getElementById('install-onboarding-mascot');
  const installOnboardingInstructions = document.getElementById('install-onboarding-instructions');
  const installOnboardingHeckle = document.getElementById('install-onboarding-heckle');
  const installOnboardingPrimary = document.getElementById('install-onboarding-primary');
  const installOnboardingSkip = document.getElementById('install-onboarding-skip');
  const startRoundButton = document.getElementById('start-round-button');
  const joinRoundButton = document.getElementById('join-round-button');
  const roundFlowModal = document.getElementById('round-flow-modal');
  const roundFlowCardGame = roundFlowModal?.querySelector('.round-flow-card-game');
  const roundFlowClose = document.getElementById('round-flow-close');
  const roundFlowTitle = document.getElementById('round-flow-title');
  const roundFlowMessage = document.getElementById('round-flow-message');
  const roundSetupHeckle = document.getElementById('round-setup-heckle');
  const roundSetupHeckleText = document.getElementById('round-setup-heckle-text');
  const startRoundForm = document.getElementById('start-round-form');
  const setupMiniStages = document.querySelectorAll('[data-setup-mini-stage]');
  const setupMinis = document.querySelectorAll('[data-setup-mini]');
  const setupSteps = document.querySelectorAll('[data-setup-step]');
  const setupStepDots = document.querySelectorAll('[data-setup-step-dot]');
  const setupNextButtons = document.querySelectorAll('[data-setup-next]');
  const setupBackButtons = document.querySelectorAll('[data-setup-back]');
  const courseStepMessage = document.getElementById('course-step-message');
  const roundHolesHint = document.getElementById('round-holes-hint');
  const individualScoringFieldset = document.getElementById('individual-scoring-fieldset');
  const joinRoundForm = document.getElementById('join-round-form');
  const joinRoundSubmit = document.getElementById('join-round-submit');
  const joinTeeField = document.getElementById('join-tee-field');
  const joinTeeSelect = document.getElementById('join-tee-select');
  const claimPlayerPanel = document.getElementById('claim-player-panel');
  const claimPlayerList = document.getElementById('claim-player-list');
  const claimPlayerNone = document.getElementById('claim-player-none');
  const lobbyPanel = document.getElementById('lobby-panel');
  const lobbyCode = document.getElementById('lobby-code');
  const lobbySummary = document.getElementById('lobby-summary');
  const lobbyParticipants = document.getElementById('lobby-participants');
  const lobbyBanterFeed = document.getElementById('lobby-banter-feed');
  const lobbyBanterForm = document.getElementById('lobby-banter-form');
  const lobbyBanterInput = document.getElementById('lobby-banter-input');
  const lobbyBanterSend = document.getElementById('lobby-banter-send');
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
  const startTeeLabel = document.getElementById('start-tee-label');
  const startTeeSelect = document.getElementById('start-tee-select');
  const startHoleInput = document.getElementById('start-hole-input');
  const trackingStartPosition = document.getElementById('tracking-start-position');
  const priorHolesMode = document.getElementById('prior-holes-mode');
  const routePreview = document.getElementById('route-preview');
  const lobbyTeePanel = document.getElementById('lobby-tee-panel');
  const lobbyTeeLabel = document.getElementById('lobby-tee-label');
  const lobbyTeeSelect = document.getElementById('lobby-tee-select');
  const lobbyTeeSave = document.getElementById('lobby-tee-save');
  const lobbyParSetup = document.getElementById('lobby-par-setup');
  const lobbyParGrid = document.getElementById('lobby-par-grid');
  const lobbyParSave = document.getElementById('lobby-par-save');
  const lobbyHandicapPanel = document.getElementById('lobby-handicap-panel');
  const lobbyHandicapList = document.getElementById('lobby-handicap-list');
  const liveRoundPanel = document.getElementById('live-round-panel');
  const liveRoundPlace = document.getElementById('live-round-place');
  const spectatorJoinPlayPanel = document.getElementById('spectator-join-play-panel');
  const spectatorJoinTeeField = document.getElementById('spectator-join-tee-field');
  const spectatorJoinTeeSelect = document.getElementById('spectator-join-tee-select');
  const spectatorJoinPlayButton = document.getElementById('spectator-join-play-button');
  const lateBackfillPanel = document.getElementById('late-backfill-panel');
  const lateBackfillStart = document.getElementById('late-backfill-start');
  const lateBackfillGo = document.getElementById('late-backfill-go');
  const lateBackfillDismiss = document.getElementById('late-backfill-dismiss');
  const liveRoundCode = document.getElementById('live-round-code');
  const holePrev = document.getElementById('hole-prev');
  const holeNext = document.getElementById('hole-next');
  const advanceLiveHole = document.getElementById('advance-live-hole');
  const advanceWarningPanel = document.getElementById('advance-warning-panel');
  const advanceWarningCopy = document.getElementById('advance-warning-copy');
  const advanceWarningFix = document.getElementById('advance-warning-fix');
  const advanceWarningGo = document.getElementById('advance-warning-go');
  const roundSettingsButton = document.getElementById('round-settings-button');
  const roundSettingsPanel = document.getElementById('round-settings-panel');
  const roundSettingsTeeField = document.getElementById('round-settings-tee-field');
  const roundSettingsTeeLabel = document.getElementById('round-settings-tee-label');
  const roundSettingsTeeSelect = document.getElementById('round-settings-tee-select');
  const roundSettingsTeeSave = document.getElementById('round-settings-tee-save');
  const roundParTrackingPanel = document.getElementById('round-par-tracking-panel');
  const roundParTrackingCopy = document.getElementById('round-par-tracking-copy');
  const roundParTrackingOn = document.getElementById('round-par-tracking-on');
  const roundParTrackingOff = document.getElementById('round-par-tracking-off');
  const roundHandicapPanel = document.getElementById('round-handicap-panel');
  const roundHandicapList = document.getElementById('round-handicap-list');
  const offlinePlayerPanel = document.getElementById('offline-player-panel');
  const offlinePlayerName = document.getElementById('offline-player-name');
  const offlinePlayerTeeField = document.getElementById('offline-player-tee-field');
  const offlinePlayerTeeSelect = document.getElementById('offline-player-tee-select');
  const offlinePlayerAdd = document.getElementById('offline-player-add');
  const claimUndoPanel = document.getElementById('claim-undo-panel');
  const claimUndoCopy = document.getElementById('claim-undo-copy');
  const claimUndoButton = document.getElementById('claim-undo-button');
  const roundSettingsClose = document.getElementById('round-settings-close');
  const backToLive = document.getElementById('back-to-live');
  const holeStateLabel = document.getElementById('hole-state-label');
  const holeNumber = document.getElementById('hole-number');
  const holeParLabel = document.getElementById('hole-par-label');
  const parForm = document.getElementById('par-form');
  const parInput = document.getElementById('par-input');
  const parSubmit = document.getElementById('par-submit');
  const liveEditPar = document.getElementById('live-edit-par');
  const liveScoreArea = document.getElementById('live-score-area');
  const liveHoleSelector = document.getElementById('live-hole-selector');
  const liveBanterFeed = document.getElementById('live-banter-feed');
  const liveBanterForm = document.getElementById('live-banter-form');
  const liveBanterInput = document.getElementById('live-banter-input');
  const liveBanterSend = document.getElementById('live-banter-send');
  const liveHoleStats = document.getElementById('live-hole-stats');
  const liveMorePanel = document.getElementById('live-more-panel');
  const liveNavPlay = document.getElementById('live-nav-play');
  const liveNavScorecard = document.getElementById('live-nav-scorecard');
  const liveNavStats = document.getElementById('live-nav-stats');
  const liveNavMore = document.getElementById('live-nav-more');
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
  const receiptsUnseenBadge = document.getElementById('receipts-unseen-badge');
  const receiptsList = document.getElementById('receipts-list');
  const bagButton = document.getElementById('bag-of-bullshit-button');
  const towelButton = document.getElementById('towel-button');
  const towelPanel = document.getElementById('towel-panel');
  const towelReason = document.getElementById('towel-reason');
  const towelConfirm = document.getElementById('towel-confirm');
  const towelCancel = document.getElementById('towel-cancel');
  const endEarlyButton = document.getElementById('end-early-button');
  const endEarlyPanel = document.getElementById('end-early-panel');
  const endEarlyCopy = document.getElementById('end-early-copy');
  const endEarlyVoters = document.getElementById('end-early-voters');
  const endEarlyYes = document.getElementById('end-early-yes');
  const endEarlyNo = document.getElementById('end-early-no');
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
  let advanceWarningPosition = null;
  let pendingScoreAfterPar = null;
  let parEditorOpen = false;
  let pendingClaimJoin = null;
  let pendingJoinPreview = null;
  let lobbyBanterTimer = null;
  let lobbyBanterRoundId = '';
  let lobbyIdleRows = [];
  let lobbyIdleLastId = '';
  let lobbyIdleMessages = [];
  let claimUndoConfirmPending = false;
  let receiptMarkInFlight = false;
  let deferredInstallPrompt = null;
  let installOnboardingAccountKey = '';
  let currentAuthView = 'login';
  let authHeckleRows = [];
  let authHeckleBag = [];
  let authHeckleLastId = '';
  let authHeckleInterval = null;
  let authHeckleResumeTimer = null;
  let authHeckleFadeTimer = null;
  let authHeckleLoadPromise = null;
  let authHeckleEventKey = '';
  const authMessageCache = new Map();
  const userMessageCache = new Map();
  const userHeckleTimers = new Map();
  const userHeckleLastIds = new Map();

  const AUTH_HECKLE_ROTATE_MS = 5000;
  const AUTH_HECKLE_RESUME_MS = 9000;
  const USER_HECKLE_ROTATE_MS = 7000;
  const LOBBY_BANTER_ROTATE_MS = 8000;

  const AUTH_IDLE_EVENTS = {
    login: 'auth.signin.idle',
    register: 'auth.create_account.idle',
    recover: 'auth.recover.idle',
  };

  const INSTALL_ONBOARDING_ASSETS = [
    '/static/assets/mascots/onboarding/install/WPM_Onboarding_Install_StopOpeningThisLikeAPsychopath.webp',
    '/static/assets/mascots/onboarding/install/WPM_Onboarding_Install_LiterallyTellingYouWhereToTap.webp',
    '/static/assets/mascots/onboarding/install/WPM_Onboarding_Install_PutMeOnYourFuckingHomeScreen.webp',
    '/static/assets/mascots/onboarding/install/WPM_Onboarding_Install_MakeItAnAppYouLazyBastard.webp',
    '/static/assets/mascots/onboarding/install/WPM_Onboarding_Install_47OtherUselessApps.webp',
  ];

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

  const formBusyState = new WeakMap();

  const setFormBusy = (form, busy) => {
    if (!form) return;
    const controls = [...form.querySelectorAll('button, input, select')];

    if (busy) {
      if (!formBusyState.has(form)) {
        formBusyState.set(
          form,
          new Map(controls.map((control) => [control, control.disabled]))
        );
      }
      controls.forEach((control) => {
        control.disabled = true;
      });
      return;
    }

    const previous = formBusyState.get(form);
    controls.forEach((control) => {
      control.disabled = previous?.get(control) ?? false;
    });
    formBusyState.delete(form);
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

    const vulgarity = String(preferences?.max_vulgarity || 'brutal');
    const radio = settingsForm.querySelector(
      `input[name="max_vulgarity"][value="${vulgarity}"]`
    );
    if (radio) radio.checked = true;
  };

  const populateProfileHandicap = (account) => {
    if (!settingsHandicapIndex) return;
    settingsHandicapIndex.value = (
      account?.handicap_index !== null
      && account?.handicap_index !== undefined
    )
      ? Number(account.handicap_index).toFixed(1)
      : '';
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
      const error = new Error('Could not reach the server.');
      error.kind = 'network';
      throw error;
    }

    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      const error = new Error(payload.error || `Request failed (${response.status})`);
      error.status = response.status;
      throw error;
    }
    return payload;
  };

  const shuffledCopy = (rows) => {
    const shuffled = [...rows];
    for (let index = shuffled.length - 1; index > 0; index -= 1) {
      const swapIndex = Math.floor(Math.random() * (index + 1));
      [shuffled[index], shuffled[swapIndex]] = [
        shuffled[swapIndex],
        shuffled[index],
      ];
    }
    return shuffled;
  };

  const pickMessage = (rows, previousId = '') => {
    if (!rows.length) return null;
    const choices = rows.length > 1
      ? rows.filter((row) => row.id !== previousId)
      : rows;
    return choices[Math.floor(Math.random() * choices.length)] || null;
  };

  const loadMessageBank = async (eventKey, { authenticated = false } = {}) => {
    const cache = authenticated ? userMessageCache : authMessageCache;
    if (cache.has(eventKey)) return cache.get(eventKey);

    const endpoint = authenticated
      ? '/api/content/messages/user'
      : '/api/content/messages';
    const payload = await requestJson(
      `${endpoint}?event=${encodeURIComponent(eventKey)}`,
      { authenticated },
    );
    const rows = (payload.messages || []).filter(
      (row) => row && row.id && row.text
    );
    cache.set(eventKey, rows);
    return rows;
  };

  const refillAuthHeckleBag = () => {
    authHeckleBag = shuffledCopy(authHeckleRows);
    if (
      authHeckleBag.length > 1
      && authHeckleBag[authHeckleBag.length - 1]?.id === authHeckleLastId
    ) {
      [
        authHeckleBag[0],
        authHeckleBag[authHeckleBag.length - 1],
      ] = [
        authHeckleBag[authHeckleBag.length - 1],
        authHeckleBag[0],
      ];
    }
  };

  const nextAuthHeckle = () => {
    if (!authHeckleRows.length) return null;
    if (!authHeckleBag.length) refillAuthHeckleBag();
    const row = authHeckleBag.pop() || null;
    if (row) authHeckleLastId = row.id;
    return row;
  };

  const renderAuthHeckle = (row) => {
    if (!authHeckle || !authHeckleText || !row?.text) return;

    const apply = () => {
      authHeckleText.textContent = row.text;
      authHeckle.hidden = false;
      authHeckle.classList.remove('is-changing');
    };

    if (authHeckle.hidden || !authHeckleText.textContent) {
      apply();
      return;
    }

    authHeckle.classList.add('is-changing');
    if (authHeckleFadeTimer) window.clearTimeout(authHeckleFadeTimer);
    authHeckleFadeTimer = window.setTimeout(apply, 150);
  };

  const stopAuthHeckles = ({ hide = false } = {}) => {
    if (authHeckleInterval) {
      window.clearInterval(authHeckleInterval);
      authHeckleInterval = null;
    }
    if (authHeckleResumeTimer) {
      window.clearTimeout(authHeckleResumeTimer);
      authHeckleResumeTimer = null;
    }
    if (hide && authHeckle) authHeckle.hidden = true;
  };

  const currentAuthIdleEvent = () => (
    AUTH_IDLE_EVENTS[currentAuthView] || 'auth.signin.idle'
  );

  const startAuthHeckles = async ({
    eventKey = currentAuthIdleEvent(),
    advance = true,
  } = {}) => {
    stopAuthHeckles();
    authHeckleEventKey = eventKey;

    try {
      authHeckleRows = await loadMessageBank(eventKey, {
        authenticated: false,
      });
    } catch (_error) {
      if (authHeckle) authHeckle.hidden = true;
      return;
    }

    if (
      authHeckleEventKey !== eventKey
      || !authHeckleRows.length
      || !authShell
      || authShell.hidden
    ) {
      return;
    }

    authHeckleBag = [];
    if (advance) renderAuthHeckle(nextAuthHeckle());
    authHeckleInterval = window.setInterval(() => {
      if (
        authHeckleEventKey === eventKey
        && currentAuthIdleEvent() === eventKey
      ) {
        renderAuthHeckle(nextAuthHeckle());
      }
    }, AUTH_HECKLE_ROTATE_MS);
  };

  const showAuthHeckleOnce = async (eventKey) => {
    stopAuthHeckles();
    authHeckleEventKey = eventKey;
    try {
      const rows = await loadMessageBank(eventKey, { authenticated: false });
      const row = pickMessage(rows, authHeckleLastId);
      if (row) {
        authHeckleLastId = row.id;
        renderAuthHeckle(row);
      }
    } catch (_error) {
      // Plain validation/error copy still tells the user what happened.
    }
  };

  const scheduleAuthHeckleResume = () => {
    const eventKey = currentAuthIdleEvent();
    if (authHeckleResumeTimer) {
      window.clearTimeout(authHeckleResumeTimer);
    }
    authHeckleResumeTimer = window.setTimeout(() => {
      authHeckleResumeTimer = null;
      void startAuthHeckles({ eventKey, advance: true });
    }, AUTH_HECKLE_RESUME_MS);
  };

  const pauseAuthHecklesForInteraction = () => {
    if (authHeckleInterval) {
      window.clearInterval(authHeckleInterval);
      authHeckleInterval = null;
    }
    scheduleAuthHeckleResume();
  };

  const authFailureDetails = (error, fallbackEvent) => {
    const raw = String(error?.message || 'Something went wrong.');
    const lower = raw.toLowerCase();

    if (error?.kind === 'network') {
      return navigator.onLine === false
        ? {
            message: 'NO INTERNET CONNECTION — CHECK YOUR SIGNAL AND TRY AGAIN.',
            event: 'auth.offline',
          }
        : {
            message: 'WE COULDN’T REACH THE SERVER — TRY AGAIN.',
            event: 'auth.system_error',
          };
    }
    if (Number(error?.status) >= 500 || lower.includes('database request failed')) {
      return {
        message: 'OUR SERVER HIT A PROBLEM — TRY AGAIN.',
        event: 'auth.system_error',
      };
    }
    if (lower.includes('username is already taken')) {
      return {
        message: 'USERNAME ALREADY TAKEN — PICK ANOTHER.',
        event: 'auth.username_taken',
      };
    }
    if (lower.includes('username must be 3-16')) {
      return {
        message: 'USERNAME MUST BE 3–16 CHARACTERS USING LETTERS, NUMBERS, ., _, OR -.',
        event: 'auth.username_invalid',
      };
    }
    if (lower.includes('display_name must be between 1 and 20')) {
      return {
        message: 'DISPLAY NAME MUST BE 1–20 CHARACTERS.',
        event: 'auth.display_name_invalid',
      };
    }
    if (lower.includes('password must be between 10 and 128')) {
      return {
        message: 'PASSWORD MUST BE AT LEAST 10 CHARACTERS.',
        event: 'auth.password_invalid',
      };
    }
    if (lower.includes('password cannot be all numbers')) {
      return {
        message: 'PASSWORD CAN’T BE ALL NUMBERS.',
        event: 'auth.password_invalid',
      };
    }
    if (lower.includes('password cannot be a single word')) {
      return {
        message: 'PASSWORD CAN’T BE A SINGLE WORD.',
        event: 'auth.password_invalid',
      };
    }
    if (lower.includes('password is too obvious')) {
      return {
        message: 'THAT PASSWORD IS TOO OBVIOUS.',
        event: 'auth.password_invalid',
      };
    }
    if (lower.includes('recovery key must use the format')) {
      return {
        message: 'RECOVERY KEY MUST LOOK LIKE XXXX-XXXX.',
        event: 'auth.recovery_key_invalid_format',
      };
    }
    if (lower.includes('recovery key not found')) {
      return {
        message: 'THAT RECOVERY KEY DOESN’T MATCH AN ACCOUNT.',
        event: 'auth.recovery_failed',
      };
    }
    if (lower.includes('invalid username or password')) {
      return {
        message: 'USERNAME OR PASSWORD IS INCORRECT.',
        event: 'auth.login_failed',
      };
    }

    return {
      message: raw.toUpperCase(),
      event: fallbackEvent,
    };
  };

  const showAuthFailure = async (error, fallbackEvent) => {
    const details = authFailureDetails(error, fallbackEvent);
    setAuthMessage(details.message);
    await showAuthHeckleOnce(details.event);
  };

  const validateNewPassword = (value) => {
    const password = String(value || '');
    const lowered = password.trim().toLowerCase();
    const compact = lowered.replace(/[^a-z0-9]+/g, '');
    const obvious = new Set([
      'password123',
      'password1234',
      'letmein123',
      'qwerty1234',
      'welcome123',
      'golfgolfgolf',
    ]);
    const sequences = [
      '01234567890123456789',
      '98765432109876543210',
      'abcdefghijklmnopqrstuvwxyz',
      'zyxwvutsrqponmlkjihgfedcba',
      'qwertyuiopasdfghjklzxcvbnm',
    ];

    if (password.length < 10 || password.length > 128) {
      return new Error('password must be between 10 and 128 characters');
    }
    if (/^\d+$/.test(password)) {
      return new Error('password cannot be all numbers');
    }
    if (/^[A-Za-z]+$/.test(password)) {
      return new Error('password cannot be a single word');
    }
    if (
      lowered
      && (
        new Set(lowered).size === 1
        || obvious.has(lowered)
        || obvious.has(compact)
        || sequences.some((source) => source.includes(lowered))
      )
    ) {
      return new Error('password is too obvious');
    }
    return null;
  };

  const validateRegisterValues = (values) => {
    const displayName = String(values.get('display_name') || '').trim();
    const username = String(values.get('username') || '').trim().toLowerCase();
    const password = String(values.get('password') || '');

    if (displayName.length < 1 || displayName.length > 20) {
      return new Error('display_name must be between 1 and 20 characters');
    }
    if (!/^[a-z0-9][a-z0-9_.-]{2,15}$/.test(username)) {
      return new Error(
        'username must be 3-16 characters using letters, numbers, ., _, or -'
      );
    }
    return validateNewPassword(password);
  };

  const validateRecoveryValues = (values) => {
    const key = String(values.get('recovery_key') || '').trim().toUpperCase();
    const current = /^[A-HJ-KM-NP-Z2-9]{4}-[A-HJ-KM-NP-Z2-9]{4}$/;
    const legacy = /^[A-HJ-KM-NP-Z2-9]{4}(?:-[A-HJ-KM-NP-Z2-9]{4}){3}$/;
    if (!current.test(key) && !legacy.test(key)) {
      return new Error('recovery key must use the format XXXX-XXXX');
    }
    return validateNewPassword(values.get('new_password'));
  };

  const stopUserHeckle = (name, { hide = false } = {}) => {
    const timer = userHeckleTimers.get(name);
    if (timer) window.clearInterval(timer);
    userHeckleTimers.delete(name);

    const target = {
      home: homeHeckle,
      roundSetup: roundSetupHeckle,
      install: installOnboardingHeckle,
    }[name];
    if (hide && target) target.hidden = true;
  };

  const userHeckleTarget = (name) => ({
    home: { container: homeHeckle, text: homeHeckleText },
    roundSetup: { container: roundSetupHeckle, text: roundSetupHeckleText },
    install: { container: installOnboardingHeckle, text: installOnboardingHeckle },
  }[name] || {});

  const renderUserHeckle = (name, row) => {
    const { container, text } = userHeckleTarget(name);
    if (!container || !text || !row?.text) return;
    text.textContent = row.text;
    container.hidden = false;
    userHeckleLastIds.set(name, row.id);
  };

  const showUserHeckleOnce = async (name, eventKey) => {
    stopUserHeckle(name);
    try {
      const rows = await loadMessageBank(eventKey, { authenticated: true });
      renderUserHeckle(
        name,
        pickMessage(rows, userHeckleLastIds.get(name) || ''),
      );
    } catch (_error) {
      stopUserHeckle(name, { hide: true });
    }
  };

  const startUserHeckles = async (name, eventKey, active) => {
    stopUserHeckle(name);
    let rows;
    try {
      rows = await loadMessageBank(eventKey, { authenticated: true });
    } catch (_error) {
      if (name === 'roundSetup' && roundSetupHeckle) {
        roundSetupHeckle.hidden = false;
        return;
      }
      stopUserHeckle(name, { hide: true });
      return;
    }
    if (!rows.length || !active()) {
      if (name === 'roundSetup' && roundSetupHeckle && active()) {
        roundSetupHeckle.hidden = false;
        return;
      }
      stopUserHeckle(name, { hide: true });
      return;
    }

    const rotate = () => {
      if (!active()) return;
      renderUserHeckle(
        name,
        pickMessage(rows, userHeckleLastIds.get(name) || ''),
      );
    };
    rotate();
    userHeckleTimers.set(
      name,
      window.setInterval(rotate, USER_HECKLE_ROTATE_MS),
    );
  };

  const switchAuthView = (view) => {
    setAuthMessage('');
    pendingAccount = null;
    currentAuthView = view;
    if (recoveryCard) recoveryCard.hidden = true;
    if (authTabs) authTabs.hidden = false;

    authViewButtons.forEach((button) => {
      button.classList.toggle('is-active', button.dataset.authView === view);
    });
    authPanels.forEach((panel) => {
      panel.hidden = panel.dataset.authPanel !== view;
    });

    void startAuthHeckles({
      eventKey: currentAuthIdleEvent(),
      advance: true,
    });
  };

  const showAuth = (view = 'login') => {
    document.body.classList.remove('app-ready');
    if (appShell) appShell.setAttribute('aria-hidden', 'true');
    if (splash) {
      splash.hidden = false;
      splash.classList.remove('splash-leaving');
      splash.classList.add('splash-auth-ready');
    }
    if (authShell) authShell.hidden = false;
    switchAuthView(view);
  };

  const isStandaloneApp = () => {
    return (
      window.matchMedia('(display-mode: standalone)').matches
      || window.navigator.standalone === true
    );
  };

  const installOnboardingKey = (account) => {
    const identity = String(account?.id || account?.username || 'account');
    return `wpm_install_onboarding_seen:${identity}`;
  };

  const closeInstallOnboarding = ({ remember = true } = {}) => {
    stopUserHeckle('install', { hide: true });
    if (remember && installOnboardingAccountKey) {
      window.localStorage.setItem(installOnboardingAccountKey, '1');
    }
    if (installOnboardingModal) installOnboardingModal.hidden = true;
    document.body.classList.remove('modal-open');
    if (installOnboardingInstructions) {
      installOnboardingInstructions.hidden = true;
      installOnboardingInstructions.textContent = '';
    }
    if (installOnboardingPrimary) {
      installOnboardingPrimary.textContent = 'FINE. INSTALL THE DAMN THING.';
      installOnboardingPrimary.dataset.instructionsShown = '';
    }
    if (sessionToken()) {
      void startUserHeckles(
        'home',
        'home.idle',
        () => (
          Boolean(appShell?.getAttribute('aria-hidden') !== 'true')
          && Boolean(roundFlowModal?.hidden)
          && Boolean(settingsModal?.hidden)
          && Boolean(installOnboardingModal?.hidden)
        ),
      );
    }
  };

  window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    deferredInstallPrompt = event;
  });

  window.addEventListener('appinstalled', () => {
    deferredInstallPrompt = null;
    closeInstallOnboarding({ remember: true });
  });

  installOnboardingPrimary?.addEventListener('click', async () => {
    if (deferredInstallPrompt) {
      const prompt = deferredInstallPrompt;
      deferredInstallPrompt = null;
      await prompt.prompt();
      const choice = await prompt.userChoice.catch(() => null);
      if (choice?.outcome === 'accepted') {
        closeInstallOnboarding({ remember: true });
      }
      return;
    }

    if (installOnboardingPrimary.dataset.instructionsShown === '1') {
      closeInstallOnboarding({ remember: true });
      return;
    }

    const isAppleMobile = /iPad|iPhone|iPod/.test(navigator.userAgent);
    if (installOnboardingInstructions) {
      installOnboardingInstructions.textContent = isAppleMobile
        ? 'Tap the Share button, then choose Add to Home Screen.'
        : 'Open your browser menu and choose Install app or Add to Home screen.';
      installOnboardingInstructions.hidden = false;
    }
    installOnboardingPrimary.dataset.instructionsShown = '1';
    installOnboardingPrimary.textContent = 'FINE. I GET IT.';
  });

  installOnboardingSkip?.addEventListener('click', () => {
    closeInstallOnboarding({ remember: true });
  });

  const maybeShowInstallOnboarding = (account) => {
    if (!installOnboardingModal) return;

    installOnboardingAccountKey = installOnboardingKey(account);
    if (isStandaloneApp()) {
      window.localStorage.setItem(installOnboardingAccountKey, '1');
      return;
    }
    if (window.localStorage.getItem(installOnboardingAccountKey) === '1') {
      return;
    }

    const identity = String(account?.id || account?.username || 'wpm');
    const assetIndex = [...identity].reduce(
      (total, character) => total + character.charCodeAt(0),
      0
    ) % INSTALL_ONBOARDING_ASSETS.length;
    if (installOnboardingMascot) {
      installOnboardingMascot.src = INSTALL_ONBOARDING_ASSETS[assetIndex];
    }

    installOnboardingModal.hidden = false;
    document.body.classList.add('modal-open');
    stopUserHeckle('home');
    void startUserHeckles(
      'install',
      'onboarding.install.idle',
      () => Boolean(installOnboardingModal && !installOnboardingModal.hidden),
    );
    installOnboardingPrimary?.focus();
  };

  const showApp = (account, { entryEvent = 'auth.welcome' } = {}) => {
    pendingAccount = null;
    stopAuthHeckles({ hide: true });
    if (authShell) authShell.hidden = true;
    if (appShell) appShell.removeAttribute('aria-hidden');
    void loadRandomHomeHero();
    if (welcomeName) {
      const name = String(account?.display_name || '').trim();
      welcomeName.textContent = name || 'Golfer';
    }
    document.body.classList.add('app-ready');

    if (splash && !splash.hidden) {
      splash.classList.remove('splash-auth-ready');
      splash.classList.add('splash-leaving');
      window.setTimeout(() => {
        splash.hidden = true;
        splash.classList.remove('splash-leaving');
      }, 320);
    }

    void showUserHeckleOnce('home', entryEvent).finally(() => {
      window.setTimeout(() => {
        void startUserHeckles(
          'home',
          'home.idle',
          () => (
            Boolean(appShell?.getAttribute('aria-hidden') !== 'true')
            && Boolean(roundFlowModal?.hidden)
            && Boolean(settingsModal?.hidden)
            && Boolean(installOnboardingModal?.hidden)
          ),
        );
      }, 5500);
    });

    window.setTimeout(() => maybeShowInstallOnboarding(account), 0);
  };

  const showRecoveryKey = (
    result,
    {
      statusEvent = 'auth.account_created',
      snarkEvent = 'auth.recovery_key_issued',
    } = {},
  ) => {
    pendingAccount = result.account || null;
    stopAuthHeckles({ hide: true });
    if (authTabs) authTabs.hidden = true;
    authPanels.forEach((panel) => {
      panel.hidden = true;
    });
    setAuthMessage('');
    if (recoveryKeyValue) recoveryKeyValue.textContent = result.recovery_key || '';
    if (recoveryKeyCopy) recoveryKeyCopy.textContent = 'COPIED? GOOD. KEEP IT SAFE.';
    if (recoveryKeyInstruction) {
      recoveryKeyInstruction.textContent = result.recovery_key_rotated
        ? 'Your old recovery key is now invalid. Write this new key down and keep it somewhere physically safe.'
        : 'Write this recovery key down and keep it somewhere physically safe.';
    }
    if (recoveryKeyStatus) recoveryKeyStatus.textContent = '';
    if (recoveryKeySnark) recoveryKeySnark.textContent = '';

    void loadMessageBank(statusEvent, { authenticated: false })
      .then((rows) => {
        const row = pickMessage(rows);
        if (recoveryKeyStatus && row) recoveryKeyStatus.textContent = row.text;
      })
      .catch(() => {});

    void loadMessageBank(snarkEvent, { authenticated: false })
      .then((rows) => {
        const row = pickMessage(rows);
        if (recoveryKeySnark && row) recoveryKeySnark.textContent = row.text;
      })
      .catch(() => {});

    if (recoveryCard) recoveryCard.hidden = false;
  };

  const acceptAuthResult = (
    result,
    {
      showRecovery = false,
      recoveryStatusEvent,
      recoverySnarkEvent,
      entryEvent = 'auth.welcome',
    } = {},
  ) => {
    const token = result?.session?.token;
    if (!token) throw new Error('Server did not return a session token.');
    saveSession(token);

    if (showRecovery) {
      showRecoveryKey(result, {
        statusEvent: recoveryStatusEvent,
        snarkEvent: recoverySnarkEvent,
      });
      return;
    }
    showApp(result.account, { entryEvent });
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
      setAuthMessage('YOUR SESSION EXPIRED — SIGN IN AGAIN.');
      void showAuthHeckleOnce('auth.session_expired');
    }
  };

  const loadRandomHomeHero = async () => {
    if (!homeHeroArt) return;

    try {
      const response = await fetch('/static/assets/_meta/asset-manifest.json');
      if (!response.ok) return;

      const manifest = await response.json();
      const heroes = (manifest.assets || []).filter(
        (item) => (
          item.family === 'home-hero'
          && item.pool === 'home.heroes'
          && item.enabled !== false
          && item.production
        )
      );
      if (!heroes.length) return;

      const rememberedId = window.sessionStorage.getItem(
        HOME_HERO_SESSION_KEY
      );
      let picked = heroes.find(
        (item) => item.asset_id === rememberedId
      );
      if (!picked) {
        picked = heroes[Math.floor(Math.random() * heroes.length)];
      }

      const productionPath = String(picked.production).replace(/^\/+/, '');
      const imagePath = productionPath.startsWith('static/')
        ? `/${productionPath}`
        : `/static/${productionPath}`;

      const preload = new Image();
      preload.addEventListener(
        'load',
        () => {
          homeHeroArt.src = imagePath;
          homeHeroArt.dataset.homeHero = String(
            picked.asset_id || picked.production
          );
          homeHeroArt.classList.add('is-loaded');
        },
        { once: true }
      );
      preload.src = imagePath;

      window.sessionStorage.setItem(
        HOME_HERO_SESSION_KEY,
        String(picked.asset_id || '')
      );
    } catch (_error) {
      // The default approved Home hero remains visible if the manifest is unavailable.
    }
  };

  const loadRandomSplashMini = async () => {
    if (!splashMini) return;

    try {
      const response = await fetch('/static/assets/_meta/asset-manifest.json');
      if (!response.ok) return;

      const manifest = await response.json();
      const minis = (manifest.assets || []).filter(
        (item) => item.family === 'mini-mascot' && item.production
      );
      if (!minis.length) return;

      const picked = minis[Math.floor(Math.random() * minis.length)];
      const productionPath = String(picked.production).replace(/^\/+/, '');
      const imagePath = productionPath.startsWith('static/')
        ? `/${productionPath}`
        : `/static/${productionPath}`;

      splashMini.addEventListener(
        'load',
        () => splashMini.classList.add('is-loaded'),
        { once: true }
      );
      splashMini.src = imagePath;
    } catch (_error) {
      // The branded splash still works if the manifest or selected mini is unavailable.
    }
  };

  const setupMiniOpaqueBottomRatio = (mini) => {
    const cached = Number(mini?.dataset?.opaqueBottomRatio);
    if (Number.isFinite(cached) && cached >= 0) return cached;
    if (!mini?.naturalWidth || !mini?.naturalHeight) return 0;

    const maxDimension = 320;
    const scale = Math.min(
      1,
      maxDimension / Math.max(mini.naturalWidth, mini.naturalHeight)
    );
    const width = Math.max(1, Math.round(mini.naturalWidth * scale));
    const height = Math.max(1, Math.round(mini.naturalHeight * scale));
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const context = canvas.getContext('2d', { willReadFrequently: true });
    if (!context) return 0;

    try {
      context.drawImage(mini, 0, 0, width, height);
      const pixels = context.getImageData(0, 0, width, height).data;
      let lastOpaqueRow = height - 1;

      rowSearch:
      for (let y = height - 1; y >= 0; y -= 1) {
        const rowOffset = y * width * 4;
        for (let x = 0; x < width; x += 1) {
          if (pixels[rowOffset + (x * 4) + 3] > 12) {
            lastOpaqueRow = y;
            break rowSearch;
          }
        }
      }

      const ratio = Math.max(
        0,
        Math.min(1, (height - 1 - lastOpaqueRow) / height)
      );
      mini.dataset.opaqueBottomRatio = String(ratio);
      return ratio;
    } catch (_error) {
      return 0;
    }
  };

  const alignStepTwoMiniToNextButton = () => {
    const stage = [...setupMiniStages].find(
      (item) => Number(item.dataset.setupMiniStage) === 2
    );
    const mini = [...setupMinis].find(
      (item) => Number(item.dataset.setupMini) === 2
    );
    const nextButton = stage?.closest('.setup-step-actions')?.querySelector('.setup-next');
    if (
      !stage
      || !mini
      || !nextButton
      || stage.hidden
      || !mini.complete
      || !mini.naturalHeight
    ) return;

    stage.style.setProperty('--setup-mini-y', '0px');

    window.requestAnimationFrame(() => {
      if (stage.hidden) return;
      const miniRect = mini.getBoundingClientRect();
      const buttonRect = nextButton.getBoundingClientRect();
      const transparentBottom =
        setupMiniOpaqueBottomRatio(mini) * miniRect.height;
      const visibleBottom = miniRect.bottom - transparentBottom;
      const shift = Math.round(buttonRect.top - visibleBottom);
      stage.style.setProperty('--setup-mini-y', `${shift}px`);
    });
  };

  const loadRandomSetupMini = async (step = 1) => {
    const stage = [...setupMiniStages].find(
      (item) => Number(item.dataset.setupMiniStage) === Number(step)
    );
    const mini = [...setupMinis].find(
      (item) => Number(item.dataset.setupMini) === Number(step)
    );
    if (!stage || !mini) return;

    stage.hidden = true;
    stage.style.removeProperty('--setup-mini-y');
    mini.removeAttribute('src');
    delete mini.dataset.opaqueBottomRatio;
    mini.classList.remove('is-loaded');

    try {
      const [manifestResponse, preferences] = await Promise.all([
        fetch('/static/assets/_meta/asset-manifest.json'),
        requestJson('/api/preferences'),
      ]);
      if (!manifestResponse.ok || !preferences?.mini_mascots_enabled) return;

      const manifest = await manifestResponse.json();
      const allMinis = (manifest.assets || []).filter(
        (item) => item.family === 'mini-mascot' && item.production
      );
      const roundStartMinis = allMinis.filter(
        (item) => item.event_key === 'round_start'
      );
      const pool = roundStartMinis.length ? roundStartMinis : allMinis;
      if (!pool.length) return;

      const picked = pool[Math.floor(Math.random() * pool.length)];
      const productionPath = String(picked.production).replace(/^\/+/, '');
      const imagePath = productionPath.startsWith('static/')
        ? `/${productionPath}`
        : `/static/${productionPath}`;

      mini.addEventListener(
        'load',
        () => {
          const searchResultsVisible = (
            Number(step) === 2
            && Boolean(courseResults?.children.length)
          );
          const shouldHide = searchResultsVisible;
          stage.hidden = shouldHide;
          stage.classList.toggle('is-suppressed', shouldHide);
          stage.setAttribute('aria-hidden', shouldHide ? 'true' : 'false');
          mini.classList.add('is-loaded');
          if (Number(step) === 2 && !shouldHide) {
            alignStepTwoMiniToNextButton();
          }
        },
        { once: true }
      );
      mini.src = imagePath;
    } catch (_error) {
      stage.hidden = true;
    }
  };

  const revealShell = async () => {
    await bootSession();
  };

  window.setTimeout(revealShell, 3000);

  authViewButtons.forEach((button) => {
    button.addEventListener('click', () => switchAuthView(button.dataset.authView));
  });

  [loginForm, registerForm, recoverForm].forEach((form) => {
    form?.querySelectorAll('input').forEach((input) => {
      input.addEventListener('focus', pauseAuthHecklesForInteraction);
      input.addEventListener('input', () => {
        setAuthMessage('');
        pauseAuthHecklesForInteraction();
      });
    });
  });

  loginForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setAuthMessage('');
    const values = new FormData(loginForm);
    setFormBusy(loginForm, true);

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
      await showAuthFailure(error, 'auth.login_failed');
    } finally {
      setFormBusy(loginForm, false);
    }
  });

  registerForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setAuthMessage('');
    const values = new FormData(registerForm);
    const validationError = validateRegisterValues(values);
    if (validationError) {
      await showAuthFailure(validationError, 'auth.create_account_failed');
      return;
    }
    setFormBusy(registerForm, true);

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
      acceptAuthResult(result, {
        showRecovery: true,
        recoveryStatusEvent: 'auth.account_created',
        recoverySnarkEvent: 'auth.recovery_key_issued',
      });
      registerForm.reset();
    } catch (error) {
      await showAuthFailure(error, 'auth.create_account_failed');
    } finally {
      setFormBusy(registerForm, false);
    }
  });

  recoverForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setAuthMessage('');
    const values = new FormData(recoverForm);
    const validationError = validateRecoveryValues(values);
    if (validationError) {
      await showAuthFailure(validationError, 'auth.recovery_failed');
      return;
    }
    setFormBusy(recoverForm, true);

    try {
      const result = await requestJson('/api/auth/recover', {
        method: 'POST',
        authenticated: false,
        body: {
          recovery_key: values.get('recovery_key'),
          new_password: values.get('new_password'),
        },
      });
      acceptAuthResult(result, {
        showRecovery: true,
        recoveryStatusEvent: 'auth.password_changed.recovery',
        recoverySnarkEvent: 'auth.recovery_key_warning',
      });
      recoverForm.reset();
    } catch (error) {
      await showAuthFailure(error, 'auth.recovery_failed');
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
      showApp(pendingAccount, { entryEvent: 'auth.welcome' });
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
    stopUserHeckle('home', { hide: true });
    stopUserHeckle('roundSetup', { hide: true });
    stopUserHeckle('install', { hide: true });
    showAuth('login');
    setAuthMessage('SIGNED OUT.');
    void showAuthHeckleOnce('auth.logout');
  });

  const teeOptionLabel = (tee) => {
    const yardage = tee?.total_yardage ? ` • ${tee.total_yardage} YDS` : '';
    const rating = (
      tee?.course_rating !== null
      && tee?.course_rating !== undefined
      && tee?.slope_rating
    )
      ? ` • ${tee.course_rating}/${tee.slope_rating}`
      : '';
    return `${tee?.tee_name || 'Tee'}${yardage}${rating}`;
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

  const renderRoundHandicapEditor = (container, round) => {
    if (!container) return;
    container.replaceChildren();

    const canEdit = viewerIsActivePlayer(round);
    const players = (round.participants || []).filter(
      (participant) =>
        participant.role === 'player'
        && participant.participation_state !== 'removed'
    );

    players.forEach((participant) => {
      const row = document.createElement('div');
      row.className = 'round-handicap-row';

      const copy = document.createElement('div');
      copy.className = 'round-handicap-copy';

      const name = document.createElement('strong');
      name.textContent = participant.display_name || 'Golfer';

      const source = document.createElement('small');
      const index = (
        participant.handicap_index !== null
        && participant.handicap_index !== undefined
      )
        ? `HI ${Number(participant.handicap_index).toFixed(1)}`
        : 'NO PROFILE INDEX';
      const sourceLabel = participant.handicap_source === 'course'
        ? 'AUTO FROM COURSE'
        : (
            participant.handicap_source === 'manual'
              ? 'MANUAL ROUND HANDICAP'
              : 'NET PLACEMENT PENDING'
          );
      source.textContent = `${index} • ${sourceLabel}`;
      copy.append(name, source);

      const input = document.createElement('input');
      input.type = 'number';
      input.min = '-20';
      input.max = '80';
      input.step = '1';
      input.inputMode = 'numeric';
      input.placeholder = 'ROUND HCP';
      input.setAttribute(
        'aria-label',
        `${participant.display_name || 'Golfer'} round handicap`
      );
      input.value = (
        participant.round_handicap !== null
        && participant.round_handicap !== undefined
      )
        ? String(participant.round_handicap)
        : '';
      input.disabled = !canEdit;

      const save = document.createElement('button');
      save.type = 'button';
      save.textContent = 'SAVE HCP';
      save.disabled = !canEdit;

      save.addEventListener('click', async () => {
        const raw = input.value.trim();
        const handicap = raw === '' ? null : Number(raw);
        if (
          handicap !== null
          && (
            !Number.isInteger(handicap)
            || handicap < -20
            || handicap > 80
          )
        ) {
          setRoundFlowMessage('Round handicap must be between -20 and 80.');
          input.focus();
          return;
        }

        save.disabled = true;
        setRoundFlowMessage('');
        try {
          const result = await requestJson(
            `/api/rounds/${round.id}/handicap`,
            {
              method: 'PATCH',
              body: {
                player_participant_id: participant.id,
                round_handicap: handicap,
                confirm_correction: save.dataset.confirm === '1',
              },
            }
          );

          if (result.requires_confirmation) {
            save.dataset.confirm = '1';
            save.textContent = 'CONFIRM CORRECTION';
            save.disabled = false;
            setRoundFlowMessage(
              'Scores already exist. Confirm the handicap correction so the receipt stays honest.'
            );
            return;
          }

          await refreshRound(round.active_code);
        } catch (error) {
          setRoundFlowMessage(error.message);
          save.disabled = false;
        }
      });

      row.append(copy, input, save);
      container.append(row);
    });
  };

  const selectedRoundMode = () => {
    return String(
      startRoundForm?.querySelector('input[name="mode"]:checked')?.value
      || 'individual'
    );
  };

  const refreshStartModeControls = () => {
    const mode = selectedRoundMode();
    if (startTeeLabel) {
      startTeeLabel.textContent = mode === 'scramble'
        ? 'TEAM SCORING TEE'
        : 'YOUR TEE';
    }
    if (individualScoringFieldset) {
      individualScoringFieldset.hidden = mode === 'scramble';
    }
    if (mode === 'scramble' && startRoundForm) {
      const gross = startRoundForm.querySelector(
        'input[name="individual_scoring"][value="gross"]'
      );
      if (gross) gross.checked = true;
    }
  };

  const clearSelectedCourse = () => {
    selectedCourse = null;
    if (selectedCourseBox) {
      selectedCourseBox.hidden = true;
      selectedCourseBox.style.display = 'none';
    }
    if (selectedCourseName) selectedCourseName.textContent = '';
    if (selectedCourseLocation) selectedCourseLocation.textContent = '';
    if (startTeeField) {
      startTeeField.hidden = true;
      startTeeField.style.display = 'none';
    }
    if (startTeeSelect) startTeeSelect.replaceChildren();
  };

  const setCourseStepMessage = (message = '') => {
    if (!courseStepMessage) return;
    courseStepMessage.textContent = message;
    courseStepMessage.hidden = !message;
  };

  const setupMiniParts = (step) => ({
    stage: [...setupMiniStages].find(
      (item) => Number(item.dataset.setupMiniStage) === Number(step)
    ),
    mini: [...setupMinis].find(
      (item) => Number(item.dataset.setupMini) === Number(step)
    ),
  });

  const setRoundHolesHint = (message) => {
    if (roundHolesHint) roundHolesHint.textContent = message;
  };

  const updateRoundHolesHint = () => {
    const courseMode = startRoundForm?.querySelector(
      'input[name="course_mode"]:checked'
    )?.value || 'course';

    if (courseMode === 'free') {
      setRoundHolesHint(
        'Pick 9 or 18. No course data here, so try remembering where you are.'
      );
      return;
    }

    if (!selectedCourse) {
      setRoundHolesHint(
        'Pick 9 or 18. Select a course and we’ll tell you if it only has nine.'
      );
      return;
    }

    const teeHoleCounts = (selectedCourse.tees || [])
      .map((tee) => Number(tee.holes_with_tee || 0))
      .filter((count) => count > 0);
    const physicalCount = teeHoleCounts.length ? Math.max(...teeHoleCounts) : 0;

    if (physicalCount === 9) {
      setRoundHolesHint(
        'Course data says 9 holes. Choose 18 if you’re playing the nine twice.'
      );
    } else if (physicalCount >= 18) {
      setRoundHolesHint(
        'Course data says 18 holes. For once, the numbers are cooperating.'
      );
    } else {
      setRoundHolesHint(
        'Course hole count is unavailable. Pick the round you’re actually playing.'
      );
    }
  };

  const syncStepTwoMiniVisibility = () => {
    const hasSearchResults = Boolean(courseResults?.children.length);
    const { stage, mini } = setupMiniParts(2);
    if (!stage) return;
    const shouldShow = !hasSearchResults;
    stage.hidden = !shouldShow;
    stage.classList.toggle('is-suppressed', !shouldShow);
    stage.setAttribute('aria-hidden', shouldShow ? 'false' : 'true');
    if (courseSearchPanel) {
      courseSearchPanel.classList.toggle('has-results', hasSearchResults);
    }
    if (shouldShow && mini && !mini.src) {
      void loadRandomSetupMini(2);
    } else if (shouldShow && mini?.complete) {
      alignStepTwoMiniToNextButton();
    }
  };

  const setCourseMode = (mode) => {
    const useCourse = mode === 'course';
    setCourseStepMessage('');
    if (courseSearchPanel) courseSearchPanel.hidden = !useCourse;
    if (freePlayField) freePlayField.hidden = useCourse;

    if (!useCourse) {
      clearSelectedCourse();
      if (courseResults) courseResults.replaceChildren();
    }
    updateRoundHolesHint();
    syncStepTwoMiniVisibility();
    renderRoutePreview();
  };

  const selectedRoundHoleCount = () => {
    const checked = startRoundForm?.querySelector('input[name="holes"]:checked');
    return Number(checked?.value || 18);
  };

  const selectedPhysicalHoleCount = () => {
    const courseMode = startRoundForm?.querySelector(
      'input[name="course_mode"]:checked'
    )?.value;
    if (courseMode === 'free') {
      const checked = startRoundForm?.querySelector(
        'input[name="course_hole_count"]:checked'
      );
      return Number(checked?.value || 18);
    }

    const teeHoleCounts = (selectedCourse?.tees || [])
      .map((tee) => Number(tee.holes_with_tee || 0))
      .filter((count) => count > 0);
    return teeHoleCounts.length ? Math.max(...teeHoleCounts) : 18;
  };

  const renderRoutePreview = () => {
    if (!routePreview || !startHoleInput) return;
    const physicalCount = selectedPhysicalHoleCount();
    const holes = selectedRoundHoleCount();
    const start = Number(startHoleInput.value || 1);
    startHoleInput.max = String(physicalCount);

    if (!Number.isInteger(start) || start < 1 || start > physicalCount) {
      routePreview.textContent = `STARTING HOLE MUST BE 1-${physicalCount}`;
      return;
    }

    const route = [];
    for (let index = 0; index < holes; index += 1) {
      route.push(((start - 1 + index) % physicalCount) + 1);
    }

    const previousTracking = Number(trackingStartPosition?.value || 1);
    const selectedTracking = Math.max(
      1,
      Math.min(
        Number.isInteger(previousTracking) ? previousTracking : 1,
        route.length
      )
    );
    if (trackingStartPosition) {
      trackingStartPosition.replaceChildren();
      route.forEach((holeNumber, index) => {
        const position = index + 1;
        const option = document.createElement('option');
        option.value = String(position);
        option.textContent =
          `HOLE ${holeNumber} • ${position} OF ${route.length}`;
        option.selected = position === selectedTracking;
        trackingStartPosition.append(option);
      });
    }
    if (priorHolesMode) {
      priorHolesMode.hidden = selectedTracking <= 1;
    }

    const short = route.length <= 9
      ? route.join(', ')
      : `${route.slice(0, 6).join(', ')} … ${route.slice(-3).join(', ')}`;
    const trackingCopy = selectedTracking > 1
      ? ` • APP JOINS AT ${selectedTracking} OF ${route.length}`
      : '';
    routePreview.textContent =
      `ROUTE: ${short} • ${holes} HOLE${holes === 1 ? '' : 'S'}${trackingCopy}`;
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
      setCourseStepMessage('');
      updateRoundHolesHint();
      renderRoutePreview();

      if (courseResults) courseResults.replaceChildren();

      if (selectedCourseName) selectedCourseName.textContent = course.name || 'Selected course';
      if (selectedCourseLocation) {
        const pieces = [result.city, result.state, result.country].filter(Boolean);
        selectedCourseLocation.textContent = pieces.join(', ');
      }
      if (selectedCourseBox) {
        selectedCourseBox.hidden = false;
        selectedCourseBox.style.removeProperty('display');
      }

      const tees = course.tees || [];
      refreshStartModeControls();
      fillTeeSelect(startTeeSelect, tees);
      if (startTeeField) {
        const showTee = tees.length > 0;
        startTeeField.hidden = !showTee;
        if (showTee) startTeeField.style.removeProperty('display');
        else startTeeField.style.display = 'none';
      }
      syncStepTwoMiniVisibility();
      setRoundFlowMessage('');
    } catch (error) {
      setRoundFlowMessage(error.message);
    }
  };

  const renderCourseResults = (results) => {
    if (!courseResults) return;
    courseResults.replaceChildren();

    // A new search invalidates the prior course/tee presentation. Keeping it
    // visible steals the space reserved for the three search results.
    clearSelectedCourse();
    updateRoundHolesHint();
    renderRoutePreview();

    if (!results.length) {
      const empty = document.createElement('div');
      empty.className = 'selected-course';
      empty.textContent = 'No course found. Try another search or use Free Play.';
      courseResults.append(empty);
      syncStepTwoMiniVisibility();
      return;
    }

    results.slice(0, 3).forEach((result) => {
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
    syncStepTwoMiniVisibility();
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

  const setSetupStep = (step) => {
    const resolved = Math.max(1, Math.min(3, Number(step) || 1));
    setupSteps.forEach((panel) => {
      const active = Number(panel.dataset.setupStep) === resolved;
      panel.hidden = !active;
      panel.classList.toggle('is-active', active);
    });
    setupStepDots.forEach((dot) => {
      const value = Number(dot.dataset.setupStepDot);
      dot.classList.toggle('is-active', value === resolved);
      dot.classList.toggle('is-complete', value < resolved);
    });
    if (resolved === 2) {
      setCourseMode(
        startRoundForm?.querySelector('input[name="course_mode"]:checked')?.value
        || 'course'
      );
    }
    if (resolved === 3) renderRoutePreview();
    if (
      resolved !== 2
      || startRoundForm?.querySelector('input[name="course_mode"]:checked')?.value === 'course'
    ) {
      void loadRandomSetupMini(resolved);
    }
  };

  const setRoundFlowMessage = (message = '') => {
    if (!roundFlowMessage) return;
    roundFlowMessage.textContent = message;
    roundFlowMessage.hidden = !message;
  };

  const closeRoundFlow = () => {
    if (!roundFlowModal) return;
    stopUserHeckle('roundSetup', { hide: true });
    roundFlowModal.hidden = true;
    document.body.classList.remove('modal-open');
    setRoundFlowMessage('');
    if (bagModal) bagModal.hidden = true;
    currentBagAction = null;
    currentLobbyRound = null;
    viewedRoutePosition = null;
    finishIncompletePending = false;
    resetClaimPlayerPanel();
    advanceWarningPosition = null;
    pendingScoreAfterPar = null;
    parEditorOpen = false;
    if (advanceWarningPanel) advanceWarningPanel.hidden = true;
    if (roundSettingsPanel) roundSettingsPanel.hidden = true;
    claimUndoConfirmPending = false;
    if (claimUndoPanel) claimUndoPanel.hidden = true;
    if (endEarlyPanel) endEarlyPanel.hidden = true;
    if (towelPanel) towelPanel.hidden = true;
    if (towelReason) towelReason.value = '';
    clearSelectedCourse();
    if (lobbyRefreshTimer) {
      window.clearInterval(lobbyRefreshTimer);
      lobbyRefreshTimer = null;
    }
    if (sessionToken()) {
      void startUserHeckles(
        'home',
        'home.idle',
        () => (
          Boolean(appShell?.getAttribute('aria-hidden') !== 'true')
          && Boolean(roundFlowModal?.hidden)
          && Boolean(settingsModal?.hidden)
          && Boolean(installOnboardingModal?.hidden)
        ),
      );
    }
  };

  const resetClaimPlayerPanel = () => {
    pendingClaimJoin = null;
    pendingJoinPreview = null;
    if (claimPlayerPanel) claimPlayerPanel.hidden = true;
    if (claimPlayerList) claimPlayerList.replaceChildren();
    if (joinTeeField) joinTeeField.hidden = true;
    if (joinTeeSelect) joinTeeSelect.replaceChildren();
    if (joinRoundSubmit) {
      joinRoundSubmit.hidden = false;
      joinRoundSubmit.textContent = 'LET ME INTO THIS MESS';
    }
  };

  const showRoundPanel = (panel) => {
    if (!roundFlowModal) return;
    roundFlowCardGame?.classList.remove('is-live-round');
    stopUserHeckle('home');
    stopUserHeckle('roundSetup', { hide: true });
    roundFlowModal.hidden = false;
    document.body.classList.add('modal-open');
    setRoundFlowMessage('');
    currentLobbyRound = null;
    resetClaimPlayerPanel();

    if (startRoundForm) startRoundForm.hidden = panel !== 'start';
    setCourseStepMessage('');
    if (joinRoundForm) joinRoundForm.hidden = panel !== 'join';
    if (lobbyPanel) lobbyPanel.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = true;
    roundFlowCardGame?.classList.remove('is-live-round');
    if (roundEndPanel) roundEndPanel.hidden = true;
    if (receiptsPanel) receiptsPanel.hidden = true;
    if (roundFlowTitle) {
      roundFlowTitle.textContent = panel === 'start' ? 'START A ROUND' : 'JOIN A ROUND';
    }
    if (roundSetupHeckle) {
      const showSetupChrome = panel === 'start';
      roundSetupHeckle.hidden = !showSetupChrome;
      roundSetupHeckle.classList.toggle('is-panel-hidden', !showSetupChrome);
    }
    if (panel === 'start') {
      if (roundSetupHeckle) {
        roundSetupHeckle.hidden = false;
        roundSetupHeckle.classList.remove('is-panel-hidden');
      }
      if (roundSetupHeckleText && !roundSetupHeckleText.textContent) {
        roundSetupHeckleText.textContent = ' ';
      }
      setSetupStep(1);
      clearSelectedCourse();
      setCourseMode(
        startRoundForm?.querySelector('input[name="course_mode"]:checked')?.value
        || 'course'
      );
      void startUserHeckles(
        'roundSetup',
        'round_setup.idle',
        () => (
          Boolean(roundFlowModal && !roundFlowModal.hidden)
          && Boolean(startRoundForm && !startRoundForm.hidden)
        ),
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

  const missingScoresAtPosition = (round, position) => {
    if (round.mode === 'scramble') {
      return findScore(round, position) ? [] : ['TEAM SCORE'];
    }

    return (round.participants || [])
      .filter((participant) =>
        participant.role === 'player'
        && participant.participation_state === 'active'
        && Number(participant.tracked_from_position || 1) <= Number(position)
      )
      .filter((participant) => !findScore(round, position, participant.id))
      .map((participant) => participant.display_name || 'Golfer');
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

    const events = round.events || [];
    const backfilled = [];
    for (const item of events) {
      if (
        ['score_report', 'score_push'].includes(item.event_type)
        && item.data?.backfilled
      ) {
        backfilled.push(item);
        continue;
      }
      break;
    }

    if (backfilled.length) {
      const participantIds = new Set(
        backfilled
          .map((item) => item.data?.player_participant_id)
          .filter(Boolean)
          .map(String)
      );
      let subject = 'THE HISTORICAL RECORD';
      if (participantIds.size === 1) {
        const participantId = [...participantIds][0];
        const participant = (round.participants || []).find(
          (row) => String(row.id) === participantId
        );
        if (participant?.display_name) {
          subject = participant.display_name.toUpperCase();
        }
      } else if (round.mode === 'scramble') {
        subject = 'THE TEAM';
      }

      const count = backfilled.length;
      if (latestBanter) {
        latestBanter.textContent =
          `${subject} JUST FILED ${count} SCORE${count === 1 ? '' : 'S'} AFTER THE FACT.`;
      }
      if (latestFallback) {
        latestFallback.textContent =
          'THE HISTORICAL RECORD HAS BEEN CONVENIENTLY UPDATED.';
      }
      if (latestMascot) {
        latestMascot.removeAttribute('src');
        latestMascot.alt = '';
        latestMascot.hidden = true;
      }
      latestPresentation.hidden = false;
      return;
    }

    const event = events.find((item) => {
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

    const responsePanel = document.createElement('details');
    responsePanel.className = 'score-response-panel live-score-social-details';

    const responseSummary = document.createElement('summary');
    responseSummary.textContent = 'REACTIONS / CHALLENGES';
    responsePanel.append(responseSummary);

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

        const actorName =
          reply.data?.actor_display_name
          || actor?.display_name
          || 'Someone';
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
      && route?.state !== 'skipped'
      && Number(position) <= Number(round.current_route_position)
    );

    const addCard = (label, participantId = null, detail = '') => {
      const score = findScore(round, position, participantId);
      const card = document.createElement('section');
      card.className = 'live-score-card live-score-row';

      const identity = document.createElement('div');
      identity.className = 'live-score-identity';

      const avatar = document.createElement('span');
      avatar.className = 'live-score-avatar';
      avatar.textContent = String(label || 'G').trim().charAt(0).toUpperCase();

      const identityCopy = document.createElement('div');
      const name = document.createElement('strong');
      name.textContent = label;
      const meta = document.createElement('small');
      const relative = score && par
        ? scoreRelativeLabel(Number(score.strokes), Number(par))
        : '';
      meta.textContent = [
        detail,
        score ? (relative ? (relative + ' TO PAR') : 'SCORE SAVED') : 'NO SCORE',
      ]
        .filter(Boolean)
        .join(' • ');
      identityCopy.append(name, meta);
      identity.append(avatar, identityCopy);
      card.append(identity);

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
        readonly.textContent = route?.state === 'skipped'
          ? 'UNTRACKED'
          : (score ? String(score.strokes) : '—');
        card.append(readonly);
        appendScoreResponsePanel(card, round, position, participantId, score);
        liveScoreArea.append(card);
        return;
      }

      const controls = document.createElement('div');
      controls.className = 'live-score-stepper';

      const minus = document.createElement('button');
      minus.type = 'button';
      minus.className = 'live-score-step';
      minus.textContent = '−';
      minus.setAttribute('aria-label', 'Lower ' + label + ' score');

      const input = document.createElement('input');
      input.className = 'live-score-input';
      input.type = 'number';
      input.min = '1';
      input.max = '99';
      input.inputMode = 'numeric';
      input.value = score ? String(score.strokes) : '';
      input.placeholder = '—';
      input.setAttribute(
        'aria-label',
        'Enter ' + label + ' strokes for hole ' + hole
      );

      const plus = document.createElement('button');
      plus.type = 'button';
      plus.className = 'live-score-step';
      plus.textContent = '+';
      plus.setAttribute('aria-label', 'Raise ' + label + ' score');

      const setBusy = (busy) => {
        minus.disabled = busy;
        plus.disabled = busy;
        input.disabled = busy;
      };

      const persistScore = async (strokes) => {
        if (!Number.isInteger(strokes) || strokes < 1 || strokes > 99) {
          setRoundFlowMessage('Strokes must be between 1 and 99.');
          return false;
        }

        if (round.par_tracking_enabled && !par) {
          pendingScoreAfterPar = {
            roundId: String(round.id),
            activeCode: round.active_code,
            position: Number(position),
            participantId,
            strokes,
          };
          setRoundFlowMessage('WE NEED PAR BEFORE WE CAN JUDGE YOU PROPERLY.');
          parInput?.focus();
          return false;
        }

        pendingScoreAfterPar = null;
        setBusy(true);
        setRoundFlowMessage('');
        try {
          const body = { strokes };
          if (round.mode === 'individual') {
            body.player_participant_id = participantId;
          }
          await requestJson(
            '/api/rounds/' + round.id + '/positions/' + position + '/score',
            { method: 'PUT', body }
          );
          await refreshRound(round.active_code);
          return true;
        } catch (error) {
          setRoundFlowMessage(error.message);
          setBusy(false);
          return false;
        }
      };

      minus.addEventListener('click', async () => {
        const base = Number(input.value || score?.strokes || par || 1);
        const next = Math.max(1, base - 1);
        input.value = String(next);
        await persistScore(next);
      });

      plus.addEventListener('click', async () => {
        const base = Number(input.value || score?.strokes || par || 1);
        const next = Math.min(99, base + 1);
        input.value = String(next);
        await persistScore(next);
      });

      input.addEventListener('change', async () => {
        const strokes = Number(input.value);
        await persistScore(strokes);
      });

      controls.append(minus, input, plus);
      card.append(controls);

      if (score) {
        const remove = document.createElement('button');
        remove.type = 'button';
        remove.className = 'live-score-remove';
        remove.textContent = '×';
        remove.setAttribute('aria-label', 'REMOVE SCORE FOR ' + label);
        remove.addEventListener('click', async () => {
          remove.disabled = true;
          setRoundFlowMessage('');
          try {
            const body = {};
            if (round.mode === 'individual') {
              body.player_participant_id = participantId;
            }
            await requestJson(
              '/api/rounds/' + round.id + '/positions/' + position + '/score',
              { method: 'DELETE', body }
            );
            await refreshRound(round.active_code);
          } catch (error) {
            setRoundFlowMessage(error.message);
            remove.disabled = false;
          }
        });
        card.append(remove);
      }

      appendScoreResponsePanel(card, round, position, participantId, score);
      liveScoreArea.append(card);
    };

    if (round.mode === 'scramble') {
      addCard('TEAM SCORE', null, 'SCRAMBLE');
      return;
    }

    (round.participants || [])
      .filter((participant) => participant.role === 'player')
      .forEach((participant) => {
        const details = [];
        if (participant.round_only) details.push('OFFLINE');
        if (participant.tee_name) details.push(participant.tee_name + ' TEE');
        if (
          participant.round_handicap !== null
          && participant.round_handicap !== undefined
        ) {
          details.push('HCP ' + participant.round_handicap);
        }
        addCard(
          participant.display_name || 'Golfer',
          participant.id,
          details.join(' • ')
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

  const APP_BANTER_AVATAR =
    '/static/assets/icons/alternates/WPM_Icon_Mascot_Alt2.webp';

  const renderLiveHoleSelector = (round, viewedPosition, livePosition) => {
    if (!liveHoleSelector) return;
    liveHoleSelector.replaceChildren();

    (round.route || []).forEach((route) => {
      const position = Number(route.route_position);
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = String(route.hole_number || position);
      button.dataset.routePosition = String(position);
      button.classList.toggle('is-viewed', position === Number(viewedPosition));
      button.classList.toggle('is-live', position === Number(livePosition));
      button.classList.toggle('is-skipped', route.state === 'skipped');
      button.setAttribute(
        'aria-label',
        'View hole ' + String(route.hole_number || position)
      );
      button.addEventListener('click', () => {
        if (!currentLobbyRound) return;
        parEditorOpen = false;
        viewedRoutePosition = position;
        renderLiveRound(currentLobbyRound);
      });
      liveHoleSelector.append(button);
    });
  };

  const renderLiveBanter = (round) => {
    if (!liveBanterFeed) return;
    liveBanterFeed.replaceChildren();

    const socialTypes = new Set([
      'open_mic',
      'callout',
      'praise',
      'shot_call',
      'challenge',
      'excuse',
      'score_response',
      'score_report',
      'score_push',
      'round_end_result',
    ]);

    const rows = (round.events || [])
      .filter((event) => {
        const text = String(presentationText(event) || '').trim();
        if (!text) return false;
        const presentation = event.presentation || {};
        return (
          socialTypes.has(String(event.event_type || ''))
          || Boolean(presentation.banter?.text)
          || Boolean(presentation.mascot?.copy)
          || Boolean(presentation.fallback?.text)
        );
      })
      .slice(0, 8)
      .reverse();

    if (!rows.length) {
      const empty = document.createElement('div');
      empty.className = 'live-banter-empty';
      empty.textContent = 'Quiet so far. Suspicious.';
      liveBanterFeed.append(empty);
      return;
    }

    rows.forEach((event) => {
      const actor = (round.participants || []).find(
        (participant) =>
          String(participant.id) === String(event.actor_participant_id || '')
      );
      const explicitMessage = String(event.data?.message || '').trim();
      const playerAuthored = Boolean(
        actor
        && explicitMessage
        && ['open_mic', 'callout', 'praise', 'shot_call', 'challenge', 'excuse', 'score_response']
          .includes(String(event.event_type || ''))
      );

      const row = document.createElement('div');
      row.className = playerAuthored
        ? 'live-banter-row is-player'
        : 'live-banter-row is-app';

      const avatar = document.createElement('div');
      avatar.className = playerAuthored
        ? 'live-banter-avatar is-player'
        : 'live-banter-avatar is-app';

      if (playerAuthored) {
        avatar.textContent = String(actor?.display_name || 'G')
          .trim()
          .charAt(0)
          .toUpperCase();
      } else {
        const image = document.createElement('img');
        image.src = APP_BANTER_AVATAR;
        image.alt = 'Who Pushed Me mascot';
        avatar.append(image);
      }

      const content = document.createElement('div');
      content.className = 'live-banter-content';

      const meta = document.createElement('div');
      meta.className = 'live-banter-meta';
      const author = document.createElement('strong');
      author.textContent = playerAuthored
        ? (actor?.display_name || 'Golfer')
        : 'WPM';
      const time = document.createElement('span');
      if (event.created_at) {
        const date = new Date(event.created_at);
        if (!Number.isNaN(date.getTime())) {
          time.textContent = date.toLocaleTimeString([], {
            hour: 'numeric',
            minute: '2-digit',
          });
        }
      }
      meta.append(author, time);

      const bubble = document.createElement('div');
      bubble.className = 'live-banter-bubble';
      bubble.textContent = presentationText(event);

      content.append(meta, bubble);
      row.append(avatar, content);
      liveBanterFeed.append(row);
    });

    liveBanterFeed.scrollTop = liveBanterFeed.scrollHeight;
  };

  const appendLobbyBanterRow = ({
    text,
    actorName = 'WPM',
    playerAuthored = false,
    createdAt = null,
  }) => {
    if (!lobbyBanterFeed || !text) return;

    const row = document.createElement('div');
    row.className = playerAuthored
      ? 'live-banter-row is-player'
      : 'live-banter-row is-app';

    const avatar = document.createElement('div');
    avatar.className = playerAuthored
      ? 'live-banter-avatar is-player'
      : 'live-banter-avatar is-app';

    if (playerAuthored) {
      avatar.textContent = String(actorName || 'G')
        .trim()
        .charAt(0)
        .toUpperCase();
    } else {
      const image = document.createElement('img');
      image.src = APP_BANTER_AVATAR;
      image.alt = 'Who Pushed Me mascot';
      avatar.append(image);
    }

    const content = document.createElement('div');
    content.className = 'live-banter-content';

    const meta = document.createElement('div');
    meta.className = 'live-banter-meta';
    const author = document.createElement('strong');
    author.textContent = playerAuthored ? actorName : 'WPM';
    const time = document.createElement('span');
    if (createdAt) {
      const date = new Date(createdAt);
      if (!Number.isNaN(date.getTime())) {
        time.textContent = date.toLocaleTimeString([], {
          hour: 'numeric',
          minute: '2-digit',
        });
      }
    }
    meta.append(author, time);

    const bubble = document.createElement('div');
    bubble.className = 'live-banter-bubble';
    bubble.textContent = text;

    content.append(meta, bubble);
    row.append(avatar, content);
    lobbyBanterFeed.append(row);
  };

  const renderLobbyBanter = (round) => {
    if (!lobbyBanterFeed) return;
    lobbyBanterFeed.replaceChildren();

    const eventRows = (round.events || [])
      .filter((event) => {
        const text = String(presentationText(event) || '').trim();
        if (!text) return false;
        return (
          event.event_type === 'open_mic'
          || String(event.content_event_key || '').startsWith('lobby.')
          || String(event.event_type || '').startsWith('player_join')
          || String(event.event_type || '').includes('join')
        );
      })
      .slice(0, 10)
      .reverse();

    eventRows.forEach((event) => {
      const actor = (round.participants || []).find(
        (participant) =>
          String(participant.id) === String(event.actor_participant_id || '')
      );
      const playerAuthored = (
        event.event_type === 'open_mic'
        && Boolean(actor)
        && Boolean(String(event.data?.message || '').trim())
      );
      appendLobbyBanterRow({
        text: presentationText(event),
        actorName: actor?.display_name || 'Golfer',
        playerAuthored,
        createdAt: event.created_at,
      });
    });

    lobbyIdleMessages.forEach((message) => {
      appendLobbyBanterRow({
        text: message.text,
        actorName: 'WPM',
        playerAuthored: false,
        createdAt: message.created_at,
      });
    });

    if (!lobbyBanterFeed.childElementCount) {
      const empty = document.createElement('div');
      empty.className = 'live-banter-empty';
      empty.textContent = 'Waiting for somebody to embarrass themselves.';
      lobbyBanterFeed.append(empty);
    }

    lobbyBanterFeed.scrollTop = lobbyBanterFeed.scrollHeight;
  };

  const stopLobbyBanterRotation = () => {
    if (lobbyBanterTimer) {
      window.clearInterval(lobbyBanterTimer);
      lobbyBanterTimer = null;
    }
    lobbyBanterRoundId = '';
    lobbyIdleRows = [];
    lobbyIdleLastId = '';
    lobbyIdleMessages = [];
  };

  const startLobbyBanterRotation = async (round) => {
    const roundId = String(round?.id || '');
    if (!roundId || round.status !== 'setup') return;
    if (lobbyBanterRoundId === roundId) return;

    stopLobbyBanterRotation();
    lobbyBanterRoundId = roundId;

    try {
      lobbyIdleRows = await loadMessageBank('lobby.idle', {
        authenticated: true,
      });
    } catch (_error) {
      lobbyIdleRows = [];
      return;
    }

    if (
      lobbyBanterRoundId !== roundId
      || !lobbyIdleRows.length
    ) {
      return;
    }

    const addIdleMessage = () => {
      if (
        !currentLobbyRound
        || String(currentLobbyRound.id) !== roundId
        || currentLobbyRound.status !== 'setup'
        || !lobbyPanel
        || lobbyPanel.hidden
      ) {
        return;
      }

      const picked = pickMessage(lobbyIdleRows, lobbyIdleLastId);
      if (!picked) return;
      lobbyIdleLastId = picked.id;
      lobbyIdleMessages.push({
        id: picked.id + ':' + String(Date.now()),
        text: picked.text,
        created_at: new Date().toISOString(),
      });
      lobbyIdleMessages = lobbyIdleMessages.slice(-6);
      renderLobbyBanter(currentLobbyRound);
    };

    lobbyBanterTimer = window.setInterval(
      addIdleMessage,
      LOBBY_BANTER_ROTATE_MS,
    );
  };

  const renderLiveHoleStats = (round, position) => {
    if (!liveHoleStats) return;

    const par = findPar(round, position);
    let scores = [];
    let expected = 1;

    if (round.mode === 'scramble') {
      const score = findScore(round, position);
      if (score) scores = [Number(score.strokes)];
    } else {
      const players = (round.participants || []).filter(
        (participant) =>
          participant.role === 'player'
          && participant.participation_state === 'active'
          && Number(participant.tracked_from_position || 1) <= Number(position)
      );
      expected = players.length;
      scores = players
        .map((participant) => findScore(round, position, participant.id))
        .filter(Boolean)
        .map((score) => Number(score.strokes));
    }

    liveHoleStats.replaceChildren();

    const heading = document.createElement('div');
    heading.className = 'live-hole-stat-heading';
    heading.innerHTML = '<strong>HOLE STATS</strong><small>REAL SCORES ONLY</small>';
    liveHoleStats.append(heading);

    const addStat = (label, value) => {
      const stat = document.createElement('div');
      stat.className = 'live-hole-stat';
      const small = document.createElement('small');
      small.textContent = label;
      const strong = document.createElement('strong');
      strong.textContent = value;
      stat.append(small, strong);
      liveHoleStats.append(stat);
    };

    const average = scores.length
      ? (scores.reduce((sum, value) => sum + value, 0) / scores.length)
      : null;
    const averageRelative = average !== null && par
      ? average - Number(par)
      : null;

    addStat('SCORES IN', String(scores.length) + '/' + String(expected || 1));
    addStat('AVG SCORE', average === null ? '—' : average.toFixed(1));
    addStat(
      'AVG TO PAR',
      averageRelative === null
        ? '—'
        : (averageRelative === 0
          ? 'E'
          : (averageRelative > 0
            ? ('+' + averageRelative.toFixed(1))
            : averageRelative.toFixed(1)))
    );

    liveHoleStats.hidden = false;
  };

  const setLiveNavActive = (activeButton) => {
    [liveNavPlay, liveNavScorecard, liveNavStats, liveNavMore].forEach(
      (button) => button?.classList.toggle('is-active', button === activeButton)
    );
  };

  const updateReceiptsBadge = (round) => {
    if (!receiptsUnseenBadge) return;
    const unseen = Number(round.receipts_state?.unseen_count || 0);
    receiptsUnseenBadge.hidden = unseen < 1;
    receiptsUnseenBadge.textContent =
      `YOU MISSED SOME SHIT • ${unseen}`;
  };

  const markReceiptsSeen = async (round) => {
    const unseen = Number(round?.receipts_state?.unseen_count || 0);
    if (!round?.id || unseen < 1 || receiptMarkInFlight) return;

    receiptMarkInFlight = true;
    try {
      const state = await requestJson(
        `/api/rounds/${round.id}/receipts-seen`,
        { method: 'PATCH', body: {} }
      );
      if (
        currentLobbyRound
        && String(currentLobbyRound.id) === String(round.id)
      ) {
        currentLobbyRound.receipts_state = state;
        updateReceiptsBadge(currentLobbyRound);
      }
    } catch (_error) {
      // Catch-up marking is non-blocking. The next refresh/open can retry.
    } finally {
      receiptMarkInFlight = false;
    }
  };

  const renderReceipts = (round) => {
    if (!receiptsPanel || !receiptsList) return;

    const events = round.events || [];
    receiptsPanel.hidden = events.length === 0;
    updateReceiptsBadge(round);
    receiptsList.replaceChildren();

    events.slice(0, 40).forEach((event) => {
      const row = document.createElement('div');
      row.className = 'receipt-row';

      const title = document.createElement('strong');
      if (event.event_type === 'tee_change') {
        const actor = (round.participants || []).find(
          (participant) =>
            String(participant.id) === String(event.actor_participant_id)
        );
        const actorName = String(
          event.data?.actor_display_name
          || actor?.display_name
          || 'SOMEONE'
        ).toUpperCase();
        const oldTee = String(event.old_value || 'UNSET').toUpperCase();
        const newTee = String(event.new_value || 'UNSET').toUpperCase();
        const scope = event.data?.scope === 'team' ? 'TEAM TEE' : 'TEE';
        title.textContent =
          `${actorName} CHANGED ${scope} ${oldTee} → ${newTee}`;
      } else if (event.event_type === 'score_removed') {
        const actor = (round.participants || []).find(
          (participant) =>
            String(participant.id) === String(event.actor_participant_id)
        );
        const subject = event.data?.scope === 'team'
          ? 'TEAM SCORE'
          : String(event.data?.subject || 'GOLFER').toUpperCase();
        const oldScore = Number(event.old_value);
        const actorName = String(
          event.data?.actor_display_name
          || actor?.display_name
          || 'SOMEONE'
        ).toUpperCase();
        title.textContent = event.data?.scope === 'team'
          ? `${actorName} REMOVED ${subject} ${oldScore}`
          : `${actorName} REMOVED ${subject}'S ${oldScore}`;
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

      if (['score_report', 'score_push'].includes(event.event_type)) {
        const social = document.createElement('div');
        social.className = 'receipt-social-summary';

        const reactions = eventReactions(round, event.id);
        if (reactions.length) {
          const counts = new Map();
          reactions.forEach((reaction) => {
            const kind = String(reaction.reaction_kind || '').toUpperCase();
            counts.set(kind, (counts.get(kind) || 0) + 1);
          });
          const reactionLine = document.createElement('small');
          reactionLine.textContent = `REACTIONS: ${[...counts.entries()]
            .map(([kind, count]) => `${kind} ${count}`)
            .join(' • ')}`;
          social.append(reactionLine);
        }

        const replies = scoreResponses(round, event.id);
        replies
          .filter((reply) => ['custom', 'blame'].includes(reply.data?.response_kind))
          .slice()
          .reverse()
          .forEach((reply) => {
            const actor = (round.participants || []).find(
              (participant) =>
                String(participant.id) === String(reply.actor_participant_id)
            );
            const line = document.createElement('small');
            const actorName =
              reply.data?.actor_display_name
              || actor?.display_name
              || 'Someone';
            line.textContent =
              `${actorName}: ${presentationText(reply)
                || String(reply.data?.message || reply.data?.response_kind || '')}`;
            social.append(line);
          });

        const challenges = activeScoreChallenges(round, event.id);
        if (challenges.length) {
          const challengeLine = document.createElement('small');
          challengeLine.textContent =
            `CHALLENGES: ${challenges.map((challenge) => {
              const challenger = (round.participants || []).find(
                (participant) =>
                  String(participant.id)
                  === String(challenge.challenger_participant_id)
              );
              const pieces = [
                challenger?.display_name || 'Someone',
                challenge.proposed_score
                  ? `SAYS ${challenge.proposed_score}`
                  : '',
                challenge.comment || '',
              ].filter(Boolean);
              return pieces.join(' ');
            }).join(' • ')}`;
          social.append(challengeLine);
        }

        if (social.childElementCount) row.append(social);
      }

      receiptsList.append(row);
    });

    if (receiptsPanel.open) {
      void markReceiptsSeen(round);
    }
  };

  receiptsPanel?.addEventListener('toggle', () => {
    if (!receiptsPanel.open || !currentLobbyRound) return;
    void markReceiptsSeen(currentLobbyRound);
  });

  const totalParForRound = (round) => {
    const plannedPositions = (round.route || [])
      .filter((route) => route.state !== 'skipped')
      .map((route) => Number(route.route_position));
    const pars = new Map(
      (round.pars || []).map((row) => [
        Number(row.route_position),
        Number(row.par),
      ])
    );
    if (
      !plannedPositions.length
      || plannedPositions.some((position) => !pars.has(position))
    ) {
      return null;
    }
    return plannedPositions.reduce(
      (total, position) => total + Number(pars.get(position) || 0),
      0
    );
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
    roundFlowCardGame?.classList.remove('is-live-round');
    if (roundEndPanel) roundEndPanel.hidden = false;
    const endedEarly = round.end_reason === 'ended_early';
    if (roundFlowTitle) {
      roundFlowTitle.textContent = endedEarly
        ? 'ROUND ENDED EARLY'
        : (round.results?.complete ? 'ROUND COMPLETE' : 'ROUND ENDED');
    }

    if (lobbyRefreshTimer) {
      window.clearInterval(lobbyRefreshTimer);
      lobbyRefreshTimer = null;
    }

    const place = round.course?.name || round.free_play_name || 'Golf';
    const resultsComplete = Boolean(round.results?.complete);
    if (roundEndTitle) {
      roundEndTitle.textContent = endedEarly
        ? 'THE GROUP CALLED IT.'
        : (
            resultsComplete
              ? 'THE DAMAGE IS FINAL.'
              : 'INCOMPLETE SCORECARD.'
          );
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
        const baseSummary = resultsComplete || missing === 0
          ? place
          : `${place} • ${missing} REQUIRED SCORE${missing === 1 ? '' : 'S'} MISSING`;
        if (round.net_scoring_enabled) {
          const missingHandicaps = Number(
            round.results?.missing_handicaps || 0
          );
          roundEndSummary.textContent = round.results?.net_official
            ? `${baseSummary} • GROSS + NET OFFICIAL`
            : (
                missingHandicaps > 0
                  ? `${baseSummary} • NET WAITING ON ${missingHandicaps} HANDICAP${missingHandicaps === 1 ? '' : 'S'}`
                  : `${baseSummary} • NET PLACEMENT PENDING`
              );
        } else {
          roundEndSummary.textContent = baseSummary;
        }
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
          const pieces = [
            `${result.total_strokes} GROSS`,
            relative ? `${relative} TO PAR` : '',
          ];
          if (round.net_scoring_enabled) {
            if (
              result.round_handicap === null
              || result.round_handicap === undefined
            ) {
              pieces.push('NET PENDING HANDICAP');
            } else {
              pieces.push(`HCP ${result.round_handicap}`);
              if (
                result.net_total_strokes !== null
                && result.net_total_strokes !== undefined
              ) {
                pieces.push(`${result.net_total_strokes} NET`);
              }
              if (
                round.results?.net_official
                && result.net_rank !== null
                && result.net_rank !== undefined
              ) {
                const tiedNet = Number(result.net_tie_count || 0) > 1;
                pieces.push(
                  tiedNet
                    ? `NET T${result.net_rank}`
                    : `NET #${result.net_rank}`
                );
              } else {
                pieces.push('NET PLACEMENT PENDING');
              }
            }
          }
          score.textContent = pieces.filter(Boolean).join(' • ');
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

    if (
      pendingScoreAfterPar
      && (
        String(pendingScoreAfterPar.roundId) !== String(round.id)
        || Number(pendingScoreAfterPar.position) !== Number(viewedRoutePosition)
      )
    ) {
      pendingScoreAfterPar = null;
    }

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
    roundFlowCardGame?.classList.add('is-live-round');
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
    const viewer = viewerParticipant(round);
    const viewingLive = Number(viewedRoutePosition) === livePosition;
    const viewingPast = Number(viewedRoutePosition) < livePosition;
    const viewingFuture = Number(viewedRoutePosition) > livePosition;

    const spectatorCanJoinPlay = (
      round.status === 'active'
      && round.viewer_role === 'spectator'
      && viewer?.role === 'spectator'
    );
    const availableTees = round.available_tees || [];
    const viewerTrackedFrom = Number(viewer?.tracked_from_position || 1);
    const earlierBackfillable = (round.route || []).filter(
      (route) =>
        route.state !== 'skipped'
        && Number(route.route_position) < viewerTrackedFrom
    );
    const lateBackfillDismissKey = viewer
      ? `wpm_late_backfill_dismissed:${round.id}:${viewer.id}`
      : '';
    const lateBackfillDismissed = Boolean(
      lateBackfillDismissKey
      && window.localStorage.getItem(lateBackfillDismissKey) === '1'
    );
    const showLateBackfill = (
      viewerIsActivePlayer(round)
      && viewingLive
      && earlierBackfillable.length > 0
      && !lateBackfillDismissed
    );
    if (lateBackfillPanel) lateBackfillPanel.hidden = !showLateBackfill;
    if (showLateBackfill && lateBackfillStart) {
      const selected = Number(lateBackfillStart.value || 0);
      lateBackfillStart.replaceChildren();
      earlierBackfillable.forEach((route, index) => {
        const position = Number(route.route_position);
        const option = document.createElement('option');
        option.value = String(position);
        option.textContent =
          `HOLE ${route.hole_number} • ${position} OF ${length}`;
        option.selected = (
          selected
            ? position === selected
            : index === 0
        );
        lateBackfillStart.append(option);
      });
    }

    if (spectatorJoinPlayPanel) {
      spectatorJoinPlayPanel.hidden = !spectatorCanJoinPlay;
    }
    const spectatorNeedsPersonalTee = (
      spectatorCanJoinPlay
      && round.mode === 'individual'
      && availableTees.length > 0
    );
    if (spectatorJoinTeeField) {
      spectatorJoinTeeField.hidden = !spectatorNeedsPersonalTee;
    }
    if (spectatorNeedsPersonalTee) {
      fillTeeSelect(spectatorJoinTeeSelect, availableTees);
    } else if (spectatorJoinTeeSelect) {
      spectatorJoinTeeSelect.replaceChildren();
    }
    if (spectatorJoinPlayButton) {
      spectatorJoinPlayButton.disabled = false;
    }

    if (holeNumber) holeNumber.textContent = String(viewedPhysicalHole);
    if (holeParLabel) {
      holeParLabel.textContent = par ? `PAR ${par}` : 'PAR ?';
    }
    if (holeStateLabel) {
      if (viewedRoute?.state === 'skipped') {
        holeStateLabel.textContent =
          `UNTRACKED HOLE ${viewedPhysicalHole} • ${viewedRoutePosition} OF ${length} • LIVE ${livePhysicalHole}`;
      } else if (viewingLive) {
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

    const missingCurrentScores = missingScoresAtPosition(round, livePosition);
    if (
      advanceWarningPosition !== null
      && (
        Number(advanceWarningPosition) !== livePosition
        || !viewingLive
        || missingCurrentScores.length === 0
      )
    ) {
      advanceWarningPosition = null;
      if (advanceWarningPanel) advanceWarningPanel.hidden = true;
    }
    if (
      advanceWarningPosition !== null
      && Number(advanceWarningPosition) === livePosition
      && advanceWarningCopy
    ) {
      const who = missingCurrentScores.join(', ');
      advanceWarningCopy.textContent =
        `${who} ${missingCurrentScores.length === 1 ? 'IS' : 'ARE'} STILL MISSING. `
        + 'YOU CAN FIX IT NOW OR MOVE ON WITHOUT INVENTING A SCORE.';
      if (advanceWarningPanel) advanceWarningPanel.hidden = false;
    }

    const canOpenRoundSettings = (
      viewerIsActivePlayer(round)
      && round.status === 'active'
    );
    if (roundSettingsButton) {
      roundSettingsButton.hidden = !canOpenRoundSettings;
    }
    if (!canOpenRoundSettings && roundSettingsPanel) {
      roundSettingsPanel.hidden = true;
    }
    if (canOpenRoundSettings) {
      const selectedTee = round.mode === 'scramble'
        ? (round.scramble_tee_name || '')
        : (viewer?.tee_name || '');
      const hasTeeChoices = availableTees.length > 0;

      if (roundSettingsTeeLabel) {
        roundSettingsTeeLabel.textContent = round.mode === 'scramble'
          ? 'TEAM SCORING TEE'
          : 'YOUR TEE';
      }
      if (roundSettingsTeeField) {
        roundSettingsTeeField.hidden = !hasTeeChoices;
      }
      const settingsOpen = roundSettingsPanel && !roundSettingsPanel.hidden;
      if (
        hasTeeChoices
        && (
          !settingsOpen
          || !roundSettingsTeeSelect
          || roundSettingsTeeSelect.options.length === 0
        )
      ) {
        fillTeeSelect(roundSettingsTeeSelect, availableTees, selectedTee);
      }
      if (roundSettingsTeeSave) {
        roundSettingsTeeSave.hidden = !hasTeeChoices;
        roundSettingsTeeSave.disabled = false;
      }

      const parTrackingLocked = (round.scores || []).length > 0;
      if (roundParTrackingPanel) roundParTrackingPanel.hidden = false;
      if (roundParTrackingCopy) {
        roundParTrackingCopy.textContent = parTrackingLocked
          ? 'LOCKED AFTER FIRST FACTUAL SCORE.'
          : (
              round.par_tracking_enabled
                ? 'PAR TRACKING IS ON. YOU CAN TURN IT OFF UNTIL THE FIRST SCORE.'
                : 'PAR TRACKING IS OFF. YOU CAN TURN IT ON UNTIL THE FIRST SCORE.'
            );
      }
      if (roundParTrackingOn) {
        roundParTrackingOn.disabled = (
          parTrackingLocked || Boolean(round.par_tracking_enabled)
        );
      }
      if (roundParTrackingOff) {
        roundParTrackingOff.disabled = (
          parTrackingLocked || !Boolean(round.par_tracking_enabled)
        );
      }

      const showRoundHandicaps = (
        round.mode === 'individual'
        && Boolean(round.net_scoring_enabled)
      );
      if (roundHandicapPanel) {
        roundHandicapPanel.hidden = !showRoundHandicaps;
      }
      if (showRoundHandicaps) {
        renderRoundHandicapEditor(roundHandicapList, round);
      } else if (roundHandicapList) {
        roundHandicapList.replaceChildren();
      }

      const activePlayerCount = (round.participants || []).filter(
        (participant) =>
          participant.role === 'player'
          && participant.participation_state === 'active'
      ).length;
      const canAddOffline = activePlayerCount < 4;
      if (offlinePlayerPanel) offlinePlayerPanel.hidden = !canAddOffline;
      const offlineNeedsTee = (
        canAddOffline
        && round.mode === 'individual'
        && hasTeeChoices
      );
      if (offlinePlayerTeeField) {
        offlinePlayerTeeField.hidden = !offlineNeedsTee;
      }
      if (
        offlineNeedsTee
        && (
          !settingsOpen
          || !offlinePlayerTeeSelect
          || offlinePlayerTeeSelect.options.length === 0
        )
      ) {
        fillTeeSelect(offlinePlayerTeeSelect, availableTees);
      }
      if (offlinePlayerAdd) offlinePlayerAdd.disabled = false;

      const claimUndo = round.claim_undo;
      const canUndoClaim = Boolean(claimUndo?.available);
      if (claimUndoPanel) claimUndoPanel.hidden = !canUndoClaim;
      if (!canUndoClaim) {
        claimUndoConfirmPending = false;
      } else {
        const actions = Number(claimUndo.actions_after_claim || 0);
        if (claimUndoCopy) {
          claimUndoCopy.textContent = actions > 0
            ? `${actions} ACTION${actions === 1 ? '' : 'S'} HAPPENED AFTER YOU CLAIMED THIS PLAYER. THOSE RECEIPTS STAY ATTRIBUTED TO YOUR ACCOUNT.`
            : 'UNDOING THE CLAIM PUTS THIS PLAYER BACK INTO ROUND-ONLY MODE.';
        }
        if (claimUndoButton) {
          claimUndoButton.disabled = false;
          claimUndoButton.textContent = (
            claimUndoConfirmPending && actions > 0
              ? 'UNDO ANYWAY'
              : 'UNDO PLAYER CLAIM'
          );
        }
      }
    }

    const canEditViewedHole = (
      viewerIsActivePlayer(round)
      && viewedRoute?.state !== 'skipped'
      && !viewingFuture
      && round.status === 'active'
    );
    const needsPar = (
      Boolean(round.par_tracking_enabled)
      && viewedRoute?.state !== 'skipped'
      && !par
    );
    const showParEditor = (
      canEditViewedHole
      && Boolean(round.par_tracking_enabled)
      && (needsPar || parEditorOpen)
    );

    if (parForm) {
      parForm.hidden = !showParEditor;
    }
    if (parInput) {
      parInput.value = par ? String(par) : '';
      parInput.disabled = !canEditViewedHole;
    }
    if (parSubmit) {
      parSubmit.textContent = par ? 'SAVE PAR' : 'SET PAR';
      parSubmit.disabled = !canEditViewedHole;
    }
    if (liveEditPar) {
      liveEditPar.hidden = (
        !canEditViewedHole
        || !Boolean(round.par_tracking_enabled)
        || viewedRoute?.state === 'skipped'
      );
      liveEditPar.textContent = par ? ('EDIT PAR • ' + par) : 'SET PAR';
    }

    renderLiveHoleSelector(round, viewedRoutePosition, livePosition);
    renderLiveBanter(round);
    renderScoreCard(round, viewedRoutePosition);
    renderScrambleContributions(round, viewedRoutePosition);
    renderLiveHoleStats(round, viewedRoutePosition);
    renderLatestPresentation(round);
    renderReceipts(round);

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

    const endEarly = round.end_early || {};
    const canVoteEndEarly = viewerIsActivePlayer(round);
    const proposalActive = Boolean(endEarly.proposal_active);
    if (endEarlyButton) {
      endEarlyButton.hidden = !canVoteEndEarly || proposalActive;
      endEarlyButton.disabled = false;
    }
    if (endEarlyPanel) {
      endEarlyPanel.hidden = !canVoteEndEarly || !proposalActive;
    }
    if (proposalActive && canVoteEndEarly) {
      const eligible = endEarly.eligible || [];
      const required = Number(endEarly.required_count || eligible.length || 0);
      const yes = Number(endEarly.yes_count || 0);
      if (endEarlyCopy) {
        endEarlyCopy.textContent =
          `${yes} OF ${required} CONNECTED GOLFER${required === 1 ? '' : 'S'} HAVE AGREED.`;
      }
      if (endEarlyVoters) {
        endEarlyVoters.replaceChildren();
        eligible.forEach((row) => {
          const item = document.createElement('div');
          item.className = 'end-early-voter';

          const name = document.createElement('span');
          name.textContent = row.display_name || 'Golfer';

          const vote = document.createElement('strong');
          vote.textContent = row.vote === true
            ? 'YES'
            : (row.vote === false ? 'NO' : 'WAITING');

          item.append(name, vote);
          endEarlyVoters.append(item);
        });
      }
      if (endEarlyYes) endEarlyYes.disabled = false;
      if (endEarlyNo) endEarlyNo.disabled = false;
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
        viewedRoute?.state === 'skipped'
          ? 'This hole was deliberately left untracked.'
          : (viewingFuture ? 'Future holes are preview-only.' : '')
      );
    }
  };

  const renderLobby = (round) => {
    currentLobbyRound = round;
    viewedRoutePosition = null;
    stopUserHeckle('roundSetup', { hide: true });
    if (roundSetupHeckle) {
      roundSetupHeckle.hidden = true;
      roundSetupHeckle.classList.add('is-panel-hidden');
    }
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
      const teamTee = round.mode === 'scramble' && round.scramble_tee_name
        ? ` • TEAM TEE: ${round.scramble_tee_name}`
        : '';
      lobbySummary.textContent =
        `${modeLabel} • ${round.hole_count} HOLES • ${place}${teamTee}`;
    }

    if (lobbyParticipants) {
      lobbyParticipants.replaceChildren();
      (round.participants || []).forEach((participant) => {
        const row = document.createElement('div');
        row.className = 'lobby-person';

        const name = document.createElement('span');
        name.textContent = participant.display_name || 'Unknown golfer';

        const role = document.createElement('small');
        const tee = (
          round.mode === 'individual' && participant.tee_name
            ? ` • ${participant.tee_name} TEE`
            : ''
        );
        const offline = participant.round_only ? ' • OFFLINE' : '';
        role.textContent = `${participant.role || 'player'}${offline}${tee}`;

        row.append(name, role);
        lobbyParticipants.append(row);
      });
    }

    renderLobbyBanter(round);
    void startLobbyBanterRotation(round);

    const parsByPosition = new Map(
      (round.pars || []).map((row) => [
        Number(row.route_position),
        Number(row.par),
      ])
    );
    const parSetupNow = (
      round.par_tracking_enabled
      && String(window.localStorage.getItem(PAR_SETUP_NOW_KEY) || '')
        === String(round.id)
    );
    const plannedRoute = (round.route || []).filter(
      (route) => route.state !== 'skipped'
    );
    const missingParPositions = plannedRoute.filter(
      (route) => !parsByPosition.has(Number(route.route_position))
    );

    if (lobbyParSetup) lobbyParSetup.hidden = !parSetupNow;
    if (lobbyParGrid) {
      lobbyParGrid.replaceChildren();
      if (parSetupNow) {
        plannedRoute.forEach((route) => {
          const position = Number(route.route_position);
          const row = document.createElement('label');
          row.className = 'lobby-par-row';

          const label = document.createElement('span');
          label.textContent =
            `HOLE ${route.hole_number} • ${position} OF ${routeLength(round)}`;

          const input = document.createElement('input');
          input.type = 'number';
          input.min = '2';
          input.max = '7';
          input.inputMode = 'numeric';
          input.dataset.routePosition = String(position);
          input.value = parsByPosition.has(position)
            ? String(parsByPosition.get(position))
            : '';
          input.placeholder = 'PAR';

          row.append(label, input);
          lobbyParGrid.append(row);
        });
      }
    }
    if (lobbyParSave) {
      lobbyParSave.hidden = !parSetupNow;
      lobbyParSave.disabled = false;
    }

    if (lobbyStart) {
      const canStart = round.viewer_role === 'player' && round.status === 'setup';
      const missingRequiredPars = parSetupNow && missingParPositions.length > 0;
      lobbyStart.hidden = !canStart;
      lobbyStart.disabled = missingRequiredPars;
      if (canStart && missingRequiredPars) {
        setRoundFlowMessage('Finish entering pars before starting.');
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

  startRoundForm?.querySelectorAll('input[name="mode"]').forEach((radio) => {
    radio.addEventListener('change', refreshStartModeControls);
  });

  startRoundForm?.querySelectorAll(
    'input[name="holes"], input[name="course_hole_count"]'
  ).forEach((control) => {
    control.addEventListener('change', renderRoutePreview);
  });
  startHoleInput?.addEventListener('input', renderRoutePreview);
  trackingStartPosition?.addEventListener('change', renderRoutePreview);

  setupNextButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const target = Number(button.dataset.setupNext);
      if (target === 3) {
        const courseMode = startRoundForm?.querySelector(
          'input[name="course_mode"]:checked'
        )?.value || 'course';
        if (courseMode === 'course' && !selectedCourse?.id) {
          setCourseStepMessage('Pick a course first, or switch to Free Play.');
          courseSearchInput?.focus();
          return;
        }
      }
      setCourseStepMessage('');
      setSetupStep(target);
    });
  });
  setupBackButtons.forEach((button) => {
    button.addEventListener('click', () => setSetupStep(button.dataset.setupBack));
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
    const values = new FormData(startRoundForm);
    setFormBusy(startRoundForm, true);

    try {
      const courseMode = values.get('course_mode');
      if (courseMode === 'course' && !selectedCourse?.id) {
        throw new Error('Pick a course first, or switch to Free Play.');
      }

      const holes = Number(values.get('holes'));
      const startHole = Number(values.get('start_hole') || 1);
      const physicalCount = selectedPhysicalHoleCount();
      if (!Number.isInteger(startHole) || startHole < 1 || startHole > physicalCount) {
        throw new Error(`Starting hole must be between 1 and ${physicalCount}.`);
      }

      const parSetup = String(values.get('par_setup') || 'as_go');
      const trackingStart = Number(
        values.get('tracking_start_position') || 1
      );
      const priorMode = String(
        values.get('prior_holes_mode') || 'untracked'
      );
      const mode = String(values.get('mode') || 'individual');
      const individualScoring = String(
        values.get('individual_scoring') || 'gross'
      );
      const body = {
        mode,
        holes,
        start_hole: startHole,
        par_tracking_enabled: parSetup !== 'off',
        tracking_start_position: trackingStart,
        prior_holes_mode: priorMode,
        net_scoring_enabled: (
          mode === 'individual'
          && individualScoring === 'net'
        ),
      };

      if (courseMode === 'course') {
        body.course_id = selectedCourse.id;
        if (startTeeSelect?.value) body.tee_name = startTeeSelect.value;
      } else {
        body.free_play_name =
          String(values.get('free_play_name') || '').trim() || 'Free Play';
        body.course_hole_count = holes;
      }

      const created = await requestJson('/api/rounds', {
        method: 'POST',
        body,
      });
      if (parSetup === 'now') {
        window.localStorage.setItem(PAR_SETUP_NOW_KEY, String(created.id));
      } else {
        window.localStorage.removeItem(PAR_SETUP_NOW_KEY);
      }
      await refreshLobby(created.active_code);
      startLobbyPolling(created.active_code);
      startRoundForm.reset();
      refreshStartModeControls();
      renderRoutePreview();
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      setFormBusy(startRoundForm, false);
    }
  });

  const enterJoinedRound = async (code) => {
    await refreshLobby(code);
    startLobbyPolling(code);
    joinRoundForm?.reset();
    resetClaimPlayerPanel();
  };

  const joinAsNewParticipant = async (code, role, teeName = '') => {
    await requestJson('/api/rounds/join', {
      method: 'POST',
      body: {
        code,
        role,
        tee_name: teeName || null,
      },
    });
    await enterJoinedRound(code);
  };

  const prepareJoinTeeChoice = (payload, code, role = 'player') => {
    const tees = payload?.available_tees || [];
    const needsTee = (
      role === 'player'
      && payload?.mode === 'individual'
      && tees.length > 0
    );
    if (!needsTee || !joinTeeField || !joinTeeSelect) return false;

    pendingJoinPreview = { code, role, payload };
    fillTeeSelect(joinTeeSelect, tees);
    joinTeeField.hidden = false;
    if (joinRoundSubmit) {
      joinRoundSubmit.hidden = false;
      joinRoundSubmit.textContent = 'JOIN THE LOBBY';
    }
    joinTeeSelect.focus();
    return true;
  };

  const showClaimablePlayers = (payload, code) => {
    const players = payload?.players || [];
    if (!claimPlayerPanel || !claimPlayerList || !players.length) return false;

    pendingClaimJoin = {
      code,
      roundId: payload.round_id,
      role: 'player',
      preview: payload,
    };
    claimPlayerList.replaceChildren();

    players.forEach((player) => {
      const row = document.createElement('div');
      row.className = 'claim-player-row';

      const copy = document.createElement('span');
      const tee = player.tee_name ? ` • ${player.tee_name} TEE` : '';
      copy.textContent =
        `${player.display_name || 'Unknown golfer'}${tee}`;

      const claim = document.createElement('button');
      claim.type = 'button';
      claim.textContent = "THAT'S ME";
      claim.addEventListener('click', async () => {
        setFormBusy(joinRoundForm, true);
        setRoundFlowMessage('');
        try {
          await requestJson(
            `/api/rounds/${payload.round_id}/claim-player`,
            {
              method: 'PATCH',
              body: { participant_id: player.participant_id },
            }
          );
          await enterJoinedRound(code);
        } catch (error) {
          setRoundFlowMessage(error.message);
        } finally {
          setFormBusy(joinRoundForm, false);
        }
      });

      row.append(copy, claim);
      claimPlayerList.append(row);
    });

    claimPlayerPanel.hidden = false;
    if (joinRoundSubmit) joinRoundSubmit.hidden = true;
    return true;
  };

  joinRoundForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setRoundFlowMessage('');
    const values = new FormData(joinRoundForm);
    setFormBusy(joinRoundForm, true);
    const code = String(values.get('code') || '').trim();
    const role = String(values.get('role') || 'player');

    try {
      const teeChoiceReady = (
        role === 'player'
        && pendingJoinPreview?.code === code
        && joinTeeField
        && !joinTeeField.hidden
      );
      if (teeChoiceReady) {
        const teeName = String(joinTeeSelect?.value || '').trim();
        if (!teeName) {
          throw new Error('Pick your tee before entering the lobby.');
        }
        await joinAsNewParticipant(code, role, teeName);
        return;
      }

      if (role === 'player') {
        const claimable = await requestJson(
          `/api/rounds/code/${encodeURIComponent(code)}/claimable-players`
        );
        if (showClaimablePlayers(claimable, code)) return;
        if (prepareJoinTeeChoice(claimable, code, role)) return;
      }

      await joinAsNewParticipant(code, role);
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      setFormBusy(joinRoundForm, false);
    }
  });

  claimPlayerNone?.addEventListener('click', async () => {
    if (!pendingClaimJoin) return;
    const { code, role, preview } = pendingClaimJoin;
    setRoundFlowMessage('');
    if (claimPlayerPanel) claimPlayerPanel.hidden = true;
    if (claimPlayerList) claimPlayerList.replaceChildren();

    if (prepareJoinTeeChoice(preview, code, role)) {
      return;
    }

    setFormBusy(joinRoundForm, true);
    try {
      await joinAsNewParticipant(code, role);
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      setFormBusy(joinRoundForm, false);
    }
  });

  lobbyParSave?.addEventListener('click', async () => {
    if (!currentLobbyRound || !lobbyParGrid) return;

    const inputs = [...lobbyParGrid.querySelectorAll('input[data-route-position]')];
    const rows = inputs.map((input) => ({
      input,
      position: Number(input.dataset.routePosition),
      par: Number(input.value),
    }));
    const invalid = rows.find(
      (row) => !Number.isInteger(row.par) || row.par < 2 || row.par > 7
    );
    if (invalid) {
      invalid.input.focus();
      setRoundFlowMessage('Every par must be between 2 and 7.');
      return;
    }

    lobbyParSave.disabled = true;
    setRoundFlowMessage('Saving pars...');
    try {
      for (const row of rows) {
        await requestJson(
          `/api/rounds/${currentLobbyRound.id}/positions/${row.position}/par`,
          {
            method: 'PUT',
            body: { par: row.par },
          }
        );
      }
      window.localStorage.removeItem(PAR_SETUP_NOW_KEY);
      await refreshLobby(currentLobbyRound.active_code);
      setRoundFlowMessage('');
    } catch (error) {
      setRoundFlowMessage(error.message);
      lobbyParSave.disabled = false;
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

  spectatorJoinPlayButton?.addEventListener('click', async () => {
    if (!currentLobbyRound || currentLobbyRound.viewer_role !== 'spectator') return;

    const tees = currentLobbyRound.available_tees || [];
    const teeName = spectatorJoinTeeSelect?.value || '';
    if (
      currentLobbyRound.mode === 'individual'
      && tees.length
      && !teeName
    ) {
      setRoundFlowMessage('Pick a tee before joining the round.');
      return;
    }

    spectatorJoinPlayButton.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/join-play`,
        {
          method: 'PATCH',
          body: {
            tee_name: teeName || null,
          },
        }
      );
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      spectatorJoinPlayButton.disabled = false;
    }
  });

  const dismissLateBackfillPrompt = () => {
    if (!currentLobbyRound) return;
    const viewer = viewerParticipant(currentLobbyRound);
    if (!viewer) return;
    window.localStorage.setItem(
      `wpm_late_backfill_dismissed:${currentLobbyRound.id}:${viewer.id}`,
      '1'
    );
    if (lateBackfillPanel) lateBackfillPanel.hidden = true;
  };

  lateBackfillGo?.addEventListener('click', () => {
    if (!currentLobbyRound) return;
    const position = Number(lateBackfillStart?.value || 0);
    if (!Number.isInteger(position) || position < 1) return;

    dismissLateBackfillPrompt();
    viewedRoutePosition = position;
    renderLiveRound(currentLobbyRound);
    setRoundFlowMessage(
      'BACKFILLING OLD DAMAGE. USE BACK TO LIVE WHEN YOU ARE DONE.'
    );
  });

  lateBackfillDismiss?.addEventListener('click', () => {
    dismissLateBackfillPrompt();
  });

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

  const castEndEarlyVote = async (vote) => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) return;

    if (endEarlyButton) endEarlyButton.disabled = true;
    if (endEarlyYes) endEarlyYes.disabled = true;
    if (endEarlyNo) endEarlyNo.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/end-early-vote`,
        {
          method: 'PATCH',
          body: { vote: Boolean(vote) },
        }
      );
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      if (endEarlyButton) endEarlyButton.disabled = false;
      if (endEarlyYes) endEarlyYes.disabled = false;
      if (endEarlyNo) endEarlyNo.disabled = false;
    }
  };

  endEarlyButton?.addEventListener('click', async () => {
    await castEndEarlyVote(true);
  });

  endEarlyYes?.addEventListener('click', async () => {
    await castEndEarlyVote(true);
  });

  endEarlyNo?.addEventListener('click', async () => {
    await castEndEarlyVote(false);
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
    parEditorOpen = false;
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

    parEditorOpen = false;
    viewedRoutePosition = viewed + 1;
    renderLiveRound(currentLobbyRound);
  });

  const advanceSharedLiveHole = async () => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) return;

    const length = routeLength(currentLobbyRound);
    const livePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    if (livePosition >= length) return;

    if (advanceLiveHole) advanceLiveHole.disabled = true;
    if (advanceWarningGo) advanceWarningGo.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/current-hole`,
        {
          method: 'PATCH',
          body: { route_position: livePosition + 1 },
        }
      );
      advanceWarningPosition = null;
      if (advanceWarningPanel) advanceWarningPanel.hidden = true;
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      if (advanceLiveHole) advanceLiveHole.disabled = false;
      if (advanceWarningGo) advanceWarningGo.disabled = false;
    }
  };

  advanceLiveHole?.addEventListener('click', async () => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) return;

    const livePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    const missing = missingScoresAtPosition(currentLobbyRound, livePosition);
    if (missing.length) {
      advanceWarningPosition = livePosition;
      if (advanceWarningCopy) {
        const who = missing.join(', ');
        advanceWarningCopy.textContent =
          `${who} ${missing.length === 1 ? 'IS' : 'ARE'} STILL MISSING. `
          + 'YOU CAN FIX IT NOW OR MOVE ON WITHOUT INVENTING A SCORE.';
      }
      if (advanceWarningPanel) advanceWarningPanel.hidden = false;
      return;
    }

    await advanceSharedLiveHole();
  });

  advanceWarningFix?.addEventListener('click', () => {
    advanceWarningPosition = null;
    if (advanceWarningPanel) advanceWarningPanel.hidden = true;
    if (!currentLobbyRound) return;
    viewedRoutePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    renderLiveRound(currentLobbyRound);
    liveScoreArea?.querySelector('input:not([disabled])')?.focus();
  });

  advanceWarningGo?.addEventListener('click', advanceSharedLiveHole);

  roundSettingsButton?.addEventListener('click', () => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) return;
    if (roundSettingsPanel) roundSettingsPanel.hidden = false;
    roundSettingsTeeSelect?.focus();
  });

  roundSettingsClose?.addEventListener('click', () => {
    if (roundSettingsPanel) roundSettingsPanel.hidden = true;
  });

  roundSettingsTeeSave?.addEventListener('click', async () => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) return;
    const teeName = String(roundSettingsTeeSelect?.value || '').trim();
    if (!teeName) return;

    roundSettingsTeeSave.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/tee`,
        {
          method: 'PATCH',
          body: { tee_name: teeName },
        }
      );
      if (roundSettingsPanel) roundSettingsPanel.hidden = true;
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      roundSettingsTeeSave.disabled = false;
    }
  });

  const setRoundParTrackingMode = async (enabled) => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) return;

    if (roundParTrackingOn) roundParTrackingOn.disabled = true;
    if (roundParTrackingOff) roundParTrackingOff.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/par-tracking`,
        {
          method: 'PATCH',
          body: { enabled: Boolean(enabled) },
        }
      );
      pendingScoreAfterPar = null;
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      if (roundParTrackingOn) roundParTrackingOn.disabled = false;
      if (roundParTrackingOff) roundParTrackingOff.disabled = false;
    }
  };

  roundParTrackingOn?.addEventListener('click', async () => {
    await setRoundParTrackingMode(true);
  });

  roundParTrackingOff?.addEventListener('click', async () => {
    await setRoundParTrackingMode(false);
  });

  offlinePlayerAdd?.addEventListener('click', async () => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) return;

    const displayName = String(offlinePlayerName?.value || '').trim();
    if (!displayName) {
      setRoundFlowMessage('Give the offline golfer a name first.');
      offlinePlayerName?.focus();
      return;
    }

    const tees = currentLobbyRound.available_tees || [];
    const teeName = String(offlinePlayerTeeSelect?.value || '').trim();
    if (
      currentLobbyRound.mode === 'individual'
      && tees.length
      && !teeName
    ) {
      setRoundFlowMessage('Pick a tee for the offline golfer.');
      offlinePlayerTeeSelect?.focus();
      return;
    }

    offlinePlayerAdd.disabled = true;
    setRoundFlowMessage('');
    try {
      await requestJson(
        `/api/rounds/${currentLobbyRound.id}/round-only-players`,
        {
          method: 'POST',
          body: {
            display_name: displayName,
            tee_name: teeName || null,
          },
        }
      );
      if (offlinePlayerName) offlinePlayerName.value = '';
      if (roundSettingsPanel) roundSettingsPanel.hidden = true;
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
      offlinePlayerAdd.disabled = false;
    }
  });

  claimUndoButton?.addEventListener('click', async () => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) return;

    const state = currentLobbyRound.claim_undo;
    if (!state?.available) return;
    const actions = Number(state.actions_after_claim || 0);

    if (actions > 0 && !claimUndoConfirmPending) {
      claimUndoConfirmPending = true;
      renderLiveRound(currentLobbyRound);
      return;
    }

    claimUndoButton.disabled = true;
    setRoundFlowMessage('');
    try {
      const result = await requestJson(
        `/api/rounds/${currentLobbyRound.id}/claim-player/undo`,
        {
          method: 'PATCH',
          body: {
            confirm_actor_history: (
              claimUndoConfirmPending || actions === 0
            ),
          },
        }
      );

      if (result.requires_confirmation && !result.undone) {
        claimUndoConfirmPending = true;
        currentLobbyRound.claim_undo = result;
        renderLiveRound(currentLobbyRound);
        return;
      }

      claimUndoConfirmPending = false;
      closeRoundFlow();
    } catch (error) {
      setRoundFlowMessage(error.message);
      claimUndoButton.disabled = false;
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

      const pending = (
        pendingScoreAfterPar
        && String(pendingScoreAfterPar.roundId) === String(currentLobbyRound.id)
        && Number(pendingScoreAfterPar.position) === Number(viewedRoutePosition)
      )
        ? pendingScoreAfterPar
        : null;

      if (pending) {
        const body = { strokes: pending.strokes };
        if (currentLobbyRound.mode === 'individual') {
          body.player_participant_id = pending.participantId;
        }
        await requestJson(
          `/api/rounds/${currentLobbyRound.id}/positions/${pending.position}/score`,
          {
            method: 'PUT',
            body,
          }
        );
        pendingScoreAfterPar = null;
      }

      parEditorOpen = false;
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

  liveBanterForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!currentLobbyRound) return;
    const message = String(liveBanterInput?.value || '').trim();
    if (!message) return;

    if (liveBanterSend) liveBanterSend.disabled = true;
    setRoundFlowMessage('');
    try {
      await sendSocialEvent('open_mic', { message });
      if (liveBanterInput) liveBanterInput.value = '';
      await refreshRound(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      if (liveBanterSend) liveBanterSend.disabled = false;
    }
  });

  liveNavPlay?.addEventListener('click', () => {
    if (liveMorePanel) liveMorePanel.hidden = true;
    setLiveNavActive(liveNavPlay);
    liveRoundPanel?.scrollTo({ top: 0, behavior: 'smooth' });
  });

  liveNavScorecard?.addEventListener('click', () => {
    if (liveMorePanel) liveMorePanel.hidden = true;
    setLiveNavActive(liveNavScorecard);
    liveScoreArea?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  liveNavStats?.addEventListener('click', () => {
    if (liveMorePanel) liveMorePanel.hidden = true;
    setLiveNavActive(liveNavStats);
    liveHoleStats?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  liveNavMore?.addEventListener('click', () => {
    if (!liveMorePanel) return;
    const opening = liveMorePanel.hidden;
    liveMorePanel.hidden = !opening;
    setLiveNavActive(opening ? liveNavMore : liveNavPlay);
    if (opening) {
      liveMorePanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  liveEditPar?.addEventListener('click', () => {
    if (!currentLobbyRound || viewedRoutePosition === null) return;
    parEditorOpen = true;
    if (liveMorePanel) liveMorePanel.hidden = true;
    setLiveNavActive(liveNavPlay);
    renderLiveRound(currentLobbyRound);
    window.requestAnimationFrame(() => {
      parInput?.focus();
      parForm?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

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


  const openSettings = async () => {
    if (!settingsModal || !settingsForm) return;
    setSettingsMessage('');
    settingsModal.hidden = false;
    document.body.classList.add('modal-open');

    try {
      const [preferences, account] = await Promise.all([
        requestJson('/api/preferences'),
        requestJson('/api/auth/me'),
      ]);
      populateSettings(preferences);
      populateProfileHandicap(account);
      settingsClose?.focus();
    } catch (error) {
      setSettingsMessage(error.message);
    }
  };

  const closeSettings = () => {
    if (!settingsModal) return;
    settingsModal.hidden = true;
    document.body.classList.remove('modal-open');
    if (sessionToken()) {
      void startUserHeckles(
        'home',
        'home.idle',
        () => (
          Boolean(appShell?.getAttribute('aria-hidden') !== 'true')
          && Boolean(roundFlowModal?.hidden)
          && Boolean(settingsModal?.hidden)
          && Boolean(installOnboardingModal?.hidden)
        ),
      );
    }
  };

  colorThemeTease?.addEventListener('click', () => {
    const messages = [
      'STFU, snowflake. You get the color I chose. Stop being needy.',
      'COLOR THEME? ABSOLUTELY. IT\'S GREEN. YOU\'RE WELCOME.',
      'THE THEME IS BAD GOLF GREEN. THIS IS NOT A HOME MAKEOVER SHOW.',
      'YOU GET GREEN, CREAM, ORANGE, AND THE PRIVILEGE OF COMPLAINING ABOUT IT.',
      'CUSTOM COLORS COST EXTRA. PAYMENT ACCEPTED IN BIRDIES. YOU HAVE NONE.',
    ];
    setSettingsMessage(
      messages[Math.floor(Math.random() * messages.length)]
    );
  });

  settingsOpenButtons.forEach((button) => {
    button.addEventListener('click', openSettings);
  });
  settingsClose?.addEventListener('click', closeSettings);
  settingsModal?.addEventListener('click', (event) => {
    if (event.target === settingsModal) closeSettings();
  });

  settingsForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setSettingsMessage('');

    const checkedVulgarity = settingsForm.querySelector(
      'input[name="max_vulgarity"]:checked'
    );
    const patch = {
      mini_mascots_enabled:
        settingsForm.elements.mini_mascots_enabled.checked,
      trash_talk_enabled:
        settingsForm.elements.trash_talk_enabled.checked,
      max_vulgarity: checkedVulgarity?.value || 'brutal',
      themes: {
        drinking: settingsForm.elements.drinking.checked,
        wife: settingsForm.elements.wife.checked,
      },
    };
    const rawHandicapIndex = String(
      settingsHandicapIndex?.value || ''
    ).trim();
    const handicapIndex = rawHandicapIndex === ''
      ? null
      : Number(rawHandicapIndex);
    if (
      handicapIndex !== null
      && (
        !Number.isFinite(handicapIndex)
        || handicapIndex < -10
        || handicapIndex > 54
      )
    ) {
      setSettingsMessage('Handicap Index must be between -10.0 and 54.0.');
      settingsHandicapIndex?.focus();
      return;
    }

    setFormBusy(settingsForm, true);

    try {
      const preferences = await requestJson('/api/preferences', {
        method: 'PATCH',
        body: patch,
      });
      const account = await requestJson('/api/profile/handicap', {
        method: 'PATCH',
        body: { handicap_index: handicapIndex },
      });
      populateSettings(preferences);
      populateProfileHandicap(account);
      userMessageCache.clear();
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
