"""Generate a small packet index for the existing 720p H.264 clip. Requires ffprobe."""
from pathlib import Path
import json
import subprocess

root = Path(__file__).resolve().parents[1]
video = root / 'assets/ip-home-mobile-v3.mp4'
raw = json.loads(subprocess.check_output([
    'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_data',
    '-show_entries', 'stream=extradata,width,height:packet=pts_time,duration_time,pos,size,flags',
    '-of', 'json', str(video),
], encoding='utf-8'))
stream = raw['streams'][0]
extra = bytes.fromhex(''.join(
    line.split(':', 1)[1].split('  ')[0].replace(' ', '')
    for line in stream['extradata'].splitlines() if ':' in line
))
packets = [[int(p['pos']), int(p['size']), round(float(p['pts_time']) * 1e6),
            round(float(p['duration_time']) * 1e6), int('K' in p['flags'])]
           for p in raw['packets']]
assert all(p[0] + p[1] <= video.stat().st_size for p in packets)
manifest = dict(codec='avc1.' + extra[1:4].hex(), width=stream['width'], height=stream['height'],
                description=list(extra), duration=max(p[2] + p[3] for p in packets), packets=packets)
(root / 'assets/ip-home-mobile-v3.frames.json').write_text(
    json.dumps(manifest, separators=(',', ':')), encoding='utf-8')
