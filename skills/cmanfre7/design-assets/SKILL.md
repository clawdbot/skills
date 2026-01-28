# design-assets

Create and edit graphic design assets: icons, favicons, images, and color systems.

## Tool Selection

| Task | Tool | Why |
|------|------|-----|
| AI image generation | nano-banana-pro | Generate images from text prompts |
| Image resize/convert | sips | macOS native, fast, no deps |
| Advanced manipulation | ImageMagick | Compositing, effects, batch processing |
| Icons & logos | SVG | Scalable, small file size, editable |
| Screenshots | screencapture | macOS native |

## App Icon Generation

Generate all required sizes from a single 1024x1024 source icon.

### iOS / macOS Icon Sizes
```bash
#!/bin/bash
# generate-app-icons.sh <source-1024.png> <output-dir>
SOURCE="$1"
OUTDIR="${2:-.}"
mkdir -p "$OUTDIR"

SIZES=(16 20 29 32 40 48 58 60 64 76 80 87 120 128 152 167 180 256 512 1024)
for SIZE in "${SIZES[@]}"; do
  sips -z $SIZE $SIZE "$SOURCE" --out "$OUTDIR/icon-${SIZE}x${SIZE}.png" 2>/dev/null
done
echo "Generated ${#SIZES[@]} icon sizes in $OUTDIR"
```

### Android Icon Sizes
```bash
# Android adaptive icon sizes
declare -A ANDROID_SIZES=(
  ["mdpi"]=48 ["hdpi"]=72 ["xhdpi"]=96
  ["xxhdpi"]=144 ["xxxhdpi"]=192
)
for DENSITY in "${!ANDROID_SIZES[@]}"; do
  SIZE=${ANDROID_SIZES[$DENSITY]}
  mkdir -p "res/mipmap-$DENSITY"
  sips -z $SIZE $SIZE "$SOURCE" --out "res/mipmap-$DENSITY/ic_launcher.png"
done
```

## Favicon Generation

```bash
#!/bin/bash
# generate-favicons.sh <source.png> <output-dir>
SOURCE="$1"
OUTDIR="${2:-.}"
mkdir -p "$OUTDIR"

# Standard web favicons
sips -z 16 16 "$SOURCE" --out "$OUTDIR/favicon-16x16.png"
sips -z 32 32 "$SOURCE" --out "$OUTDIR/favicon-32x32.png"
sips -z 180 180 "$SOURCE" --out "$OUTDIR/apple-touch-icon.png"
sips -z 192 192 "$SOURCE" --out "$OUTDIR/android-chrome-192x192.png"
sips -z 512 512 "$SOURCE" --out "$OUTDIR/android-chrome-512x512.png"

# ICO file (requires ImageMagick)
magick "$OUTDIR/favicon-16x16.png" "$OUTDIR/favicon-32x32.png" "$OUTDIR/favicon.ico"

echo "Favicons generated in $OUTDIR"
```

### HTML Meta Tags
```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

### site.webmanifest
```json
{
  "name": "My App",
  "short_name": "App",
  "icons": [
    { "src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

## Color Palette Generator

Given a primary color, generate a full palette:

```javascript
// HSL-based palette generation
function generatePalette(hue, saturation = 70) {
  return {
    50:  `hsl(${hue}, ${saturation}%, 97%)`,
    100: `hsl(${hue}, ${saturation}%, 94%)`,
    200: `hsl(${hue}, ${saturation}%, 86%)`,
    300: `hsl(${hue}, ${saturation}%, 74%)`,
    400: `hsl(${hue}, ${saturation}%, 62%)`,
    500: `hsl(${hue}, ${saturation}%, 50%)`,  // Primary
    600: `hsl(${hue}, ${saturation}%, 42%)`,
    700: `hsl(${hue}, ${saturation}%, 34%)`,
    800: `hsl(${hue}, ${saturation}%, 26%)`,
    900: `hsl(${hue}, ${saturation}%, 18%)`,
    950: `hsl(${hue}, ${saturation}%, 10%)`,
  };
}
```

## ImageMagick Quick Reference

```bash
# Resize
magick input.png -resize 800x600 output.png

# Convert format
magick input.png output.webp

# Add border
magick input.png -border 10 -bordercolor "#333" output.png

# Round corners (with transparency)
magick input.png \( +clone -alpha extract -draw "roundrectangle 0,0,%[w],%[h],20,20" \) -alpha off -compose CopyOpacity -composite output.png

# Composite / overlay
magick base.png overlay.png -gravity center -composite output.png

# Batch resize all PNGs
magick mogrify -resize 50% *.png

# Create solid color image
magick -size 1200x630 xc:"#1a1a2e" output.png

# Add text to image
magick input.png -gravity south -pointsize 24 -fill white -annotate +0+20 "Caption" output.png
```

## sips Quick Reference (macOS)

```bash
# Resize (maintain aspect ratio)
sips --resampleWidth 800 input.png --out output.png

# Exact resize
sips -z 600 800 input.png --out output.png

# Convert format
sips -s format jpeg input.png --out output.jpg

# Get image info
sips -g all input.png

# Rotate
sips --rotate 90 input.png --out output.png
```
