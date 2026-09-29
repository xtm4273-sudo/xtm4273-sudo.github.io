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
- Mobile buffers this small loop once, then plays a local Blob URL. This avoids
  network buffering during playback or subsequent loops. If fetching the Blob
  fails, native MP4 loading is the fallback.
- The original character sheet starts loading after the mobile video is buffered,
  preserving its image quality and keeping it off the video's critical path.
- Playback remains muted and inline. Touch/pointer gestures and
  `WeixinJSBridgeReady` retry playback. A play button appears only if autoplay
  is denied; the removed pause control stays removed.
- Offscreen and hidden-tab playback pauses and resumes when visible again.

## Reproduction

```sh
ffmpeg -i assets/ip-home-v2.mp4 -map 0:v:0 -an -c:v libx264 -preset slow -crf 24 -maxrate 900k -bufsize 900k -profile:v main -level 3.1 -pix_fmt yuv420p -g 48 -movflags +faststart -map_metadata -1 assets/ip-home-mobile-v3.mp4
ffmpeg -i assets/ip-home-v2.mp4 -map 0:v:0 -c:v copy -an -movflags +faststart -map_metadata -1 assets/ip-home-desktop-v3.mp4
```

Initial optimized measurement under the same cold-cache throttle: first play
at 4.77 seconds, no rebuffering over the following 12 seconds. Loop boundary
events were 0–1 ms. Tests cover autoplay denial, touch recovery, bridge-ready
recovery, offscreen pause/resume and desktop/mobile layouts.

These measurements use Chromium mobile emulation, not a physical Android
WeChat device; actual startup also depends on the user's network and WebView.

References: [FFmpeg faststart](https://ffmpeg.org/ffmpeg-formats.html),
[WebKit muted inline autoplay](https://webkit.org/blog/6784/new-video-policies-for-ios/).
