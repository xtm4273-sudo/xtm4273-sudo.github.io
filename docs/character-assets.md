# 工作视频与底部联系人物

工作视频来自用户提供的《视频节点 9.mp4》《视频节点 11.mp4》，分别保存为 assets/testing-work.mp4 和 assets/fde-work.mp4。视频保留原始文件、分辨率与帧率；仅在网页中施加柔边遮罩，未进行逐帧人物抠像。封面帧使用 ffmpeg 提取。

底部联系人物保存为 assets/contact-character.png（1024×1536，RGBA），由内置 imagegen 根据用户提供的底部联系页参考图提取，保留透明通道；原生成文件另行保留。未使用 CLI/API fallback。

## 最终生成提示

Edit target: attached website screenshot. Background extraction for a website asset. Extract ONLY the full-body blonde 3D steampunk girl on the left, precisely preserving her identity, face, amber eyes, hair bun and loose braid, brown mechanic outfit, brass goggles around neck, boots, pose with left hand at hip and right hand pointing down-right. Remove ALL website UI, text, background, divider lines, glows, floor and shadows. Clean genuine transparent alpha background, not a checkerboard. Full body including every fingertip and boot, no cropping. Keep original proportions and realistic 3D material detail, do not redesign character. Output a portrait transparent PNG with a small transparent margin around the character suitable for placing on a dark website. Save the output image file and provide its path.
