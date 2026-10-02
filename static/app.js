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
  const settingsSpouseType = document.getElementById('settings-spouse-type');
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
  const joinRoundHeckle = document.getElementById('join-round-heckle');
  const joinRoundHeckleText = document.getElementById('join-round-heckle-text');
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
  const joinRoundCode = document.getElementById('join-round-code');
  const joinCodeDigits = [...document.querySelectorAll('[data-join-code-digit]')];
  const joinRoundSubmit = document.getElementById('join-round-submit');
  const unfinishedRoundsPanel = document.getElementById('unfinished-rounds-panel');
  const unfinishedRoundsList = document.getElementById('unfinished-rounds-list');
  const joinCtaDock = document.getElementById('join-cta-dock');
  const joinCtaMiniStage = document.getElementById('join-cta-mini-stage');
  const joinCtaMini = document.getElementById('join-cta-mini');
  const joinTeeField = document.getElementById('join-tee-field');
  const joinTeeSelect = document.getElementById('join-tee-select');
  const inviteJoinBanner = document.getElementById('invite-join-banner');
  const inviteJoinTitle = document.getElementById('invite-join-title');
  const inviteJoinCopy = document.getElementById('invite-join-copy');
  const roundInviteButtons = [...document.querySelectorAll('[data-invite-role]')];
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
  const courseLayoutFieldset = document.getElementById('course-layout-fieldset');
  const courseLayoutHint = document.getElementById('course-layout-hint');
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
  const routePreview = document.getElementById('route-preview');
  const setupParTracking = document.getElementById('setup-par-tracking');
  const lobbyParSetup = document.getElementById('lobby-par-setup');
  const lobbyParGrid = document.getElementById('lobby-par-grid');
  const lobbyParSave = document.getElementById('lobby-par-save');
  const lobbyHandicapPanel = document.getElementById('lobby-handicap-panel');
  const lobbyHandicapList = document.getElementById('lobby-handicap-list');
  const liveRoundPanel = document.getElementById('live-round-panel');
  const liveRoundPlace = document.getElementById('live-round-place');
  const scoreAnnouncement = document.getElementById('score-announcement');
  const scoreAnnouncementText = document.getElementById('score-announcement-text');
  const holeTransition = document.getElementById('hole-transition');
  const holeTransitionMascot = document.getElementById('hole-transition-mascot');
  const holeTransitionLabel = document.getElementById('hole-transition-label');
  const holeTransitionResult = document.getElementById('hole-transition-result');
  const holeTransitionContinue = document.getElementById('hole-transition-continue');
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
  const liveBanterPanel = document.getElementById('live-banter-panel');
  const liveBanterExpand = document.getElementById('live-banter-expand');
  const liveCalloutButton = document.getElementById('live-callout-button');
  const scrambleContributionOpen = document.getElementById('scramble-contribution-open');
  const liveHoleStats = document.getElementById('live-hole-stats');
  const liveMorePanel = document.getElementById('live-more-panel');
  const liveNavMore = document.getElementById('live-nav-more');
  const latestPresentation = document.getElementById('latest-presentation');
  const latestMascot = document.getElementById('latest-mascot');
  const latestBanter = document.getElementById('latest-banter');
  const latestFallback = document.getElementById('latest-fallback');
  const scrambleContributionPanel = document.getElementById('scramble-contribution-panel');
  const scrambleContributionList = document.getElementById('scramble-contribution-list');
  const scrambleContributionSkip = document.getElementById('scramble-contribution-skip');
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
  const roundHistoryOpenButtons = [
    ...document.querySelectorAll('[data-round-history-open]')
  ];
  const receiptsUnseenBadges = [
    ...document.querySelectorAll('[data-receipts-unseen-badge]')
  ];
  const roundHistoryPage = document.getElementById('round-history-page');
  const roundHistoryBack = document.getElementById('round-history-back');
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
  const scoreResponseModal = document.getElementById('score-response-modal');
  const scoreResponseClose = document.getElementById('score-response-close');
  const scoreResponseContext = document.getElementById('score-response-context');
  const scoreResponseSheetBody = document.getElementById('score-response-sheet-body');

  const modal = document.getElementById('construction-modal');
  const modalClose = document.getElementById('construction-close');
  const underConstructionButtons = document.querySelectorAll('[data-under-construction]');

  let pendingAccount = null;
  let currentLobbyRound = null;
  let roundHistoryOpen = false;
  let selectedCourse = null;
  let lobbyRefreshTimer = null;
  let viewedRoutePosition = null;
  let currentBagAction = null;
  let currentBagReplyToEventId = null;
  let currentBagRoutePosition = null;
  let currentBagLockedTargetId = null;
  let openScoreResponseEventId = '';
  let scrambleContributionComposerOpen = false;
  let finishIncompletePending = false;
  let advanceWarningPosition = null;
  let pendingScoreAfterPar = null;
  let parEditorOpen = false;
  let skippedScrambleContributionPromptKey = '';
  let scoreAnnouncementRoundId = '';
  let seenScoreAnnouncementEventIds = new Set();
  let scoreAnnouncementQueue = [];
  let scoreAnnouncementTimer = null;
  let holeTransitionTimer = null;
  let transitionAssetsPromise = null;
  let pendingClaimJoin = null;
  let pendingJoinPreview = null;
  let pendingRoundInvitePreview = null;
  let roundInviteProcessing = false;
  const invitePathMatch = window.location.pathname.match(
    /^\/invite\/([^/]+)\/?$/
  );
  let pendingRoundInviteToken = '';
  if (invitePathMatch) {
    try {
      pendingRoundInviteToken = decodeURIComponent(invitePathMatch[1]);
    } catch (_error) {
      pendingRoundInviteToken = '';
    }
  }
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
  const LOBBY_BANTER_ROTATE_MS = 10000;

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

  };

  const populateProfileRelationship = (preferences) => {
    if (!settingsSpouseType) return;
    settingsSpouseType.value = String(preferences?.spouse_type || '');
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
    const spouseType = String(values.get('spouse_type') || '').trim();

    if (displayName.length < 1 || displayName.length > 20) {
      return new Error('display_name must be between 1 and 20 characters');
    }
    if (!/^[a-z0-9][a-z0-9_.-]{2,15}$/.test(username)) {
      return new Error(
        'username must be 3-16 characters using letters, numbers, ., _, or -'
      );
    }
    if (!['wife', 'husband', 'not_married'].includes(spouseType)) {
      return new Error('spouse_type must be wife, husband, or not_married');
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
      roundJoin: joinRoundHeckle,
      install: installOnboardingHeckle,
    }[name];
    if (hide && target) target.hidden = true;
  };

  const userHeckleTarget = (name) => ({
    home: { container: homeHeckle, text: homeHeckleText },
    roundSetup: { container: roundSetupHeckle, text: roundSetupHeckleText },
    roundJoin: { container: joinRoundHeckle, text: joinRoundHeckleText },
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

    if (pendingRoundInviteToken) {
      window.setTimeout(() => {
        void processPendingRoundInvite();
      }, 0);
    } else {
      window.setTimeout(() => maybeShowInstallOnboarding(account), 0);
    }
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
      if (pendingRoundInviteToken) {
        setAuthMessage('ROUND INVITE WAITING. SIGN IN OR CREATE AN ACCOUNT.');
      }
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

  const alignJoinMiniToButton = () => {
    if (
      !joinCtaMiniStage
      || !joinCtaMini
      || !joinRoundSubmit
      || joinCtaMiniStage.hidden
      || !joinCtaMini.complete
      || !joinCtaMini.naturalHeight
    ) return;

    joinCtaMiniStage.style.setProperty('--join-mini-y', '0px');

    window.requestAnimationFrame(() => {
      if (joinCtaMiniStage.hidden) return;
      const miniRect = joinCtaMini.getBoundingClientRect();
      const buttonRect = joinRoundSubmit.getBoundingClientRect();
      const transparentBottom =
        setupMiniOpaqueBottomRatio(joinCtaMini) * miniRect.height;
      const visibleBottom = miniRect.bottom - transparentBottom;
      const shift = Math.round(buttonRect.top - visibleBottom);
      joinCtaMiniStage.style.setProperty('--join-mini-y', `${shift}px`);
    });
  };

  const updateJoinMiniVisibility = () => {
    if (!joinCtaDock || !joinCtaMiniStage || !joinCtaMini) return;

    const enoughRoom = window.innerHeight >= 760;
    const extraJoinPanelOpen = Boolean(
      (joinTeeField && !joinTeeField.hidden)
      || (claimPlayerPanel && !claimPlayerPanel.hidden)
    );
    const ready = Boolean(
      joinCtaMini.getAttribute('src')
      && joinCtaMini.complete
      && joinCtaMini.naturalHeight
    );
    const show = Boolean(
      enoughRoom
      && ready
      && joinRoundForm
      && !joinRoundForm.hidden
      && !extraJoinPanelOpen
    );

    joinCtaMiniStage.hidden = !show;
    joinCtaMiniStage.setAttribute('aria-hidden', show ? 'false' : 'true');
    joinCtaDock.classList.toggle('has-mini', show);

    if (show) alignJoinMiniToButton();
  };

  const loadRandomJoinMini = async (role = 'player') => {
    if (!joinCtaDock || !joinCtaMiniStage || !joinCtaMini) return;

    joinCtaMiniStage.hidden = true;
    joinCtaMiniStage.setAttribute('aria-hidden', 'true');
    joinCtaDock.classList.remove('has-mini');
    joinCtaMini.classList.remove('is-loaded');
    joinCtaMini.removeAttribute('src');
    delete joinCtaMini.dataset.opaqueBottomRatio;

    try {
      const [manifestResponse, preferences] = await Promise.all([
        fetch('/static/assets/_meta/asset-manifest.json'),
        requestJson('/api/preferences'),
      ]);
      if (!manifestResponse.ok || !preferences?.mini_mascots_enabled) return;

      const manifest = await manifestResponse.json();
      const joiningMinis = (manifest.assets || []).filter(
        (item) => (
          item.family === 'mini-mascot'
          && item.category === 'joining'
          && item.production
        )
      );

      const eventKeys = role === 'spectator'
        ? new Set(['player_join_spectator'])
        : new Set(['player_join_new', 'player_join_returning']);
      const matching = joiningMinis.filter(
        (item) => eventKeys.has(String(item.event_key || ''))
      );
      const pool = matching.length ? matching : joiningMinis;
      if (!pool.length) return;

      const picked = pool[Math.floor(Math.random() * pool.length)];
      const productionPath = String(picked.production).replace(/^\/+/, '');
      const imagePath = productionPath.startsWith('static/')
        ? `/${productionPath}`
        : `/static/${productionPath}`;

      joinCtaMini.addEventListener(
        'load',
        () => {
          joinCtaMini.classList.add('is-loaded');
          updateJoinMiniVisibility();
        },
        { once: true }
      );
      joinCtaMini.src = imagePath;
    } catch (_error) {
      joinCtaMiniStage.hidden = true;
      joinCtaDock.classList.remove('has-mini');
    }
  };

  [joinTeeField, claimPlayerPanel].forEach((panel) => {
    if (!panel) return;
    const observer = new MutationObserver(updateJoinMiniVisibility);
    observer.observe(panel, {
      attributes: true,
      attributeFilter: ['hidden'],
    });
  });
  window.addEventListener('resize', updateJoinMiniVisibility);

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
          spouse_type: values.get('spouse_type'),
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

  const resetInviteJoinUi = ({ clearToken = false } = {}) => {
    pendingRoundInvitePreview = null;
    joinRoundForm?.classList.remove('is-invite-acceptance');
    if (inviteJoinBanner) inviteJoinBanner.hidden = true;
    if (inviteJoinTitle) inviteJoinTitle.textContent = "YOU'RE INVITED";
    if (inviteJoinCopy) {
      inviteJoinCopy.textContent = 'Sign in, pick what the round needs, and get in.';
    }
    if (clearToken) {
      pendingRoundInviteToken = '';
      if (window.location.pathname.startsWith('/invite/')) {
        window.history.replaceState({}, '', '/');
      }
    }
  };

  const configureInviteJoinUi = (preview) => {
    if (!joinRoundForm) return;
    joinRoundForm.classList.add('is-invite-acceptance');
    if (inviteJoinBanner) inviteJoinBanner.hidden = false;
    if (inviteJoinTitle) {
      inviteJoinTitle.textContent =
        preview.role === 'spectator'
          ? 'INVITED AS SPECTATOR'
          : 'INVITED AS PLAYER';
    }
    if (inviteJoinCopy) {
      const place = preview.course_name || preview.free_play_name || 'this round';
      inviteJoinCopy.textContent =
        preview.role === 'spectator'
          ? `You’re watching ${place}. Sign in and get straight into the damage.`
          : `You’re playing ${place}. Pick a tee only if the course needs one.`;
    }

    const roleRadio = joinRoundForm.querySelector(
      `input[name="role"][value="${preview.role}"]`
    );
    if (roleRadio) roleRadio.checked = true;

    if (joinRoundSubmit) {
      joinRoundSubmit.hidden = false;
      joinRoundSubmit.textContent = 'JOIN THIS ROUND';
    }
  };

  const acceptPendingRoundInvite = async (teeName = '') => {
    if (!pendingRoundInviteToken) return false;
    const accepted = await requestJson(
      `/api/invites/${encodeURIComponent(pendingRoundInviteToken)}/accept`,
      {
        method: 'POST',
        body: { tee_name: teeName || null },
      }
    );

    pendingRoundInviteToken = '';
    pendingRoundInvitePreview = null;
    joinRoundForm?.classList.remove('is-invite-acceptance');
    if (inviteJoinBanner) inviteJoinBanner.hidden = true;
    window.history.replaceState({}, '', '/');
    await enterJoinedRound(accepted.active_code);
    return true;
  };

  const processPendingRoundInvite = async () => {
    if (
      !pendingRoundInviteToken
      || !sessionToken()
      || roundInviteProcessing
    ) return;

    roundInviteProcessing = true;
    try {
      const preview = await requestJson(
        `/api/invites/${encodeURIComponent(pendingRoundInviteToken)}`,
        { authenticated: false }
      );
      pendingRoundInvitePreview = preview;
      showRoundPanel('join');
      configureInviteJoinUi(preview);

      if (joinTeeField) joinTeeField.hidden = true;
      if (joinTeeSelect) joinTeeSelect.replaceChildren();

      if (preview.requires_tee) {
        try {
          setFormBusy(joinRoundForm, true);
          await acceptPendingRoundInvite('');
          return;
        } catch (error) {
          if (!/pick a tee/i.test(String(error?.message || ''))) {
            throw error;
          }
        } finally {
          setFormBusy(joinRoundForm, false);
        }

        fillTeeSelect(joinTeeSelect, preview.available_tees || []);
        if (joinTeeField) joinTeeField.hidden = false;
        joinTeeSelect?.focus();
        return;
      }

      setFormBusy(joinRoundForm, true);
      try {
        await acceptPendingRoundInvite('');
      } finally {
        setFormBusy(joinRoundForm, false);
      }
    } catch (error) {
      showRoundPanel('join');
      configureInviteJoinUi({
        role: pendingRoundInvitePreview?.role || 'player',
        course_name: null,
        free_play_name: null,
      });
      if (joinRoundSubmit) joinRoundSubmit.hidden = true;
      setRoundFlowMessage(error.message);
    } finally {
      roundInviteProcessing = false;
    }
  };

  const copyRoundInvite = async (url) => {
    try {
      await navigator.clipboard.writeText(url);
      return true;
    } catch (_error) {
      const input = document.createElement('textarea');
      input.value = url;
      input.setAttribute('readonly', '');
      input.style.position = 'fixed';
      input.style.opacity = '0';
      document.body.append(input);
      input.select();
      const copied = document.execCommand('copy');
      input.remove();
      return copied;
    }
  };

  const shareRoundInvite = async (role, button) => {
    if (
      !currentLobbyRound
      || !['setup', 'active'].includes(currentLobbyRound.status)
    ) return;

    if (button) button.disabled = true;
    setRoundFlowMessage('');
    try {
      const invite = await requestJson(
        `/api/rounds/${currentLobbyRound.id}/invites`,
        {
          method: 'POST',
          body: { role },
        }
      );
      const url =
        `${window.location.origin}/invite/${encodeURIComponent(invite.token)}`;
      const shareText = role === 'spectator'
        ? 'Come watch this golf disaster.'
        : 'Get in this round and bring your worst golf.';

      if (navigator.share) {
        try {
          await navigator.share({
            title: 'Who Pushed Me?!',
            text: shareText,
            url,
          });
          setRoundFlowMessage(
            role === 'spectator'
              ? 'SPECTATOR INVITE READY.'
              : 'PLAYER INVITE READY.'
          );
          return;
        } catch (error) {
          if (error?.name === 'AbortError') return;
        }
      }

      const copied = await copyRoundInvite(url);
      setRoundFlowMessage(
        copied
          ? (
              role === 'spectator'
                ? 'SPECTATOR INVITE COPIED.'
                : 'PLAYER INVITE COPIED.'
            )
          : 'COULD NOT COPY THE INVITE LINK.'
      );
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      if (button) button.disabled = false;
    }
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
              'Scores already exist. Confirm the handicap correction so the round history stays honest.'
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

  const inferredCourseHoleCount = () => {
    const explicit = Number(selectedCourse?.hole_count || 0);
    if (explicit === 9 || explicit === 18) return explicit;

    const teeHoleCounts = (selectedCourse?.tees || [])
      .map((tee) => Number(tee.holes_with_tee || 0))
      .filter((count) => count > 0);
    const teeCount = teeHoleCounts.length ? Math.max(...teeHoleCounts) : 0;
    if (teeCount === 9) return 9;
    if (teeCount >= 18) return 18;
    return 0;
  };

  const setCourseLayoutChoice = (count) => {
    if (!startRoundForm || ![9, 18].includes(Number(count))) return;
    const radio = startRoundForm.querySelector(
      `input[name="course_hole_count"][value="${Number(count)}"]`
    );
    if (radio) radio.checked = true;
  };

  const syncCourseLayoutControl = () => {
    if (!courseLayoutFieldset) return;

    const courseMode = startRoundForm?.querySelector(
      'input[name="course_mode"]:checked'
    )?.value || 'course';
    const inferred = courseMode === 'course'
      ? inferredCourseHoleCount()
      : 0;
    const needsChoice = (
      courseMode === 'free'
      || (Boolean(selectedCourse) && !inferred)
    );

    courseLayoutFieldset.hidden = !needsChoice;

    if (inferred) {
      setCourseLayoutChoice(inferred);
    }

    if (courseLayoutHint) {
      courseLayoutHint.textContent = courseMode === 'free'
        ? 'Free Play needs the physical layout. A 9-hole course can still be played for 18 by looping it twice.'
        : 'Course data could not confirm 9 vs 18. Pick the physical layout so the hole route wraps correctly.';
    }
  };

  const syncSetupParTrackingVisibility = () => {
    if (!setupParTracking) return;

    const courseMode = startRoundForm?.querySelector(
      'input[name="course_mode"]:checked'
    )?.value || 'course';
    const loadedCourseHasCompletePars = Boolean(
      courseMode === 'course'
      && (
        selectedCourse?.has_complete_pars === true
        || (
          selectedCourse?.has_complete_pars == null
          && selectedCourse?.has_pars === true
        )
      )
    );

    setupParTracking.hidden = loadedCourseHasCompletePars;

    if (loadedCourseHasCompletePars && startRoundForm) {
      const asGo = startRoundForm.querySelector(
        'input[name="par_setup"][value="as_go"]'
      );
      if (asGo) asGo.checked = true;
    }
  };

  const updateRoundHolesHint = () => {
    const courseMode = startRoundForm?.querySelector(
      'input[name="course_mode"]:checked'
    )?.value || 'course';

    if (courseMode === 'free') {
      setRoundHolesHint(
        'Pick how many holes you’re playing. Course layout is a separate choice below.'
      );
      return;
    }

    if (!selectedCourse) {
      setRoundHolesHint(
        'Pick how many holes you’re playing. Select a course and we’ll detect its physical layout when possible.'
      );
      return;
    }

    const physicalCount = inferredCourseHoleCount();
    if (physicalCount === 9) {
      setRoundHolesHint(
        'Course data says this is a 9-hole course. You can still play 18 by looping the nine twice.'
      );
    } else if (physicalCount === 18) {
      setRoundHolesHint(
        'Course data says this is an 18-hole course.'
      );
    } else {
      setRoundHolesHint(
        'Course layout is unknown. Pick the physical 9/18-hole layout below.'
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
    syncCourseLayoutControl();
    syncSetupParTrackingVisibility();
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
    )?.value || 'course';

    if (courseMode === 'course') {
      const inferred = inferredCourseHoleCount();
      if (inferred) return inferred;
    }

    const checked = startRoundForm?.querySelector(
      'input[name="course_hole_count"]:checked'
    );
    return Number(checked?.value || 18);
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
      syncCourseLayoutControl();
      syncSetupParTrackingVisibility();
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
    syncCourseLayoutControl();
    syncSetupParTrackingVisibility();
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
    if (resolved === 3) {
      syncSetupParTrackingVisibility();
      renderRoutePreview();
    }
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
    stopUserHeckle('roundJoin', { hide: true });
    stopLobbyBanterRotation();
    resetLiveMomentState();
    roundFlowModal.hidden = true;
    document.body.classList.remove('modal-open');
    setRoundFlowMessage('');
    if (bagModal) bagModal.hidden = true;
    closeScoreResponseSheet();
    currentBagAction = null;
    currentLobbyRound = null;
    roundHistoryOpen = false;
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
    stopLobbyBanterRotation();
    stopUserHeckle('home');
    stopUserHeckle('roundSetup', { hide: true });
    stopUserHeckle('roundJoin', { hide: true });
    roundFlowModal.hidden = false;
    document.body.classList.add('modal-open');
    setRoundFlowMessage('');
    currentLobbyRound = null;
    roundHistoryOpen = false;
    resetLiveMomentState();
    resetClaimPlayerPanel();

    if (startRoundForm) startRoundForm.hidden = panel !== 'start';
    setCourseStepMessage('');
    if (joinRoundForm) joinRoundForm.hidden = panel !== 'join';
    if (lobbyPanel) lobbyPanel.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = true;
    roundFlowCardGame?.classList.remove('is-live-round');
    if (roundEndPanel) roundEndPanel.hidden = true;
    if (roundHistoryPage) roundHistoryPage.hidden = true;
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
    if (panel === 'join') {
      joinCodeDigits.forEach((input) => {
        input.value = '';
      });
      if (joinRoundCode) joinRoundCode.value = '';
      void loadRandomJoinMini(
        joinRoundForm?.querySelector('input[name="role"]:checked')?.value || 'player'
      );
      void startUserHeckles(
        'roundJoin',
        'round_join.idle',
        () => (
          Boolean(roundFlowModal && !roundFlowModal.hidden)
          && Boolean(joinRoundForm && !joinRoundForm.hidden)
        ),
      );
      window.requestAnimationFrame(() => joinCodeDigits[0]?.focus());
    } else {
      roundFlowClose?.focus();
    }
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

  const dismissHoleTransition = () => {
    if (holeTransitionTimer) {
      window.clearTimeout(holeTransitionTimer);
      holeTransitionTimer = null;
    }
    if (holeTransition) {
      holeTransition.hidden = true;
      holeTransition.setAttribute('aria-hidden', 'true');
    }
    if (holeTransitionMascot) {
      holeTransitionMascot.hidden = true;
      holeTransitionMascot.removeAttribute('src');
    }
  };

  const resetLiveMomentState = () => {
    scoreAnnouncementRoundId = '';
    seenScoreAnnouncementEventIds = new Set();
    scoreAnnouncementQueue = [];

    if (scoreAnnouncementTimer) {
      window.clearTimeout(scoreAnnouncementTimer);
      scoreAnnouncementTimer = null;
    }
    if (scoreAnnouncement) {
      scoreAnnouncement.hidden = true;
      scoreAnnouncement.classList.remove('is-showing');
    }

    dismissHoleTransition();
  };

  const scoreAnnouncementCopy = (round, event) => {
    const scoreName = scoreNameFromEvent(event).toUpperCase();

    if (event?.data?.scope === 'team' || round.mode === 'scramble') {
      return `TEAM SCORED ${scoreName}!`;
    }

    const subjectId = String(event?.data?.player_participant_id || '');
    if (subjectId === String(round.viewer_participant_id || '')) {
      return `YOU SCORED ${scoreName}!`;
    }

    const subject = (round.participants || []).find(
      (participant) => String(participant.id) === subjectId
    );
    return `${String(subject?.display_name || 'SOMEONE').toUpperCase()} SCORED ${scoreName}!`;
  };

  const showNextScoreAnnouncement = () => {
    if (
      !scoreAnnouncement
      || !scoreAnnouncementText
      || scoreAnnouncementTimer
      || !scoreAnnouncementQueue.length
    ) return;

    scoreAnnouncementText.textContent = scoreAnnouncementQueue.shift();
    scoreAnnouncement.hidden = false;
    scoreAnnouncement.classList.remove('is-showing');
    void scoreAnnouncement.offsetWidth;
    scoreAnnouncement.classList.add('is-showing');

    scoreAnnouncementTimer = window.setTimeout(() => {
      scoreAnnouncement.hidden = true;
      scoreAnnouncement.classList.remove('is-showing');
      scoreAnnouncementText.textContent = '';
      scoreAnnouncementTimer = null;
      if (scoreAnnouncementQueue.length) {
        window.setTimeout(showNextScoreAnnouncement, 120);
      }
    }, 2400);
  };

  const queueNewScoreAnnouncements = (round) => {
    const roundId = String(round?.id || '');
    const scoreEvents = (round.events || []).filter(
      (event) =>
        event.event_type === 'score_report'
        && !event.data?.backfilled
    );

    // First load/reconnect establishes a baseline. Old scores do not replay.
    if (scoreAnnouncementRoundId !== roundId) {
      scoreAnnouncementRoundId = roundId;
      seenScoreAnnouncementEventIds = new Set(
        scoreEvents.map((event) => String(event.id))
      );
      scoreAnnouncementQueue = [];
      return;
    }

    const unseen = scoreEvents
      .filter(
        (event) => !seenScoreAnnouncementEventIds.has(String(event.id))
      )
      .slice()
      .reverse();

    unseen.forEach((event) => {
      seenScoreAnnouncementEventIds.add(String(event.id));
      scoreAnnouncementQueue.push(
        scoreAnnouncementCopy(round, event)
      );
    });

    showNextScoreAnnouncement();
  };

  const transitionScoreBucket = (round, position) => {
    const participantId = round.mode === 'individual'
      ? round.viewer_participant_id
      : null;
    const score = findScore(round, position, participantId);
    const par = findPar(round, position);
    if (!score || !Number.isFinite(par)) return '';

    const strokes = Number(score.strokes);
    if (!Number.isFinite(strokes)) return '';
    if (strokes === 1) return 'ace';

    const delta = strokes - Number(par);
    if (delta <= -3) return 'albatross';
    if (delta === -2) return 'eagle';
    if (delta === -1) return 'birdie';
    if (delta === 0) return 'par';
    if (delta === 1) return 'bogey';
    if (delta === 2) return 'double_bogey';
    if (delta === 3) return 'triple_bogey';
    return 'quad_plus';
  };

  const transitionBucketLabel = (bucket) => ({
    ace: 'HOLE IN ONE',
    albatross: 'ALBATROSS',
    eagle: 'EAGLE',
    birdie: 'BIRDIE',
    par: 'PAR',
    bogey: 'BOGEY',
    double_bogey: 'DOUBLE BOGEY',
    triple_bogey: 'TRIPLE BOGEY',
    quad_plus: 'QUAD+',
  })[bucket] || '';

  const normalizeTransitionToken = (value) => (
    String(value || '')
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_+|_+$/g, '')
  );

  const transitionBucketAliases = (bucket) => ({
    ace: ['ace', 'hole_in_one'],
    albatross: ['albatross'],
    eagle: ['eagle'],
    birdie: ['birdie'],
    par: ['par'],
    bogey: ['bogey'],
    double_bogey: ['double_bogey'],
    triple_bogey: ['triple_bogey'],
    quad_plus: ['quad_plus', 'quadruple_bogey', 'quadruple_bogey_or_worse'],
  })[bucket] || [];

  const loadTransitionAssets = () => {
    if (transitionAssetsPromise) return transitionAssetsPromise;

    transitionAssetsPromise = fetch('/static/assets/_meta/asset-manifest.json')
      .then((response) => {
        if (!response.ok) throw new Error('asset manifest unavailable');
        return response.json();
      })
      .then((manifest) =>
        (manifest.assets || [])
          .filter(
            (item) =>
              item.production
              && item.enabled !== false
              && (
                item.family === 'mini-mascot'
                || item.asset_id === 'mascot.full_body.transparent'
              )
          )
          .sort((left, right) =>
            String(left.asset_id).localeCompare(String(right.asset_id))
          )
      )
      .catch(() => []);

    return transitionAssetsPromise;
  };

  const stableTransitionHash = (value) => {
    let hash = 2166136261;
    for (const character of String(value || '')) {
      hash ^= character.charCodeAt(0);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  };

  const scoreSpecificTransitionAssets = (assets, bucket) => {
    if (!bucket) return [];
    const aliases = transitionBucketAliases(bucket);

    return assets.filter((item) => {
      const category = normalizeTransitionToken(item.category);
      if (category !== 'score') return false;

      const fields = [
        item.transition_bucket,
        item.situation,
        item.event_key,
      ].map(normalizeTransitionToken);

      return aliases.some((alias) =>
        fields.some(
          (field) => field === alias || field.endsWith('_' + alias)
        )
      );
    });
  };

  const genericScoreTransitionAssets = (assets) => assets.filter(
    (item) => normalizeTransitionToken(item.category) === 'score'
  );

  const generalTransitionAssets = (assets) => assets.filter((item) => {
    const eventKey = normalizeTransitionToken(item.event_key);
    const category = normalizeTransitionToken(item.category);
    const situation = normalizeTransitionToken(item.situation);
    const pool = normalizeTransitionToken(item.pool);
    const transitionBucket = normalizeTransitionToken(item.transition_bucket);

    return (
      transitionBucket === 'general'
      || pool === 'round_transitions'
      || eventKey === 'round_start'
      || (category === 'round' && situation === 'start')
      || item.asset_id === 'mascot.full_body.transparent'
    );
  });

  const transitionMascotForPosition = (round, targetPosition, assets) => {
    const used = new Set();
    const genericScore = genericScoreTransitionAssets(assets);
    const general = generalTransitionAssets(assets);
    let target = null;

    // Recompute from hole one so every device derives the same sequence and
    // no transition mascot repeats inside the round.
    for (let position = 1; position <= Number(targetPosition); position += 1) {
      const bucket = transitionScoreBucket(round, position);
      const specific = scoreSpecificTransitionAssets(assets, bucket)
        .filter((item) => !used.has(String(item.asset_id)));
      const scoreFallback = bucket
        ? genericScore.filter(
            (item) => !used.has(String(item.asset_id))
          )
        : [];
      const fallback = general.filter(
        (item) => !used.has(String(item.asset_id))
      );
      const pool = specific.length
        ? specific
        : (scoreFallback.length ? scoreFallback : fallback);

      if (!pool.length) {
        if (position === Number(targetPosition)) target = null;
        continue;
      }

      const poolKind = specific.length
        ? bucket
        : (scoreFallback.length ? 'score' : 'general');
      const index = stableTransitionHash(
        `${round.id}:${position}:${poolKind}`
      ) % pool.length;
      const picked = pool[index];
      used.add(String(picked.asset_id));

      if (position === Number(targetPosition)) {
        target = picked;
      }
    }

    return target;
  };

  const playHoleTransition = async (round, fromPosition, toPosition) => {
    if (
      !holeTransition
      || !holeTransitionMascot
      || !holeTransitionLabel
      || Number(toPosition) <= Number(fromPosition)
    ) return;

    const fromRoute = routeEntry(round, fromPosition);
    const toRoute = routeEntry(round, toPosition);
    const fromHole = Number(fromRoute?.hole_number || fromPosition);
    const toHole = Number(toRoute?.hole_number || toPosition);
    const bucket = transitionScoreBucket(round, fromPosition);

    if (holeTransitionTimer) {
      window.clearTimeout(holeTransitionTimer);
      holeTransitionTimer = null;
    }

    holeTransitionLabel.textContent = `HOLE ${fromHole} → HOLE ${toHole}`;
    if (holeTransitionResult) {
      holeTransitionResult.textContent = transitionBucketLabel(bucket);
      holeTransitionResult.hidden = !holeTransitionResult.textContent;
    }

    holeTransitionMascot.hidden = true;
    holeTransitionMascot.removeAttribute('src');
    holeTransition.hidden = false;
    holeTransition.setAttribute('aria-hidden', 'false');

    const assets = await loadTransitionAssets();
    const mascot = transitionMascotForPosition(
      round,
      fromPosition,
      assets
    );

    if (mascot?.production && !holeTransition.hidden) {
      holeTransitionMascot.src = assetUrl(mascot.production);
      holeTransitionMascot.alt = 'Who Pushed Me transition mascot';
      holeTransitionMascot.hidden = false;
    }

    holeTransitionTimer = window.setTimeout(
      dismissHoleTransition,
      10000
    );
  };

  holeTransitionContinue?.addEventListener(
    'click',
    dismissHoleTransition
  );

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
    score,
    scoreEventOverride = null
  ) => {
    if (!score && !scoreEventOverride) return;

    const scoreEvent = (
      scoreEventOverride
      || findScoreEvent(round, position, participantId)
    );
    if (!scoreEvent) return;

    const responsePanel = document.createElement('section');
    responsePanel.className = 'score-response-panel live-score-social-panel';
    responsePanel.dataset.scoreEventId = String(scoreEvent.id);

    const responseHeading = document.createElement('div');
    responseHeading.className = 'score-response-heading';
    responseHeading.textContent = 'REACTIONS / CHALLENGES';

    const responseSubheading = document.createElement('small');
    responseSubheading.className = 'score-response-subheading';
    responseSubheading.textContent = 'React, challenge it, or talk your shit.';

    const reactions = eventReactions(round, scoreEvent.id);
    const viewerId = String(round.viewer_participant_id || '');
    const viewerReaction = reactions.find(
      (reaction) => String(reaction.actor_participant_id) === viewerId
    );
    let selectedResponseKind = String(viewerReaction?.reaction_kind || '');

    const sendResponse = async (
      responseKind,
      { message = '', targetParticipantId = null } = {}
    ) => {
      const body = {
        response_kind: responseKind,
      };
      if (message) body.message = message;
      if (targetParticipantId) {
        body.target_participant_id = targetParticipantId;
      }

      setRoundFlowMessage('');
      try {
        await requestJson(
          `/api/rounds/${round.id}/score-events/${scoreEvent.id}/responses`,
          {
            method: 'POST',
            body,
          }
        );
        await refreshRound(round.active_code);
        return true;
      } catch (error) {
        setRoundFlowMessage(error.message);
        return false;
      }
    };

    const responseButtons = document.createElement('div');
    responseButtons.className = 'score-response-buttons';
    const reactionButtons = new Map();

    const syncReactionButtons = () => {
      reactionButtons.forEach((button, kind) => {
        const active = selectedResponseKind === kind;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
    };

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
      reactionButtons.set(kind, button);

      button.addEventListener('click', async () => {
        const wasActive = selectedResponseKind === kind;
        button.disabled = true;
        setRoundFlowMessage('');
        try {
          await requestJson(
            `/api/rounds/${round.id}/events/${scoreEvent.id}/reaction`,
            wasActive
              ? { method: 'DELETE' }
              : {
                  method: 'PUT',
                  body: { reaction: kind },
                }
          );
          selectedResponseKind = wasActive ? '' : kind;
          syncReactionButtons();
          await refreshRound(round.active_code);
        } catch (error) {
          setRoundFlowMessage(error.message);
        } finally {
          button.disabled = false;
        }
      });
      responseButtons.append(button);
    });
    syncReactionButtons();

    responsePanel.append(
      responseHeading,
      responseSubheading,
      responseButtons
    );

    const scoreTargetId = String(
      scoreEvent.data?.player_participant_id || ''
    );
    const canCallOutScore = (
      viewerIsActivePlayer(round)
      && (
        round.mode === 'scramble'
        || (
          scoreTargetId
          && scoreTargetId !== viewerId
        )
      )
    );
    if (canCallOutScore) {
      const calloutButton = document.createElement('button');
      calloutButton.type = 'button';
      calloutButton.className = 'score-response-callout';
      calloutButton.textContent = 'CALL OUT';
      calloutButton.addEventListener('click', () => {
        closeScoreResponseSheet();
        openBag('callout', {
          replyToEventId: scoreEvent.id,
          routePosition: scoreEvent.route_position,
          targetParticipantId: round.mode === 'individual'
            ? scoreTargetId
            : null,
        });
      });
      responsePanel.append(calloutButton);
    }

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
      viewerIsActivePlayer(round)
      && String(scoreEvent.actor_participant_id || '') !== viewerId
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

      [proposed, comment].forEach((input) => {
        input.addEventListener('input', () => {
          input.dataset.socialDraftDirty = 'true';
        });
      });

      const challengeButton = document.createElement('button');
      challengeButton.type = 'button';
      challengeButton.textContent = existingChallenge
        ? 'UPDATE CHALLENGE'
        : 'CHALLENGE SCORE';
      challengeButton.addEventListener('click', async () => {
        const proposedValue = proposed.value.trim();
        const commentValue = comment.value.trim();
        if (!proposedValue && !commentValue) {
          setRoundFlowMessage(
            'Give a corrected score or say why you are challenging it.'
          );
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
    customInput.placeholder = 'Add a comment or just send the reaction...';
    customInput.addEventListener('input', () => {
      customInput.dataset.socialDraftDirty = 'true';
    });

    const customButton = document.createElement('button');
    customButton.type = 'button';
    customButton.textContent = 'SEND';
    customButton.addEventListener('click', async () => {
      const message = customInput.value.trim();
      if (!message && !selectedResponseKind) return;

      customButton.disabled = true;
      const responseKind = selectedResponseKind === 'talk_shit'
        ? 'random'
        : (selectedResponseKind || 'custom');
      const sent = await sendResponse(responseKind, { message });
      if (!sent) {
        customButton.disabled = false;
      }
    });

    customInput.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter') return;
      event.preventDefault();
      customButton.click();
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

  const closeScoreResponseSheet = () => {
    if (!scoreResponseModal) return;
    openScoreResponseEventId = '';
    scoreResponseModal.hidden = true;
    if (scoreResponseSheetBody) scoreResponseSheetBody.replaceChildren();
    if (scoreResponseContext) scoreResponseContext.textContent = '';
    document.body.classList.remove('score-response-open');
  };

  const openScoreResponseSheet = (
    round,
    scoreEvent,
    { autofocus = true } = {}
  ) => {
    if (!scoreResponseModal || !scoreResponseSheetBody || !scoreEvent) return;

    openScoreResponseEventId = String(scoreEvent.id || '');
    const participantId = scoreEvent.data?.player_participant_id || null;
    const participant = participantId
      ? (round.participants || []).find(
          (row) => String(row.id) === String(participantId)
        )
      : null;
    const label = round.mode === 'scramble'
      ? 'TEAM SCORE'
      : (participant?.display_name || 'SCORE');
    const hole = scoreEvent.hole_number || scoreEvent.route_position || '';
    if (scoreResponseContext) {
      scoreResponseContext.textContent = [label, hole ? ('HOLE ' + hole) : '']
        .filter(Boolean)
        .join(' • ');
    }

    scoreResponseSheetBody.replaceChildren();
    appendScoreResponsePanel(
      scoreResponseSheetBody,
      round,
      Number(scoreEvent.route_position || 0),
      participantId,
      { strokes: Number(scoreEvent.new_value || 0) || 1 },
      scoreEvent
    );
    scoreResponseModal.hidden = false;
    document.body.classList.add('score-response-open');
    if (autofocus) {
      window.requestAnimationFrame(() => {
        scoreResponseSheetBody.querySelector('button, input, select')?.focus();
      });
    }
  };

  const refreshOpenScoreResponseSheet = (round) => {
    if (
      !round
      || !openScoreResponseEventId
      || !scoreResponseModal
      || scoreResponseModal.hidden
    ) return;

    const freshEvent = (round.events || []).find(
      (event) => String(event.id || '') === openScoreResponseEventId
    );
    if (!freshEvent) {
      closeScoreResponseSheet();
      return;
    }

    openScoreResponseSheet(
      round,
      freshEvent,
      { autofocus: false }
    );
  };

  const renderScoreCard = (round, position) => {
    if (!liveScoreArea) return;
    liveScoreArea.replaceChildren();

    const route = routeEntry(round, position);
    const hole = Number(route?.hole_number || position);
    const par = findPar(round, position);
    const canScore = (
      round.viewer_role === 'player'
      && viewerIsActivePlayer(round)
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
        score ? (relative ? (relative + ' TO PAR') : 'SCORE SAVED') : '',
      ]
        .filter(Boolean)
        .join(' • ');
      meta.hidden = !meta.textContent;
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
      const targetCanBeEditedByViewer = (
        round.mode === 'scramble'
        || String(participantId || '') === String(round.viewer_participant_id || '')
        || Boolean(target?.round_only)
      );

      if (!canScore || !targetCanReceiveScore || !targetCanBeEditedByViewer) {
        const readonly = document.createElement('div');
        readonly.className = 'live-score-readonly';
        readonly.textContent = route?.state === 'skipped'
          ? 'UNTRACKED'
          : (score ? String(score.strokes) : '—');
        card.append(readonly);
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
      input.value = score
        ? String(score.strokes)
        : (par ? String(par) : '');
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

      const submit = document.createElement('button');
      submit.type = 'button';
      submit.className = 'live-score-submit';

      const refreshSubmitState = () => {
        const strokes = Number(input.value);
        const valid = Number.isInteger(strokes) && strokes >= 1 && strokes <= 99;
        const unchanged = Boolean(
          score && valid && Number(score.strokes) === strokes
        );
        submit.disabled = !valid || unchanged;
        submit.textContent = unchanged
          ? 'SAVED'
          : (score ? 'UPDATE' : 'SUBMIT');
      };

      const setBusy = (busy) => {
        minus.disabled = busy;
        plus.disabled = busy;
        input.disabled = busy;
        submit.disabled = busy;
      };

      let scoreSaveInFlight = false;

      const persistScore = async (strokes) => {
        if (scoreSaveInFlight) return false;
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
        scoreSaveInFlight = true;
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

          if (round.mode === 'scramble') {
            skippedScrambleContributionPromptKey = '';
          }

          await refreshRound(round.active_code);
          return true;
        } catch (error) {
          scoreSaveInFlight = false;
          setRoundFlowMessage(error.message);
          setBusy(false);
          return false;
        }
      };

      const focusScoreInput = () => {
        try {
          input.focus({ preventScroll: true });
        } catch (_error) {
          input.focus();
        }
      };

      minus.addEventListener('click', () => {
        const base = Number(input.value || par || 1);
        input.value = String(Math.max(1, base - 1));
        input.dataset.draftDirty = 'true';
        refreshSubmitState();
        focusScoreInput();
      });

      plus.addEventListener('click', () => {
        const base = Number(input.value || (par ? Number(par) - 1 : 0));
        input.value = String(Math.min(99, Math.max(1, base + 1)));
        input.dataset.draftDirty = 'true';
        refreshSubmitState();
        focusScoreInput();
      });

      input.addEventListener('input', () => {
        const digits = String(input.value || '').replace(/\D/g, '').slice(0, 2);
        input.value = digits;
        input.dataset.draftDirty = 'true';
        refreshSubmitState();
      });

      input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !submit.disabled) {
          event.preventDefault();
          submit.click();
        }
      });

      submit.addEventListener('click', async () => {
        const strokes = Number(input.value);
        const saved = await persistScore(strokes);
        if (!saved) {
          refreshSubmitState();
          return;
        }
        delete input.dataset.draftDirty;
      });

      controls.append(minus, input, plus);
      card.append(controls, submit);
      refreshSubmitState();

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

      liveScoreArea.append(card);
    };

    if (round.mode === 'scramble') {
      addCard('TEAM SCORE', null, 'SCRAMBLE');
      return;
    }

    (round.participants || [])
      .filter(
        (participant) =>
          participant.role === 'player'
          && (
            String(participant.id) === String(round.viewer_participant_id || '')
            || Boolean(participant.round_only)
          )
      )
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
    const promptKey = `${round.id}:${Number(position)}`;

    if (round.mode !== 'scramble') {
      scrambleContributionPanel.hidden = true;
      scrambleContributionList.replaceChildren();
      if (scrambleContributionSkip) scrambleContributionSkip.hidden = true;
      return;
    }

    if (!scrambleContributionComposerOpen) {
      scrambleContributionPanel.hidden = true;
      scrambleContributionList.replaceChildren();
      if (scrambleContributionSkip) scrambleContributionSkip.hidden = true;
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
    if (scrambleContributionSkip) {
      scrambleContributionSkip.hidden = !canEdit;
      scrambleContributionSkip.textContent = 'DONE';
    }

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

  const scoreNameFromEvent = (event) => {
    const key = String(
      event?.content_event_key
      || event?.presentation?.event_key
      || ''
    );
    const suffix = key.split('.').pop();
    return ({
      ace: 'a hole in one',
      albatross: 'an albatross',
      eagle: 'an eagle',
      birdie: 'a birdie',
      par: 'par',
      bogey: 'a bogey',
      double_bogey: 'a double bogey',
      triple_bogey: 'a triple bogey',
      quad_plus: 'a quadruple bogey or worse',
    })[suffix] || 'a score';
  };

  const stripScoreLead = (text, event) => {
    const value = String(text || '');
    const key = String(
      event?.content_event_key
      || event?.presentation?.event_key
      || ''
    );
    const suffix = key.split('.').pop();
    const patterns = {
      ace: /^(?:(?:a fucking )?ace|hole in one)[.!?]\s*/i,
      albatross: /^(?:an? )?albatross[.!?]\s*/i,
      eagle: /^eagle[.!?]\s*/i,
      birdie: /^birdie[.!?]\s*/i,
      par: /^par[.!?]\s*/i,
      bogey: /^bogey[.!?]\s*/i,
      double_bogey: /^double bogey[.!?]\s*/i,
      triple_bogey: /^triple bogey[.!?]\s*/i,
      quad_plus: /^(?:a )?quadruple bogey or worse[.!?]\s*/i,
    };
    const pattern = patterns[suffix];
    return (pattern ? value.replace(pattern, '') : value).trim();
  };

  const thirdPersonScoreComment = (text) => {
    return String(text || '')
      .replace(/\bYou're\b/g, "They're")
      .replace(/\byou're\b/g, "they're")
      .replace(/\bYou are\b/g, 'They are')
      .replace(/\byou are\b/g, 'they are')
      .replace(/\bYour\b/g, 'Their')
      .replace(/\byour\b/g, 'their')
      .replace(/\bYou\b/g, 'They')
      .replace(/\byou\b/g, 'they');
  };

  const scoreFeedText = (round, event) => {
    const eventType = String(event?.event_type || '');

    if (eventType === 'score_response') {
      const responseKind = String(event?.data?.response_kind || '').trim();
      const message = String(event?.data?.message || '').trim();
      if (message && responseKind && responseKind !== 'custom') {
        return responseKind.replaceAll('_', ' ').toUpperCase() + ': ' + message;
      }
      return message || presentationText(event);
    }

    if (eventType === 'score_challenge') {
      const message = String(event?.data?.message || '').trim();
      const proposed = event?.data?.proposed_score;
      const parts = ['SCORE CHALLENGE'];
      if (proposed !== null && proposed !== undefined && proposed !== '') {
        parts.push('SAYS ' + String(proposed));
      }
      if (message) parts.push(message);
      return parts.join(' — ');
    }
    if (
      round?.mode !== 'individual'
      || !['score_report', 'score_push'].includes(eventType)
    ) {
      return presentationText(event);
    }

    const subjectId = String(event?.data?.player_participant_id || '');
    const subject = (round.participants || []).find(
      (participant) => String(participant.id) === subjectId
    );
    if (!subject) return presentationText(event);

    const viewerIsSubject = subjectId === String(round.viewer_participant_id || '');
    const presentation = event?.presentation || {};
    const rawPresentationComment = String(
      presentation.banter?.text || ''
    ).trim();
    if (eventType === 'score_report' && !rawPresentationComment) {
      return '';
    }
    const rawComment = eventType === 'score_report'
      ? stripScoreLead(rawPresentationComment, event)
      : rawPresentationComment;
    const comment = viewerIsSubject
      ? rawComment
      : thirdPersonScoreComment(rawComment);

    let prefix;
    if (eventType === 'score_report') {
      const scoreName = scoreNameFromEvent(event);
      prefix = viewerIsSubject
        ? 'You scored ' + scoreName + '.'
        : (subject.display_name || 'Golfer') + ' scored ' + scoreName + '.';
    } else if (viewerIsSubject) {
      prefix = 'Your score changed to ' + String(event.new_value ?? '') + '.';
    } else {
      prefix = (subject.display_name || 'Golfer') + ': score changed to '
        + String(event.new_value ?? '') + '.';
    }

    return comment ? prefix + ' ' + comment : prefix;
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
    const reviewingHistory = Boolean(
      liveBanterPanel?.classList.contains('is-fullscreen')
      && (
        liveBanterFeed.scrollHeight
        - liveBanterFeed.scrollTop
        - liveBanterFeed.clientHeight
      ) > 32
    );
    const priorScrollTop = liveBanterFeed.scrollTop;
    liveBanterFeed.replaceChildren();

    const socialTypes = new Set([
      'open_mic',
      'callout',
      'excuse',
      'score_response',
      'score_challenge',
      'score_report',
      'score_push',
      'scramble_contribution_change',
      'round_end_result',
    ]);

    const seenScoreKeys = new Set();
    const rows = (round.events || [])
      .filter((event) => {
        const eventType = String(event.event_type || '');
        if (!socialTypes.has(eventType)) return false;

        if (eventType === 'score_report' || eventType === 'score_push') {
          const scoreKey = [
            event.route_position || event.hole_number || '',
            event.data?.player_participant_id || 'team',
          ].join(':');
          if (seenScoreKeys.has(scoreKey)) return false;
          seenScoreKeys.add(scoreKey);
        }

        return Boolean(String(scoreFeedText(round, event) || '').trim());
      })
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
      const eventType = String(event.event_type || '');
      const playerAuthored = Boolean(
        actor
        && (
          explicitMessage
          || eventType === 'score_response'
          || eventType === 'score_challenge'
        )
        && [
          'open_mic',
          'callout',
                      'excuse',
          'score_response',
          'score_challenge',
        ].includes(eventType)
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
      bubble.textContent = scoreFeedText(round, event);

      content.append(meta, bubble);

      if (eventType === 'score_report' || eventType === 'score_push') {
        const scoreTargetId = String(
          event.data?.player_participant_id || ''
        );
        const viewerId = String(round.viewer_participant_id || '');
        const viewerOwnsScore = (
          viewerIsActivePlayer(round)
          && (
            round.mode === 'scramble'
            || (
              scoreTargetId
              && scoreTargetId === viewerId
            )
          )
        );
        const canRespond = (
          viewerIsActivePlayer(round)
          && !viewerOwnsScore
        );

        if (viewerOwnsScore) {
          const excuse = document.createElement('button');
          excuse.type = 'button';
          excuse.className = 'live-score-respond';
          excuse.textContent = 'MAKE EXCUSE';
          excuse.addEventListener('click', () => {
            openBag('excuse', {
              replyToEventId: event.id,
              routePosition: event.route_position,
            });
          });
          content.append(excuse);
        } else if (canRespond) {
          const respond = document.createElement('button');
          respond.type = 'button';
          respond.className = 'live-score-respond';
          respond.textContent = 'RESPOND';
          respond.addEventListener('click', () => {
            openScoreResponseSheet(round, event);
          });
          content.append(respond);
        }
      }

      if (
        eventType === 'callout'
        && viewerIsActivePlayer(round)
        && String(event.data?.target_participant_id || '')
          === String(round.viewer_participant_id || '')
      ) {
        const excuse = document.createElement('button');
        excuse.type = 'button';
        excuse.className = 'live-score-respond';
        excuse.textContent = 'MAKE EXCUSE';
        excuse.addEventListener('click', () => {
          openBag('excuse', {
            replyToEventId: event.id,
            routePosition: event.route_position,
          });
        });
        content.append(excuse);
      }

      row.append(avatar, content);
      liveBanterFeed.append(row);
    });

    if (reviewingHistory) {
      liveBanterFeed.scrollTop = priorScrollTop;
    } else {
      liveBanterFeed.scrollTop = liveBanterFeed.scrollHeight;
    }
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

  const renderLiveHoleStats = (round) => {
    if (!liveHoleStats) return;

    const livePosition = Number(
      round.current_route_position
      || round.current_hole
      || 1
    );

    liveHoleStats.replaceChildren();

    const heading = document.createElement('div');
    heading.className = 'live-hole-stat-heading';
    const headingTitle = document.createElement('strong');
    headingTitle.textContent = 'ROUND STATS';
    const headingMeta = document.createElement('small');
    headingMeta.textContent = 'CURRENT ROUND';
    heading.append(headingTitle, headingMeta);

    const createStat = (label, initialValue = '—') => {
      const stat = document.createElement('div');
      stat.className = 'live-hole-stat';
      const small = document.createElement('small');
      small.textContent = label;
      const strong = document.createElement('strong');
      strong.textContent = initialValue;
      stat.append(small, strong);
      return { stat, value: strong };
    };

    const scoresInStat = createStat('SCORES IN', '0/1');
    const totalStat = createStat(
      round.mode === 'scramble' ? 'TEAM TOTAL' : 'YOUR TOTAL'
    );
    const toParStat = createStat('TO PAR');

    liveHoleStats.append(
      heading,
      scoresInStat.stat,
      totalStat.stat,
      toParStat.stat
    );
    liveHoleStats.hidden = false;

    try {
      let currentScores = [];
      let expected = 1;

      if (round.mode === 'scramble') {
        const score = findScore(round, livePosition);
        if (score) currentScores = [Number(score.strokes)];
      } else {
        const players = (round.participants || []).filter(
          (participant) =>
            participant.role === 'player'
            && participant.participation_state === 'active'
            && Number(participant.tracked_from_position || 1) <= livePosition
        );
        expected = Math.max(players.length, 1);
        currentScores = players
          .map((participant) => findScore(round, livePosition, participant.id))
          .filter(Boolean)
          .map((score) => Number(score.strokes));
      }

      scoresInStat.value.textContent =
        String(currentScores.length) + '/' + String(expected);

      const viewer = viewerParticipant(round);
      const cumulativeScores = (round.scores || []).filter((score) => {
        if (Number(score.route_position) > livePosition) return false;
        if (round.mode === 'scramble') return score.score_scope === 'team';
        return (
          viewer?.role === 'player'
          && score.score_scope === 'player'
          && String(score.player_participant_id) === String(viewer.id)
        );
      });

      const totalStrokes = cumulativeScores.length
        ? cumulativeScores.reduce(
            (sum, score) => sum + Number(score.strokes || 0),
            0
          )
        : null;

      totalStat.value.textContent =
        totalStrokes === null ? '—' : String(totalStrokes);

      let totalToPar = null;
      if (
        totalStrokes !== null
        && round.par_tracking_enabled
        && cumulativeScores.length
      ) {
        let allParsKnown = true;
        let parTotal = 0;
        cumulativeScores.forEach((score) => {
          const scorePar = findPar(round, score.route_position);
          if (!Number.isFinite(scorePar)) {
            allParsKnown = false;
            return;
          }
          parTotal += Number(scorePar);
        });
        if (allParsKnown) totalToPar = totalStrokes - parTotal;
      }

      toParStat.value.textContent = totalToPar === null
        ? '—'
        : (totalToPar === 0
          ? 'E'
          : (totalToPar > 0 ? ('+' + totalToPar) : String(totalToPar)));
    } catch (_error) {
      // Keep the stat labels visible even if a malformed live payload arrives.
    }
  };

  const updateReceiptsBadge = (round) => {
    const unseen = Number(round.receipts_state?.unseen_count || 0);
    receiptsUnseenBadges.forEach((badge) => {
      badge.hidden = unseen < 1;
      badge.textContent = `YOU MISSED SOME SHIT • ${unseen}`;
    });
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

  const ROUND_HISTORY_EVENT_TYPES = new Set([
    'score_report',
    'score_push',
    'score_removed',
    'par_report',
    'par_push',
    'tee_change',
    'round_handicap_change',
    'par_tracking_change',
    'scramble_contribution_change',
    'participant_join',
    'participant_proxy_added',
    'participant_reconnect',
    'participant_claimed',
    'participant_claim_undone',
    'spectator_joined_play',
    'round_end_early_vote',
    'round_end_early_completed',
    'round_status_change',
    'round_end_result',
  ]);

  const roundHistoryTitle = (round, event) => {
    const eventType = String(event?.event_type || '');

    if (eventType === 'score_report' || eventType === 'score_push') {
      const data = event?.data || {};
      const participant = (round.participants || []).find(
        (candidate) =>
          String(candidate.id)
          === String(data.player_participant_id || '')
      );
      const subject = data.scope === 'team'
        ? 'TEAM'
        : String(participant?.display_name || 'GOLFER').toUpperCase();
      const newScore = Number(event.new_value);
      if (eventType === 'score_push') {
        const oldScore = Number(event.old_value);
        return `${subject} — SCORE CHANGED ${oldScore} → ${newScore} STROKES`;
      }
      return `${subject} — ${newScore} STROKES`;
    }

    if (eventType === 'par_report') {
      return `PAR SET TO ${String(event.new_value ?? '?')}`;
    }
    if (eventType === 'par_push') {
      return `PAR CHANGED ${String(event.old_value ?? '?')} → ${String(event.new_value ?? '?')}`;
    }

    if (eventType === 'tee_change') {
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
      return `${actorName} CHANGED ${scope} ${oldTee} → ${newTee}`;
    }

    if (eventType === 'score_removed') {
      const actor = (round.participants || []).find(
        (participant) =>
          String(participant.id) === String(event.actor_participant_id)
      );
      const target = (round.participants || []).find(
        (participant) =>
          String(participant.id)
          === String(event.data?.player_participant_id || '')
      );
      const subject = event.data?.scope === 'team'
        ? 'TEAM SCORE'
        : String(
            event.data?.subject
            || target?.display_name
            || 'GOLFER'
          ).toUpperCase();
      const oldScore = Number(event.old_value);
      const actorName = String(
        event.data?.actor_display_name
        || actor?.display_name
        || 'SOMEONE'
      ).toUpperCase();
      return event.data?.scope === 'team'
        ? `${actorName} REMOVED ${subject} ${oldScore}`
        : `${actorName} REMOVED ${subject}'S ${oldScore}`;
    }

    return presentationText(event) || 'ROUND UPDATE';
  };

  const renderReceipts = (round) => {
    if (!receiptsList) return;

    const events = (round.events || []).filter((event) =>
      ROUND_HISTORY_EVENT_TYPES.has(String(event?.event_type || ''))
    );
    roundHistoryOpenButtons.forEach((button) => {
      button.hidden = events.length === 0;
    });
    updateReceiptsBadge(round);
    receiptsList.replaceChildren();

    events.slice(0, 40).forEach((event) => {
      const row = document.createElement('div');
      row.className = 'receipt-row';

      const title = document.createElement('strong');
      title.textContent = roundHistoryTitle(round, event);

      const meta = document.createElement('small');
      const pieces = [];
      if (event.hole_number) pieces.push(`HOLE ${event.hole_number}`);
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
  };

  const renderRoundHistoryPage = (round) => {
    if (!roundHistoryPage) return;

    currentLobbyRound = round;
    if (startRoundForm) startRoundForm.hidden = true;
    if (joinRoundForm) joinRoundForm.hidden = true;
    if (lobbyPanel) lobbyPanel.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = true;
    if (roundEndPanel) roundEndPanel.hidden = true;
    if (liveMorePanel) liveMorePanel.hidden = true;
    if (liveNavMore) liveNavMore.textContent = 'MORE';

    roundHistoryPage.hidden = false;
    if (roundFlowTitle) roundFlowTitle.textContent = 'ROUND HISTORY';
    renderReceipts(round);
  };

  const openRoundHistoryPage = () => {
    if (!currentLobbyRound || !roundHistoryPage) return;

    roundHistoryOpen = true;
    renderRoundHistoryPage(currentLobbyRound);
    receiptsList?.scrollTo({ top: 0 });
    void markReceiptsSeen(currentLobbyRound);
  };

  const closeRoundHistoryPage = () => {
    if (!currentLobbyRound) return;
    roundHistoryOpen = false;
    if (roundHistoryPage) roundHistoryPage.hidden = true;

    if (currentLobbyRound.status === 'completed') {
      renderRoundEnd(currentLobbyRound);
    } else {
      renderLiveRound(currentLobbyRound);
    }
  };

  roundHistoryOpenButtons.forEach((button) => {
    button.addEventListener('click', openRoundHistoryPage);
  });
  roundHistoryBack?.addEventListener('click', closeRoundHistoryPage);

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
    if (roundHistoryOpen) {
      renderRoundHistoryPage(round);
      return;
    }

    stopLobbyBanterRotation();
    resetLiveMomentState();
    closeScoreResponseSheet();
    if (bagModal) bagModal.hidden = true;
    if (scrambleContributionPanel) scrambleContributionPanel.hidden = true;
    if (advanceWarningPanel) advanceWarningPanel.hidden = true;
    if (finishIncompletePanel) finishIncompletePanel.hidden = true;
    if (roundSettingsPanel) roundSettingsPanel.hidden = true;
    document.body.classList.remove('score-response-open');

    currentLobbyRound = round;
    viewedRoutePosition = null;
    finishIncompletePending = false;

    if (startRoundForm) startRoundForm.hidden = true;
    if (joinRoundForm) joinRoundForm.hidden = true;
    if (lobbyPanel) lobbyPanel.hidden = true;
    if (liveRoundPanel) liveRoundPanel.hidden = true;
    roundFlowCardGame?.classList.remove('is-live-round');
    if (roundEndPanel) roundEndPanel.hidden = false;
    if (roundHistoryPage) roundHistoryPage.hidden = true;
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
    if (roundHistoryOpen) {
      renderRoundHistoryPage(round);
      return;
    }

    stopLobbyBanterRotation();
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
    const shouldPlayHoleTransition = Boolean(
      previousRound
      && String(previousRound.id) === String(round.id)
      && Number(livePosition) === Number(previousLivePosition) + 1
      && round.status === 'active'
    );
    const length = routeLength(round);
    const wasFollowingLive = (
      viewedRoutePosition === null
      || !previousRound
      || Number(viewedRoutePosition) === previousLivePosition
    );

    if (shouldPlayHoleTransition) {
      scrambleContributionComposerOpen = false;
    }

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
    if (roundHistoryPage) roundHistoryPage.hidden = true;
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
    const canUseLiveSocial = (
      viewerIsActivePlayer(round)
      && round.status === 'active'
      && viewingLive
    );
    const scrambleTeamScore = (
      round.mode === 'scramble'
      && viewingLive
      && findScore(round, livePosition)
    );
    if (scrambleTeamScore && viewerIsActivePlayer(round)) {
      scrambleContributionComposerOpen = true;
    }
    if (liveCalloutButton) liveCalloutButton.hidden = !canUseLiveSocial;
    if (scrambleContributionOpen) {
      scrambleContributionOpen.hidden = !(
        canUseLiveSocial && round.mode === 'scramble'
      );
    }

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
      const stillMissing = missingScoresAtPosition(round, livePosition);
      const canAdvanceLive = (
        viewerIsActivePlayer(round)
        && round.status === 'active'
        && viewingLive
        && livePosition < length
        && stillMissing.length > 0
      );
      advanceLiveHole.hidden = !canAdvanceLive;
      advanceLiveHole.disabled = false;
    }

    if (finishRoundButton) {
      const canFinishFromFooter = (
        viewerIsActivePlayer(round)
        && round.status === 'active'
        && viewingLive
        && livePosition === length
      );
      finishRoundButton.hidden = !canFinishFromFooter || finishIncompletePending;
      finishRoundButton.disabled = false;
      finishRoundButton.textContent = 'FINISH ROUND';
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
            ? `${actions} ACTION${actions === 1 ? '' : 'S'} HAPPENED AFTER YOU CLAIMED THIS PLAYER. THAT ROUND HISTORY STAYS ATTRIBUTED TO YOUR ACCOUNT.`
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
    renderLiveHoleStats(round);
    if (liveNavMore) {
      liveNavMore.textContent =
        liveMorePanel && !liveMorePanel.hidden ? 'CLOSE MORE' : 'MORE';
    }
    renderLatestPresentation(round);
    renderReceipts(round);
    queueNewScoreAnnouncements(round);
    void loadTransitionAssets();

    if (shouldPlayHoleTransition) {
      void playHoleTransition(
        round,
        previousLivePosition,
        livePosition
      );
    }

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
    if (finishIncompletePanel) {
      finishIncompletePanel.hidden = !(
        canFinish
        && finishIncompletePending
        && !resultsComplete
      );
      if (!finishIncompletePanel.hidden) {
        window.requestAnimationFrame(() => {
          finishIncompletePanel.scrollIntoView({
            behavior: 'smooth',
            block: 'end',
          });
        });
      }
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
    if (roundHistoryOpen) {
      renderRoundHistoryPage(round);
      return;
    }

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
    if (roundHistoryPage) roundHistoryPage.hidden = true;
    if (scrambleContributionPanel) scrambleContributionPanel.hidden = true;
    if (finishRoundButton) finishRoundButton.hidden = true;
    if (lobbyPanel) lobbyPanel.hidden = false;
    if (roundFlowTitle) roundFlowTitle.textContent = 'LOBBY';
    if (lobbyCode) lobbyCode.textContent = round.active_code || '----';

    const modeLabel =
      round.mode === 'scramble' ? 'WE SUCK TOGETHER' : 'EVERY ASSHOLE FOR THEMSELVES';
    const place = round.course?.name || round.free_play_name || 'Course round';
    if (lobbySummary) {
      lobbySummary.replaceChildren();

      const addSummaryLine = (label, value, className) => {
        const line = document.createElement('div');
        line.className = 'lobby-summary-line ' + className;

        const key = document.createElement('span');
        key.textContent = label;

        const copy = document.createElement('strong');
        copy.textContent = value;

        line.append(key, copy);
        lobbySummary.append(line);
      };

      addSummaryLine('FORMAT', modeLabel, 'is-format');
      addSummaryLine('ROUND', String(round.hole_count) + ' HOLES', 'is-holes');
      addSummaryLine('COURSE', place, 'is-course');

      if (round.mode === 'scramble' && round.scramble_tee_name) {
        addSummaryLine(
          'TEAM TEE',
          String(round.scramble_tee_name),
          'is-team-tee'
        );
      }
    }

    if (lobbyParticipants) {
      lobbyParticipants.replaceChildren();
      (round.participants || []).forEach((participant) => {
        const row = document.createElement('div');
        row.className = 'lobby-person';

        const name = document.createElement('span');
        name.textContent = participant.display_name || 'Unknown golfer';

        const meta = document.createElement('div');
        meta.className = 'lobby-person-meta';

        const addDetail = (text) => {
          const detail = document.createElement('small');
          detail.className = 'lobby-person-detail';
          detail.textContent = text;
          meta.append(detail);
        };

        addDetail(String(participant.role || 'player').toUpperCase());

        if (participant.round_only) {
          addDetail('OFFLINE');
        }

        if (round.mode === 'individual') {
          addDetail(
            participant.tee_name
              ? `${participant.tee_name} TEE`
              : 'NO TEE'
          );

          const handicap = (
            participant.round_handicap
            ?? participant.handicap_index
          );
          addDetail(
            handicap === null || handicap === undefined
              ? 'NO HANDICAP'
              : `HCP ${handicap}`
          );
        }

        row.append(name, meta);
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

    if (roundHistoryOpen) {
      renderRoundHistoryPage(round);
      return round;
    }

    renderRoundState(round);
    refreshOpenScoreResponseSheet(round);
    return round;
  };

  const refreshLobby = refreshRound;

  const liveScoreDraftInProgress = () => {
    const active = document.activeElement;
    if (active?.classList?.contains('live-score-input')) return true;
    return Boolean(
      liveScoreArea?.querySelector(
        '.live-score-input[data-draft-dirty="true"]'
      )
    );
  };

  const liveScoreSocialInteractionInProgress = () => {
    const active = document.activeElement;
    if (active?.closest?.('.live-score-social-panel')) return true;
    return Boolean(
      scoreResponseSheetBody?.querySelector(
        '.live-score-social-panel [data-social-draft-dirty="true"]'
      )
    );
  };

  const startLobbyPolling = (code) => {
    if (lobbyRefreshTimer) window.clearInterval(lobbyRefreshTimer);
    lobbyRefreshTimer = window.setInterval(async () => {
      if (!roundFlowModal || roundFlowModal.hidden || !currentLobbyRound) return;
      // Do not destroy live score controls while somebody is entering a
      // score or using Reactions / Challenges. The periodic render rebuilds
      // the score-card DOM, which otherwise closes <details>, drops focus,
      // and wipes whatever is being typed on iOS.
      if (
        liveScoreDraftInProgress()
        || liveScoreSocialInteractionInProgress()
      ) return;
      try {
        await refreshRound(code);
      } catch (_error) {
        // A manual action will surface useful errors. Polling stays quiet.
      }
    }, 3000);
  };

  startRoundButton?.addEventListener('click', () => showRoundPanel('start'));
  joinRoundButton?.addEventListener('click', () => {
    resetInviteJoinUi({ clearToken: true });
    showRoundPanel('join');
    void loadUnfinishedRounds();
  });
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
  startRoundForm?.querySelectorAll('input[name="course_hole_count"]').forEach(
    (radio) => radio.addEventListener('change', renderRoutePreview)
  );

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
        // Late-start holes remain planned so live play can optionally backfill them.
        prior_holes_mode: 'backfill',
        net_scoring_enabled: (
          mode === 'individual'
          && individualScoring === 'net'
        ),
      };

      body.course_hole_count = selectedPhysicalHoleCount();

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
    const participant = await requestJson('/api/rounds/join', {
      method: 'POST',
      body: {
        code,
        role,
        tee_name: teeName || null,
      },
    });

    if (String(participant?.role || '') !== String(role)) {
      throw new Error(
        'Round role mismatch. Rejoin using your existing role.'
      );
    }

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

  const resetJoinPreviewState = () => {
    pendingJoinPreview = null;
    pendingClaimJoin = null;
    if (claimPlayerPanel) claimPlayerPanel.hidden = true;
    if (claimPlayerList) claimPlayerList.replaceChildren();
    if (joinTeeField) joinTeeField.hidden = true;
    if (joinTeeSelect) joinTeeSelect.replaceChildren();
    if (joinRoundSubmit) {
      joinRoundSubmit.hidden = false;
      joinRoundSubmit.textContent = 'LET ME INTO THIS MESS';
    }
  };

  const loadUnfinishedRounds = async () => {
    if (!unfinishedRoundsPanel || !unfinishedRoundsList) return;

    unfinishedRoundsPanel.hidden = true;
    unfinishedRoundsList.replaceChildren();

    try {
      const payload = await requestJson('/api/rounds/unfinished');
      const rounds = Array.isArray(payload?.rounds) ? payload.rounds : [];
      if (!rounds.length) return;

      rounds.forEach((round) => {
        const row = document.createElement('section');
        row.className = 'unfinished-round-card';

        const copy = document.createElement('div');
        copy.className = 'unfinished-round-copy';

        const name = document.createElement('strong');
        name.textContent = round.display_name || 'Golf';

        const meta = document.createElement('small');
        const stateLabel = round.status === 'setup' ? 'LOBBY' : 'IN PROGRESS';
        const holeLabel = round.status === 'active'
          ? ` • HOLE ${round.current_hole || round.current_route_position || 1}`
          : '';
        meta.textContent = [
          stateLabel + holeLabel,
          `CODE ${round.active_code || '----'}`,
          String(round.mode || '').toUpperCase(),
        ].filter(Boolean).join(' • ');

        copy.append(name, meta);

        const actions = document.createElement('div');
        actions.className = 'unfinished-round-actions';

        const resume = document.createElement('button');
        resume.type = 'button';
        resume.className = 'unfinished-round-resume';
        resume.textContent = 'RESUME';
        resume.addEventListener('click', async () => {
          resume.disabled = true;
          setRoundFlowMessage('');
          try {
            const exactRound = await requestJson(
              `/api/rounds/${round.id}`
            );
            renderRoundState(exactRound);
            startLobbyPolling(exactRound.active_code);
          } catch (error) {
            await loadUnfinishedRounds();
            setRoundFlowMessage(
              error.message || 'That unfinished round is no longer available.'
            );
          } finally {
            resume.disabled = false;
          }
        });

        const remove = document.createElement('button');
        remove.type = 'button';
        remove.className = 'unfinished-round-delete';
        remove.textContent = 'DELETE';
        remove.addEventListener('click', async () => {
          remove.disabled = true;
          setRoundFlowMessage('');
          try {
            await requestJson(
              `/api/rounds/${round.id}/unfinished`,
              { method: 'DELETE' }
            );
            row.remove();
            if (!unfinishedRoundsList.children.length) {
              unfinishedRoundsPanel.hidden = true;
            }
          } catch (error) {
            setRoundFlowMessage(error.message);
            remove.disabled = false;
          }
        });

        actions.append(resume, remove);
        row.append(copy, actions);
        unfinishedRoundsList.append(row);
      });

      unfinishedRoundsPanel.hidden = false;
    } catch (_error) {
      unfinishedRoundsPanel.hidden = true;
      unfinishedRoundsList.replaceChildren();
    }
  };

  const syncJoinCode = () => {
    const code = joinCodeDigits
      .map((input) => String(input.value || '').replace(/\D/g, '').slice(-1))
      .join('');
    if (joinRoundCode) joinRoundCode.value = code;
    resetJoinPreviewState();
    return code;
  };

  const fillJoinCodeDigits = (rawValue, startIndex = 0) => {
    const digits = String(rawValue || '').replace(/\D/g, '');
    if (!digits) return syncJoinCode();

    let writeIndex = Math.max(0, Math.min(joinCodeDigits.length - 1, startIndex));
    digits.split('').forEach((digit) => {
      if (!joinCodeDigits[writeIndex]) return;
      joinCodeDigits[writeIndex].value = digit;
      writeIndex += 1;
    });

    const code = syncJoinCode();
    const nextEmpty = joinCodeDigits.find((input) => !input.value);
    (nextEmpty || joinCodeDigits[joinCodeDigits.length - 1])?.focus();
    return code;
  };

  joinRoundForm?.querySelectorAll('input[name="role"]').forEach((radio) => {
    radio.addEventListener('change', () => {
      resetJoinPreviewState();
      void loadRandomJoinMini(radio.value);
    });
  });

  joinCodeDigits.forEach((input, index) => {
    input.addEventListener('focus', () => input.select());

    input.addEventListener('input', () => {
      const digits = String(input.value || '').replace(/\D/g, '');
      if (digits.length > 1) {
        input.value = '';
        fillJoinCodeDigits(digits, index);
        return;
      }

      input.value = digits.slice(-1);
      syncJoinCode();
      if (input.value && joinCodeDigits[index + 1]) {
        joinCodeDigits[index + 1].focus();
      }
    });

    input.addEventListener('keydown', (event) => {
      if (event.key === 'Backspace' && !input.value && joinCodeDigits[index - 1]) {
        event.preventDefault();
        joinCodeDigits[index - 1].value = '';
        syncJoinCode();
        joinCodeDigits[index - 1].focus();
        return;
      }

      if (event.key === 'ArrowLeft' && joinCodeDigits[index - 1]) {
        event.preventDefault();
        joinCodeDigits[index - 1].focus();
      }

      if (event.key === 'ArrowRight' && joinCodeDigits[index + 1]) {
        event.preventDefault();
        joinCodeDigits[index + 1].focus();
      }
    });

    input.addEventListener('paste', (event) => {
      const digits = event.clipboardData?.getData('text')?.replace(/\D/g, '') || '';
      if (!digits) return;
      event.preventDefault();
      fillJoinCodeDigits(digits, index);
    });
  });

  joinRoundForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    setRoundFlowMessage('');

    if (
      pendingRoundInviteToken
      && pendingRoundInvitePreview
      && joinRoundForm.classList.contains('is-invite-acceptance')
    ) {
      const teeName = String(joinTeeSelect?.value || '').trim();
      if (pendingRoundInvitePreview.requires_tee && !teeName) {
        setRoundFlowMessage('Pick your tee before joining this round.');
        joinTeeSelect?.focus();
        return;
      }

      setFormBusy(joinRoundForm, true);
      try {
        await acceptPendingRoundInvite(teeName);
      } catch (error) {
        setRoundFlowMessage(error.message);
      } finally {
        setFormBusy(joinRoundForm, false);
      }
      return;
    }

    const values = new FormData(joinRoundForm);
    const code = String(values.get('code') || '').trim();
    const role = String(values.get('role') || 'player');

    if (!/^\d{4}$/.test(code)) {
      setRoundFlowMessage('ENTER ALL FOUR DIGITS.');
      (joinCodeDigits.find((input) => !input.value) || joinCodeDigits[0])?.focus();
      return;
    }

    setFormBusy(joinRoundForm, true);

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

  roundInviteButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const role = String(button.dataset.inviteRole || '');
      if (!['player', 'spectator'].includes(role)) return;
      void shareRoundInvite(role, button);
    });
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
    setRoundFlowMessage('Use the hole arrows to fix the missing scores, then come back here.');
  });

  finishIncompleteButton?.addEventListener('click', async () => {
    await completeRound(true);
  });

  holePrev?.addEventListener('click', () => {
    if (!currentLobbyRound || viewedRoutePosition === null) return;
    if (Number(viewedRoutePosition) <= 1) return;
    parEditorOpen = false;
    skippedScrambleContributionPromptKey = '';
    viewedRoutePosition = Number(viewedRoutePosition) - 1;
    renderLiveRound(currentLobbyRound);
  });

  backToLive?.addEventListener('click', () => {
    if (!currentLobbyRound) return;
    skippedScrambleContributionPromptKey = '';
    viewedRoutePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    renderLiveRound(currentLobbyRound);
  });

  holeNext?.addEventListener('click', () => {
    if (!currentLobbyRound || viewedRoutePosition === null) return;
    skippedScrambleContributionPromptKey = '';
    const length = routeLength(currentLobbyRound);
    const viewed = Number(viewedRoutePosition);
    if (viewed >= length) return;

    parEditorOpen = false;
    viewedRoutePosition = viewed + 1;
    renderLiveRound(currentLobbyRound);
  });

  const advanceSharedLiveHole = async () => {
    if (!currentLobbyRound || !viewerIsActivePlayer(currentLobbyRound)) {
      return false;
    }

    const length = routeLength(currentLobbyRound);
    const livePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    if (livePosition >= length) return false;

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
      return true;
    } catch (error) {
      setRoundFlowMessage(error.message);
      if (advanceLiveHole) advanceLiveHole.disabled = false;
      if (advanceWarningGo) advanceWarningGo.disabled = false;
      return false;
    }
  };

  scrambleContributionSkip?.addEventListener('click', async () => {
    if (!currentLobbyRound) return;

    const livePosition = Number(
      currentLobbyRound.current_route_position
      || currentLobbyRound.current_hole
      || 1
    );
    const finishingScoredScrambleHole = (
      currentLobbyRound.mode === 'scramble'
      && Number(viewedRoutePosition) === livePosition
      && Boolean(findScore(currentLobbyRound, livePosition))
    );

    scrambleContributionComposerOpen = false;
    if (scrambleContributionPanel) {
      scrambleContributionPanel.hidden = true;
    }

    if (!finishingScoredScrambleHole) return;

    if (scrambleContributionSkip) {
      scrambleContributionSkip.disabled = true;
    }
    const advanced = await advanceSharedLiveHole();
    if (!advanced) {
      scrambleContributionComposerOpen = true;
      renderScrambleContributions(currentLobbyRound, livePosition);
      if (scrambleContributionSkip) {
        scrambleContributionSkip.disabled = false;
      }
    }
  });

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
          participant.role === 'player'
          && String(participant.id) !== String(currentLobbyRound.viewer_participant_id)
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
    currentBagReplyToEventId = null;
    currentBagRoutePosition = null;
    currentBagLockedTargetId = null;
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
    if (bagTargetSelect) bagTargetSelect.disabled = false;
    setBagMessage('');
  };

  const openBag = (
    action,
    {
      replyToEventId = null,
      routePosition = null,
      targetParticipantId = null,
    } = {}
  ) => {
    if (
      !bagModal
      || !currentLobbyRound
      || currentLobbyRound.status !== 'active'
      || !viewerIsActivePlayer(currentLobbyRound)
      || !['callout', 'excuse'].includes(action)
      || (action === 'excuse' && !replyToEventId)
    ) {
      return;
    }

    resetBagComposer();
    currentBagReplyToEventId = replyToEventId ? String(replyToEventId) : null;
    currentBagRoutePosition = routePosition ? Number(routePosition) : null;
    currentBagLockedTargetId = targetParticipantId
      ? String(targetParticipantId)
      : null;

    if (action === 'callout') {
      populateBagTargets();
      if (currentBagLockedTargetId && bagTargetSelect) {
        bagTargetSelect.value = currentBagLockedTargetId;
        bagTargetSelect.disabled = true;
      }
    } else if (bagTargetSelect) {
      bagTargetSelect.replaceChildren();
    }
    bagModal.hidden = false;
    document.body.classList.add('modal-open');
    configureBagAction(action);
    bagClose?.focus();
  };

  const closeBag = () => {
    if (!bagModal) return;
    bagModal.hidden = true;
    resetBagComposer();
    document.body.classList.remove('modal-open');
  };

  const configureBagAction = (action) => {
    if (!bagForm) return;
    currentBagAction = action;
    if (bagActions) bagActions.hidden = true;
    bagForm.hidden = false;
    setBagMessage('');

    const config = {
      callout: {
        title: 'CALL OUT',
        submit: 'SEND IT',
        target: true,
        situation: true,
        textLabel: 'ADD YOUR OWN SHIT',
        placeholder: 'Optional. Make it personal.',
        requiredText: false,
      },
      excuse: {
        title: 'MAKE EXCUSE',
        submit: 'FILE THIS BULLSHIT',
        target: false,
        excuse: true,
        textLabel: 'YOUR OFFICIAL STATEMENT',
        placeholder: 'Optional additional bullshit.',
        requiredText: false,
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

  const sendSocialEvent = async (
    type,
    data = {},
    {
      replyToEventId = null,
      routePosition = null,
    } = {}
  ) => {
    if (!currentLobbyRound) return;
    const body = {
      type,
      hole: (
        routePosition
        || currentLobbyRound.current_route_position
        || currentLobbyRound.current_hole
      ),
      data,
    };
    if (replyToEventId) {
      body.reply_to_event_id = replyToEventId;
    }
    return requestJson(
      `/api/rounds/${currentLobbyRound.id}/events`,
      {
        method: 'POST',
        body,
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

  lobbyBanterForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!currentLobbyRound || currentLobbyRound.status !== 'setup') return;
    const message = String(lobbyBanterInput?.value || '').trim();
    if (!message) return;

    if (lobbyBanterSend) lobbyBanterSend.disabled = true;
    setRoundFlowMessage('');
    try {
      await sendSocialEvent('open_mic', { message });
      if (lobbyBanterInput) lobbyBanterInput.value = '';
      await refreshLobby(currentLobbyRound.active_code);
    } catch (error) {
      setRoundFlowMessage(error.message);
    } finally {
      if (lobbyBanterSend) lobbyBanterSend.disabled = false;
    }
  });

  liveBanterExpand?.addEventListener('click', () => {
    if (!liveBanterPanel) return;
    const opening = !liveBanterPanel.classList.contains('is-fullscreen');
    liveBanterPanel.classList.toggle('is-fullscreen', opening);
    liveBanterExpand.textContent = opening ? 'CLOSE' : 'FULL SCREEN';
    liveBanterExpand.setAttribute('aria-pressed', opening ? 'true' : 'false');
    liveBanterExpand.setAttribute(
      'aria-label',
      opening
        ? 'Close full-screen round banter'
        : 'Open full-screen round banter'
    );
  });

  scoreResponseClose?.addEventListener('click', closeScoreResponseSheet);
  scoreResponseModal?.addEventListener('click', (event) => {
    if (event.target === scoreResponseModal) closeScoreResponseSheet();
  });

  scrambleContributionOpen?.addEventListener('click', () => {
    if (
      !currentLobbyRound
      || currentLobbyRound.mode !== 'scramble'
      || viewedRoutePosition === null
    ) return;
    scrambleContributionComposerOpen = true;
    renderScrambleContributions(
      currentLobbyRound,
      Number(viewedRoutePosition)
    );
  });

  liveNavMore?.addEventListener('click', () => {
    if (!liveMorePanel) return;
    const opening = liveMorePanel.hidden;
    liveMorePanel.hidden = !opening;
    liveNavMore.textContent = opening ? 'CLOSE MORE' : 'MORE';
    if (opening) {
      liveMorePanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  liveEditPar?.addEventListener('click', () => {
    if (!currentLobbyRound || viewedRoutePosition === null) return;
    parEditorOpen = true;
    if (liveMorePanel) liveMorePanel.hidden = true;
    renderLiveRound(currentLobbyRound);
    window.requestAnimationFrame(() => {
      parInput?.focus();
      parForm?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  liveCalloutButton?.addEventListener('click', () => openBag('callout'));
  bagClose?.addEventListener('click', closeBag);
  bagModal?.addEventListener('click', (event) => {
    if (event.target === bagModal) closeBag();
  });
  bagFormCancel?.addEventListener('click', closeBag);

  bagForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!currentLobbyRound || !currentBagAction) return;

    const message = String(bagTextInput?.value || '').trim();
    if (bagTextInput?.required && !message) {
      setBagMessage('You opened your mouth. Finish the thought.');
      return;
    }

    const data = {};
    if (
      currentBagAction === 'callout'
      && !bagTargetField?.hidden
      && bagTargetSelect?.value
    ) {
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
      await sendSocialEvent(
        currentBagAction,
        data,
        {
          replyToEventId: currentBagReplyToEventId,
          routePosition: currentBagRoutePosition,
        }
      );
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
      populateProfileRelationship(preferences);
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

    const spouseType = String(settingsSpouseType?.value || '').trim();
    if (!['wife', 'husband', 'not_married'].includes(spouseType)) {
      setSettingsMessage(
        'Just fucking answer the question, snowflake — wife, husband, or not married.'
      );
      settingsSpouseType?.focus();
      return;
    }

    const patch = {
      mini_mascots_enabled:
        settingsForm.elements.mini_mascots_enabled.checked,
      trash_talk_enabled:
        settingsForm.elements.trash_talk_enabled.checked,
      spouse_type: spouseType,
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
      populateProfileRelationship(preferences);
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
