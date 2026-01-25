# Export Formats and Specifications

Complete guide to Figma export options, formats, and optimization strategies for different use cases.

## Supported Export Formats

### Raster Formats

#### PNG (Portable Network Graphics)
**Best for:** UI elements, icons with transparency, screenshots

**Characteristics:**
- Lossless compression
- Supports transparency
- Larger file sizes than JPG
- Perfect for designs with sharp edges

**Use cases:**
- App icons and UI elements
- Logos with transparency
- Screenshots and mockups
- Print materials requiring transparency

**Export settings:**
- Scale: 1x, 2x, 3x, 4x
- Recommended: 2x for web, 3x for mobile apps
- Transparent backgrounds supported

#### JPG (Joint Photographic Experts Group)
**Best for:** Photographs, complex images, web optimization

**Characteristics:**
- Lossy compression
- Smaller file sizes
- No transparency support
- Good for photographic content

**Use cases:**
- Hero images and photography
- Marketing materials
- Email templates
- Web banners where file size matters

**Export settings:**
- Quality levels available in some tools
- Automatic white background fill
- Scale options: 1x, 2x, 4x

#### WEBP
**Best for:** Web optimization, modern browsers

**Characteristics:**
- Superior compression to PNG/JPG
- Supports transparency and animation
- Smaller file sizes
- Not supported in all browsers

**Use cases:**
- Web assets for modern browsers
- Progressive web apps
- Performance-critical applications

### Vector Formats

#### SVG (Scalable Vector Graphics)
**Best for:** Icons, simple illustrations, scalable graphics

**Characteristics:**
- Infinitely scalable
- Small file sizes for simple graphics
- Editable code
- Supports interactive elements

**Use cases:**
- Icon libraries
- Simple illustrations
- Logos for web use
- Scalable graphics

**Export options:**
- `svg_include_id`: Include node IDs for manipulation
- `svg_simplify_stroke`: Optimize stroke paths
- Text handling: Convert to paths vs keep as text

#### PDF (Portable Document Format)
**Best for:** Print materials, presentations, documentation

**Characteristics:**
- Vector-based when possible
- High quality for print
- Preserves text and formatting
- Universal compatibility

**Use cases:**
- Print marketing materials
- Presentations
- Documentation handoff
- High-quality mockups

**Export settings:**
- Vector elements preserved when possible
- Raster elements included at appropriate resolution
- Text can remain selectable

## Export Scales and Resolutions

### Device Pixel Ratios

#### 1x (Standard Resolution)
- **Use for:** Web designs, standard monitors
- **Pixel density:** 96 DPI
- **File size:** Smallest
- **Quality:** Standard

#### 2x (High-DPI)
- **Use for:** Retina displays, high-DPI web
- **Pixel density:** 192 DPI
- **File size:** 4x larger than 1x
- **Quality:** Sharp on high-DPI screens

#### 3x (Mobile High-DPI)
- **Use for:** iPhone Plus, Android high-end devices
- **Pixel density:** 288 DPI
- **File size:** 9x larger than 1x
- **Quality:** Extremely sharp mobile displays

#### 4x (Maximum Resolution)
- **Use for:** Future-proofing, print materials
- **Pixel density:** 384 DPI
- **File size:** 16x larger than 1x
- **Quality:** Maximum detail

### Platform-Specific Recommendations

#### iOS Apps
- **1x:** iPhone 3GS and older (rarely needed)
- **2x:** iPhone 4-8, iPad non-Retina
- **3x:** iPhone 6 Plus and newer large iPhones
- **Required:** All three scales for App Store submission

#### Android Apps
- **ldpi (0.75x):** Low-density screens (rarely used)
- **mdpi (1x):** Medium-density baseline
- **hdpi (1.5x):** High-density screens
- **xhdpi (2x):** Extra high-density
- **xxhdpi (3x):** Extra extra high-density
- **xxxhdpi (4x):** Highest density screens

#### Web Development
- **1x:** Base resolution for all browsers
- **2x:** For `@2x` media queries and Retina displays
- **Consider WEBP:** For modern browsers with fallback

## Asset Organization Strategies

### Folder Structure

#### By Platform
```
assets/
├── web/
│   ├── 1x/
│   ├── 2x/
│   └── icons/
├── ios/
│   ├── 1x/
│   ├── 2x/
│   └── 3x/
└── android/
    ├── ldpi/
    ├── mdpi/
    ├── hdpi/
    ├── xhdpi/
    ├── xxhdpi/
    └── xxxhdpi/
```

#### By Component Type
```
assets/
├── icons/
│   ├── navigation/
│   ├── actions/
│   └── status/
├── images/
│   ├── heroes/
│   ├── thumbnails/
│   └── placeholders/
└── logos/
    ├── full-color/
    ├── monochrome/
    └── reversed/
```

### Naming Conventions

#### Descriptive Naming
```
✅ Good:
- icon-search-24px.svg
- button-primary-large@2x.png
- hero-homepage-1200w.jpg

❌ Bad:
- icon1.svg
- button.png
- image.jpg
```

#### Platform Conventions

**iOS:**
```
icon-name.png      (1x)
icon-name@2x.png   (2x)  
icon-name@3x.png   (3x)
```

**Android:**
```
ic_name.png        (mdpi)
ic_name_hdpi.png   (hdpi)
ic_name_xhdpi.png  (xhdpi)
ic_name_xxhdpi.png (xxhdpi)
```

**Web:**
```
icon-name.svg      (vector)
icon-name.png      (1x fallback)
icon-name@2x.png   (2x for Retina)
```

## Optimization Techniques

### File Size Optimization

#### PNG Optimization
- **Reduce colors:** Use 8-bit when possible instead of 24-bit
- **Remove metadata:** Strip EXIF data and comments
- **Optimize palettes:** Use indexed color for simple graphics
- **Tools:** TinyPNG, ImageOptim, OptiPNG

#### JPG Optimization
- **Quality settings:** 80-90% for most use cases
- **Progressive JPEG:** Better perceived loading
- **Appropriate dimensions:** Don't export larger than needed
- **Tools:** JPEGmini, ImageOptim, MozJPEG

#### SVG Optimization
- **Simplify paths:** Remove unnecessary points
- **Group similar elements:** Reduce code duplication
- **Remove unused definitions:** Clean up gradients, styles
- **Tools:** SVGO, SVGOMG, Figma's built-in optimization

### Performance Considerations

#### Image Dimensions
- **Web images:** No larger than container size
- **2x images:** Exactly 2x the display size
- **Responsive images:** Multiple sizes for different breakpoints
- **Lazy loading:** Consider loading strategies

#### Format Selection Decision Tree
```
Is it a photograph or complex image?
├── Yes → JPG (or WEBP for modern browsers)
└── No → Does it need transparency?
    ├── Yes → PNG (or SVG if simple)
    └── No → JPG for web, PNG for UI elements
```

## Design Handoff Specifications

### Developer Handoff Assets

#### Complete Asset Package
1. **All required scales:** Platform-specific requirements
2. **Multiple formats:** SVG + PNG fallbacks for icons
3. **Organized structure:** Clear folder organization
4. **Naming documentation:** Explain naming conventions
5. **Usage guidelines:** When to use each asset

#### Asset Specifications Document
```
Asset Name: primary-button-large
Formats Available: PNG (1x, 2x, 3x), SVG
Dimensions: 
- 1x: 120x44px
- 2x: 240x88px  
- 3x: 360x132px
Usage: Primary call-to-action buttons
States: Default, Hover, Active, Disabled
```

### Design System Documentation

#### Component Assets
- **Multiple states:** Default, hover, active, disabled, loading
- **Size variations:** Small, medium, large
- **Theme variations:** Light mode, dark mode
- **Context usage:** When and where to use each variation

#### Icon Libraries
- **Consistent sizing:** 16px, 24px, 32px standard sizes
- **Stroke weights:** Consistent line thickness across set
- **Style coherence:** Same visual style for entire set
- **Semantic grouping:** Organize by function or category

## Batch Export Strategies

### Figma Export Tips

#### Selection-Based Export
1. Select multiple frames/components
2. Use export panel for batch settings
3. Apply same settings to all selected items
4. Export to organized folder structure

#### Component-Based Workflow
1. Create export-ready components
2. Use consistent naming for automatic organization
3. Set up export settings as part of component definition
4. Use plugins for advanced batch operations

### Automation Opportunities

#### Script-Based Export
- **Figma API:** Programmatic export control
- **Custom tools:** Build specific export workflows
- **Batch processing:** Handle hundreds of assets efficiently
- **Quality assurance:** Automated optimization and validation

#### CI/CD Integration
- **Automated exports:** Trigger on design updates
- **Asset deployment:** Push directly to CDN or asset pipeline
- **Version control:** Track asset changes alongside code
- **Optimization pipeline:** Automatic image optimization

## Special Use Cases

### App Store Assets

#### iOS App Store
- **App icons:** 1024x1024px for store, various sizes for app
- **Screenshots:** Device-specific dimensions
- **Requirements:** No transparency, specific format requirements
- **Validation:** App Store Connect validation rules

#### Google Play Store
- **Feature graphic:** 1024x500px
- **Screenshots:** Various device categories
- **App icons:** 512x512px high-res icon
- **Requirements:** Specific aspect ratios and content guidelines

### Print Materials

#### Print Specifications
- **Resolution:** 300 DPI minimum for professional printing
- **Color mode:** CMYK for print, RGB for digital
- **Bleed areas:** Extra space beyond trim line
- **Safe areas:** Keep important content away from edges

#### Export Settings
- **PDF format:** Preferred for print handoff
- **High resolution:** Use 4x scale or higher
- **Color profiles:** Include ICC profiles when possible
- **Vector preservation:** Maintain vector elements where possible

### Email Templates

#### Email Constraints
- **Image blocking:** Many clients block images by default
- **File size limits:** Keep images under 100KB when possible
- **Fallback text:** ALT text for accessibility
- **Dimensions:** Consider mobile email clients

#### Optimization Strategy
- **JPG for photos:** Smaller file sizes
- **PNG for UI elements:** Crisp edges and transparency
- **Inline critical images:** Small logos and icons
- **CDN hosting:** Fast loading from reliable servers

## Quality Assurance

### Export Validation

#### Visual Inspection
- **Compare to original:** Side-by-side comparison
- **Different scales:** Verify all export scales look correct
- **Multiple devices:** Test on target devices/browsers
- **Print proofs:** Physical proofs for print materials

#### Technical Validation
- **File sizes:** Reasonable for intended use
- **Dimensions:** Correct pixel dimensions
- **Format compatibility:** Works in target environments
- **Color accuracy:** Colors match design intent

### Testing Workflows

#### Cross-Platform Testing
- **Multiple browsers:** Chrome, Firefox, Safari, Edge
- **Different devices:** iOS, Android, various screen sizes
- **Operating systems:** macOS, Windows, Linux
- **Assistive technology:** Screen readers, high contrast modes

#### Performance Testing
- **Load times:** Measure actual loading performance
- **Bandwidth testing:** Test on slow connections
- **Caching behavior:** Verify proper caching headers
- **CDN performance:** Test global delivery speeds