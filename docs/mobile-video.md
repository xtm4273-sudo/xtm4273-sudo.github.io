# Mobile homepage video

The supplied five-second source is 4,111,742 bytes, 1280×720 / 24 fps,
approximately 6.47 Mbps including audio. Its MP4 `moov` index is at the end.
The 4,220,326-byte character sheet previously loaded concurrently with the video.
At 1.6 Mbps, 150 ms RTT and 4× CPU slowdown, the previous page started at
5.33 seconds, then repeatedly stalled (including waits of 3.71 and 6.45 seconds).

## Delivery

- `ip-home-mobile-v3.mp4`: 587,577 bytes, 1280×720 / 24 fps, H.264 Main,
  yuv420p, no audio. Encoded for mobile bandwidth; it is not a lossless copy.
- `ip-home-desktop-v3.mp4`: original video stream copied without re-encoding,
  with audio removed and the index moved to the front. Decoded-frame hashes
  match the supplied source.
- Both files use `+faststart`. A coarse pointer or viewport up to 767px selects
  the mobile version once, before downloading any video.
- Ordinary mobile browsers buffer this small loop once, then play a local Blob URL. This avoids
  network buffering during playback or subsequent loops. If fetching the Blob
  fails, native MP4 loading is the fallback.
- The original character sheet starts loading after the mobile video is buffered,
  preserving its image quality and keeping it off the video's critical path.
- Android WeChat renders the same 720p clip with WebCodecs and a canvas,
  independently of HTML video autoplay permission. Other browsers switch to
  this renderer if native playback is rejected. No play button is displayed.
- The generated packet manifest is 3.8 KB; there is no third-party decoder or
  demuxing bundle. At most eight decoded/in-flight frames are held at once,
  and every rendered/discarded VideoFrame is explicitly closed.
- WebViews without a supported VideoDecoder automatically use
  `wechat-compat.webp` (640×360, 24 fps, 1,985,450 bytes). This compatibility
  image needs more bandwidth and has lower resolution than the primary path,
  but loops automatically without a video gesture requirement.
- Native video and canvas drawing pause offscreen/in hidden tabs. The legacy
  animated image is hidden when not visible; its playback is browser-managed.

## Reproduction

```sh
ffmpeg -i assets/ip-home-v2.mp4 -map 0:v:0 -an -c:v libx264 -preset slow -crf 24 -maxrate 900k -bufsize 900k -profile:v main -level 3.1 -pix_fmt yuv420p -g 48 -movflags +faststart -map_metadata -1 assets/ip-home-mobile-v3.mp4
ffmpeg -i assets/ip-home-v2.mp4 -map 0:v:0 -c:v copy -an -movflags +faststart -map_metadata -1 assets/ip-home-desktop-v3.mp4
python scripts/build_motion_manifest.py
ffmpeg -i assets/ip-home-v2.mp4 -an -vf scale=640:-2 -c:v libwebp_anim -lossless 0 -quality 50 -compression_level 6 -loop 0 assets/wechat-compat.webp
```

With HTMLMediaElement.play() forced to reject, the canvas renderer started
without user gestures at 4.82 seconds under the same cold-cache throttle.
It rendered 287 frames over the next 12 seconds, with a maximum frame gap of
121 ms including loop boundaries. Both decoder and legacy-image tests verify
changing pixels, continued looping, absence of play buttons, and zero page
errors. Ordinary desktop/mobile native playback is also tested.

These measurements use Chromium mobile emulation, not a physical Android
WeChat device; actual startup also depends on the user's network and WebView.

References: [FFmpeg faststart](https://ffmpeg.org/ffmpeg-formats.html),
[WebCodecs video processing](https://developer.chrome.com/docs/web-platform/best-practices/webcodecs),
[WebP animation](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types#webp_image).
