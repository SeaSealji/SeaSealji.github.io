(() => {
  const root = document.documentElement;
  const button = document.querySelector('.theme-toggle');
  const saved = localStorage.getItem('theme');
  const preferred = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  const apply = (theme) => {
    root.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#111816' : '#f7f4ee';
    button?.setAttribute('aria-label', theme === 'dark' ? '切换浅色模式' : '切换深色模式');
  };
  apply(saved || preferred);
  button?.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', next);
    apply(next);
  });
})();

(() => {
  const dropdowns = [...document.querySelectorAll('.nav-dropdown')];
  if (!dropdowns.length) return;
  document.addEventListener('click', (event) => {
    dropdowns.forEach((dropdown) => {
      if (!dropdown.contains(event.target)) dropdown.open = false;
    });
  });
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    const active = dropdowns.find((dropdown) => dropdown.open);
    dropdowns.forEach((dropdown) => { dropdown.open = false; });
    active?.querySelector('summary')?.focus();
  });
})();

(() => {
  const carousels = [...document.querySelectorAll('[data-device-carousel]')];
  if (!carousels.length) return;

  carousels.forEach((carousel) => {
    const track = carousel.querySelector('[data-device-track]');
    const previousButton = carousel.querySelector('[data-device-prev]');
    const nextButton = carousel.querySelector('[data-device-next]');
    if (!track || !previousButton || !nextButton) return;

    const updateButtons = () => {
      const maxScroll = Math.max(track.scrollWidth - track.clientWidth, 0);
      previousButton.disabled = track.scrollLeft <= 2;
      nextButton.disabled = track.scrollLeft >= maxScroll - 2;
    };

    const scrollOneCard = (direction) => {
      const card = track.querySelector('.device-card');
      if (!card) return;
      const gap = Number.parseFloat(getComputedStyle(track).columnGap) || 0;
      track.scrollBy({ left: direction * (card.getBoundingClientRect().width + gap), behavior: 'smooth' });
    };

    previousButton.addEventListener('click', () => scrollOneCard(-1));
    nextButton.addEventListener('click', () => scrollOneCard(1));
    track.addEventListener('scroll', updateButtons, { passive: true });
    window.addEventListener('resize', updateButtons);
    updateButtons();
  });
})();

(() => {
  const player = document.querySelector('.music-player');
  if (!player) return;

  const audio = player.querySelector('.player-audio');
  const items = [...player.querySelectorAll('.playlist-item')];
  const playButton = player.querySelector('.player-play');
  const previousButton = player.querySelector('.player-prev');
  const nextButton = player.querySelector('.player-next');
  const progress = player.querySelector('.player-progress');
  const volume = player.querySelector('.player-volume');
  const currentTime = player.querySelector('.player-current');
  const duration = player.querySelector('.player-duration');
  const title = player.querySelector('.player-title');
  const artist = player.querySelector('.player-artist');
  const cover = player.querySelector('.player-cover');
  const listToggle = player.querySelector('.player-list-toggle');
  const playlist = player.querySelector('.player-playlist');
  const listClose = player.querySelector('.playlist-close');
  const status = player.querySelector('.player-status');
  let activeIndex = Math.min(Number(localStorage.getItem('music-track')) || 0, Math.max(items.length - 1, 0));

  const formatTime = (seconds) => {
    if (!Number.isFinite(seconds)) return '0:00';
    const minutes = Math.floor(seconds / 60);
    return `${minutes}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
  };

  const announce = (message) => {
    if (status) status.textContent = message;
  };

  const setPlaying = (playing) => {
    player.classList.toggle('is-playing', playing);
    playButton?.setAttribute('aria-label', playing ? '暂停' : '播放');
    items.forEach((item, index) => {
      const state = item.querySelector('.playlist-state');
      if (state) state.textContent = index === activeIndex && playing ? '播放中' : '播放';
    });
  };

  const loadTrack = (index, shouldPlay = false) => {
    if (!items.length) return;
    activeIndex = (index + items.length) % items.length;
    const item = items[activeIndex];
    audio.src = item.dataset.src;
    title.textContent = item.dataset.title;
    artist.textContent = item.dataset.artist;
    items.forEach((entry, entryIndex) => {
      entry.classList.toggle('is-active', entryIndex === activeIndex);
      entry.setAttribute('aria-current', entryIndex === activeIndex ? 'true' : 'false');
    });
    cover.querySelector('img')?.remove();
    if (item.dataset.cover) {
      const image = document.createElement('img');
      image.src = item.dataset.cover;
      image.alt = '';
      cover.appendChild(image);
    }
    progress.value = 0;
    currentTime.textContent = '0:00';
    duration.textContent = '0:00';
    localStorage.setItem('music-track', String(activeIndex));
    announce(`已选择：${item.dataset.title}`);
    if (shouldPlay) audio.play().catch(() => announce('浏览器暂时无法播放这首音乐。'));
  };

  const togglePlaylist = (open) => {
    const shouldOpen = typeof open === 'boolean' ? open : playlist.hidden;
    playlist.hidden = !shouldOpen;
    player.classList.toggle('playlist-open', shouldOpen);
    listToggle.setAttribute('aria-expanded', String(shouldOpen));
    listToggle.setAttribute('aria-label', shouldOpen ? '关闭播放列表' : '打开播放列表');
    if (shouldOpen) listClose.focus();
  };

  if (items.length) {
    const savedVolume = Number(localStorage.getItem('music-volume'));
    audio.volume = Number.isFinite(savedVolume) && savedVolume >= 0 ? savedVolume : 0.8;
    volume.value = audio.volume;
    loadTrack(activeIndex);

    playButton.addEventListener('click', () => {
      if (audio.paused) audio.play().catch(() => announce('播放失败，请检查音频文件。'));
      else audio.pause();
    });
    previousButton.addEventListener('click', () => loadTrack(activeIndex - 1, true));
    nextButton.addEventListener('click', () => loadTrack(activeIndex + 1, true));
    items.forEach((item, index) => item.addEventListener('click', () => {
      loadTrack(index, true);
      togglePlaylist(false);
    }));
    audio.addEventListener('play', () => setPlaying(true));
    audio.addEventListener('waiting', () => announce('网络缓冲中…'));
    audio.addEventListener('playing', () => announce(`正在播放：${items[activeIndex].dataset.title}`));
    audio.addEventListener('pause', () => setPlaying(false));
    audio.addEventListener('ended', () => loadTrack(activeIndex + 1, true));
    audio.addEventListener('loadedmetadata', () => {
      progress.max = audio.duration || 100;
      duration.textContent = formatTime(audio.duration);
    });
    audio.addEventListener('timeupdate', () => {
      if (!progress.matches(':active')) progress.value = audio.currentTime;
      currentTime.textContent = formatTime(audio.currentTime);
    });
    audio.addEventListener('error', () => {
      setPlaying(false);
      announce('音频加载失败，请确认文件名和格式。');
    });
    progress.addEventListener('input', () => { audio.currentTime = Number(progress.value); });
    volume.addEventListener('input', () => {
      audio.volume = Number(volume.value);
      localStorage.setItem('music-volume', volume.value);
    });
  }

  listToggle.addEventListener('click', () => togglePlaylist());
  listClose.addEventListener('click', () => togglePlaylist(false));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !playlist.hidden) togglePlaylist(false);
  });
})();
