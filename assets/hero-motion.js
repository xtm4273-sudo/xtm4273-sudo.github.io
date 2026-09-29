// Render the same silent clip without HTMLMediaElement autoplay permissions.
export async function startHeroMotion({canvas, image, getBytes, onReady, onError}) {
  let active = true, disposed = false, decoder, raf = 0;
  let frames = [], packetIndex = 0, pendingFrames = 0;
  let clockStart = null, pausedAt = null, flushed = false, cycle = 0;
  let ready = false, imageMode = false, config, manifest, bytes;
  const context = canvas.getContext('2d', {alpha:false, desynchronized:true});
  function clearFrames() { frames.forEach(frame => frame.close()); frames = []; }
  function stopDecoder() {
    cancelAnimationFrame(raf); cycle++;
    if (decoder && decoder.state !== 'closed') decoder.close();
    clearFrames();
  }
  function showImage() {
    if (disposed || imageMode) return;
    imageMode = true; stopDecoder(); canvas.hidden = true;
    image.onload = () => {
      if (disposed) return;
      image.hidden = !active; onReady();
    };
    image.onerror = onError;
    image.src = 'assets/wechat-compat.webp';
  }
  function pump() {
    if (disposed || imageMode || !active) return;
    // Keep at most eight decoded/in-flight frames, not all 121 frames in memory.
    while (packetIndex < manifest.packets.length && pendingFrames + frames.length < 8) {
      const [offset, length, timestamp, duration, key] = manifest.packets[packetIndex++];
      pendingFrames++;
      decoder.decode(new EncodedVideoChunk({
        type:key ? 'key' : 'delta', timestamp, duration,
        data:new Uint8Array(bytes, offset, length)
      }));
    }
    if (packetIndex === manifest.packets.length && !flushed) {
      flushed = true;
      const currentCycle = cycle;
      decoder.flush().catch(() => { if (cycle === currentCycle) showImage(); });
    }
  }
  function resetCycle() {
    cycle++; decoder.reset(); decoder.configure(config);
    clearFrames(); packetIndex = 0; pendingFrames = 0; flushed = false;
    clockStart = null;
  }
  function tick(now) {
    if (!active || disposed || imageMode) return;
    try {
      if (clockStart === null && frames.length) clockStart = now;
      if (clockStart !== null && (now - clockStart) * 1000 >= manifest.duration) resetCycle();
      if (clockStart !== null) {
        const elapsed = (now - clockStart) * 1000;
        let latest;
        while (frames.length && frames[0].timestamp <= elapsed) {
          if (latest) latest.close();
          latest = frames.shift();
        }
        if (latest) {
          context.drawImage(latest, 0, 0, canvas.width, canvas.height);
          latest.close();
          if (!ready) { ready = true; canvas.hidden = false; onReady(); }
        }
      }
      pump(); raf = requestAnimationFrame(tick);
    } catch { showImage(); }
  }
  const controller = {
    setActive(value) {
      if (disposed || active === value) return;
      active = value;
      if (imageMode) { image.hidden = !value || !image.complete; return; }
      if (!value) { pausedAt = performance.now(); cancelAnimationFrame(raf); }
      else {
        if (clockStart !== null && pausedAt !== null) clockStart += performance.now() - pausedAt;
        pausedAt = null; raf = requestAnimationFrame(tick);
      }
    },
    dispose() { disposed = true; stopDecoder(); image.removeAttribute('src'); }
  };
  try {
    if (!window.VideoDecoder || !context) { showImage(); return controller; }
    const response = await fetch('assets/ip-home-mobile-v3.frames.json');
    if (!response.ok) throw new Error('Frame manifest unavailable');
    manifest = await response.json();
    config = {
      codec:manifest.codec, codedWidth:manifest.width, codedHeight:manifest.height,
      description:new Uint8Array(manifest.description)
    };
    const support = await VideoDecoder.isConfigSupported(config);
    if (!support.supported) { showImage(); return controller; }
    bytes = await getBytes();
    canvas.width = manifest.width; canvas.height = manifest.height;
    decoder = new VideoDecoder({
      output(frame) {
        if (disposed || imageMode) { frame.close(); return; }
        pendingFrames--; frames.push(frame);
      },
      error:showImage
    });
    decoder.configure(config); pump(); raf = requestAnimationFrame(tick);
  } catch { showImage(); }
  return controller;
}
