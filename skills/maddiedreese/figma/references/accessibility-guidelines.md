# Accessibility Guidelines for Figma Design

Comprehensive WCAG compliance guide and accessibility best practices for inclusive design.

## WCAG 2.1 Compliance Levels

### Level A (Minimum)
Basic web accessibility features that should be present in all designs.

### Level AA (Standard)
Recommended level for most websites and applications. Removes major barriers to accessing content.

### Level AAA (Enhanced)
Highest level, required for specialized contexts but not recommended as general policy.

**Focus on AA compliance** - this covers the vast majority of accessibility needs without excessive constraints.

## Color and Visual Accessibility

### Color Contrast Requirements

#### WCAG AA Standards
- **Normal text**: 4.5:1 contrast ratio minimum
- **Large text** (18pt+ or 14pt+ bold): 3:1 contrast ratio minimum
- **UI components**: 3:1 contrast ratio for borders, icons, form controls
- **Graphics**: 3:1 contrast ratio for meaningful graphics

#### WCAG AAA Standards (Enhanced)
- **Normal text**: 7:1 contrast ratio
- **Large text**: 4.5:1 contrast ratio

#### Testing Tools in Figma
- **Stark plugin**: Real-time contrast checking
- **Color Oracle**: Color blindness simulation
- **WebAIM contrast checker**: External validation

### Color Usage Guidelines

#### Don't Rely on Color Alone
```
❌ Bad: "Click the green button to continue"
✅ Good: "Click the 'Continue' button (green) to proceed"
```

- Use icons, text labels, or patterns alongside color
- Ensure information is conveyed through multiple visual cues
- Test designs in grayscale to verify information accessibility

#### Color Blindness Considerations
- **Red-green color blindness** affects ~8% of men, ~0.5% of women
- **Blue-yellow color blindness** is less common but still significant
- Use tools like Colorblinding or Stark to test your designs
- Consider using shapes, patterns, or positions as additional indicators

### Typography Accessibility

#### Font Size Guidelines
- **Minimum body text**: 16px (12pt) for web
- **Minimum mobile text**: 16px (prevents zoom on iOS)
- **Large text threshold**: 18pt (24px) regular, 14pt (18.7px) bold
- **Line height**: 1.5x font size minimum for body text
- **Paragraph spacing**: At least 1.5x line height

#### Font Choice
- **Sans-serif fonts** generally more readable on screens
- **Avoid decorative fonts** for body text
- **System fonts** ensure consistency and performance
- **Web-safe fonts** for broader compatibility

#### Text Layout
- **Line length**: 45-75 characters for optimal readability
- **Left alignment** for left-to-right languages
- **Adequate spacing** between letters, words, lines, paragraphs
- **Avoid justified text** which can create awkward spacing

## Interactive Element Accessibility

### Touch and Click Targets

#### Size Requirements
- **Minimum size**: 44x44px (iOS/Material Design standard)
- **Recommended size**: 48x48px for better usability
- **Spacing**: At least 8px between adjacent targets
- **Mobile considerations**: Thumb-friendly zones, easy reach

#### Visual Feedback
- **Hover states**: Clear indication of interactive elements
- **Active states**: Immediate feedback on interaction
- **Disabled states**: Clearly distinguish non-functional elements
- **Loading states**: Show progress for time-consuming actions

### Focus Management

#### Focus Indicators
- **Visible focus**: Clear outline or background change
- **High contrast**: Focus indicator must have 3:1 contrast ratio
- **Consistent style**: Same focus treatment across the interface
- **Never remove focus indicators** without providing alternative

#### Focus Order
- **Logical sequence**: Follow visual layout and reading order
- **Tab navigation**: All interactive elements reachable via keyboard
- **Skip links**: Allow bypassing repetitive navigation
- **Focus traps**: Keep focus within modals/dialogs when open

### Form Accessibility

#### Label Requirements
- **All inputs must have labels**: Use explicit labels, not just placeholders
- **Required field indicators**: Clear marking of mandatory fields
- **Group related fields**: Use fieldsets and legends for grouped inputs
- **Help text**: Provide guidance when needed

#### Error Handling
```
❌ Bad: Red border with no explanation
✅ Good: "Email address is required" with clear visual indicator
```

- **Specific error messages**: Explain what's wrong and how to fix it
- **Error summaries**: List all errors at top of form for screen readers
- **Inline validation**: Real-time feedback where helpful
- **Success confirmation**: Confirm successful form submissions

#### Form Layout
- **Single column layouts**: Easier to navigate and complete
- **Logical grouping**: Related fields grouped together
- **Progress indicators**: Show steps in multi-step forms
- **Clear submission**: Make it obvious how to submit the form

## Content Structure and Navigation

### Heading Hierarchy

#### Proper Heading Structure
```html
H1 - Page title (one per page)
├── H2 - Main sections
│   ├── H3 - Subsections
│   │   └── H4 - Sub-subsections
│   └── H3 - Another subsection
└── H2 - Another main section
```

- **Don't skip levels**: H1 → H2 → H3, never H1 → H3
- **Use headings for structure**: Not just for visual styling
- **One H1 per page**: Primary page title only

### Link Accessibility

#### Link Text Guidelines
```
❌ Bad: "Click here for more information"
✅ Good: "Read our complete accessibility guide"
```

- **Descriptive link text**: Explains where the link leads
- **Context independence**: Should make sense when read alone
- **Unique link text**: Different destinations need different text
- **External link indicators**: Show when links lead off-site

### Navigation Patterns

#### Skip Links
- **Skip to main content**: Bypass repetitive navigation
- **Skip to search**: Quick access to search functionality
- **Keyboard users**: Essential for efficient navigation
- **Hidden until focused**: Don't clutter visual design

#### Breadcrumbs
- **Show location**: Help users understand where they are
- **Provide navigation**: Easy way to move up the hierarchy
- **Current page**: Don't make current page a link
- **Separator clarity**: Use > or / with proper ARIA labels

## Images and Media

### Image Accessibility

#### Alt Text Guidelines
- **Decorative images**: Use empty alt attribute (alt="")
- **Informative images**: Describe the information conveyed
- **Functional images**: Describe the action/function
- **Complex images**: Provide detailed description nearby

#### Alt Text Examples
```
❌ Bad: alt="image"
❌ Bad: alt="photo.jpg"  
✅ Good: alt="Bar chart showing 40% increase in sales"
✅ Good: alt="Submit form" (for submit button image)
✅ Good: alt="" (for purely decorative images)
```

### Video and Audio

#### Video Accessibility
- **Captions**: For all spoken content
- **Audio descriptions**: For visual content not described in audio
- **Transcript**: Full text version of audio content
- **Player controls**: Accessible play/pause/volume controls

#### Audio Accessibility
- **Transcripts**: For all audio content
- **Auto-play restrictions**: Avoid auto-playing audio
- **Volume controls**: User control over audio levels
- **Visual indicators**: Show when audio is playing

## Mobile Accessibility

### Touch Interface Guidelines

#### Gesture Support
- **Single-tap primary**: Main interaction method
- **Alternative access**: Provide alternatives to complex gestures
- **Gesture hints**: Teach users about available gestures
- **Gesture conflicts**: Avoid conflicts with system gestures

#### Mobile-Specific Considerations
- **Orientation support**: Work in both portrait and landscape
- **Zoom support**: Allow pinch-to-zoom for text content
- **Motion sensitivity**: Respect reduced motion preferences
- **One-handed use**: Design for thumb navigation

### Screen Reader Support

#### iOS VoiceOver
- **Element labeling**: Provide clear, descriptive labels
- **Navigation order**: Logical focus sequence
- **Custom actions**: Define available actions for elements
- **Notifications**: Use announcements for dynamic changes

#### Android TalkBack
- **Content descriptions**: Equivalent to alt text for UI elements
- **Clickable indicators**: Mark interactive elements properly
- **Live regions**: Announce dynamic content changes
- **Semantic markup**: Use proper HTML/accessibility semantics

## Testing and Validation

### Automated Testing Tools

#### Figma Plugins
- **Stark**: Comprehensive accessibility checker
- **Color Blind Web Page Filter**: Color blindness simulation
- **Able**: Color contrast and font size checker
- **A11y - Color Contrast Checker**: Quick contrast validation

#### External Tools
- **WebAIM WAVE**: Web accessibility evaluation
- **axe DevTools**: Automated accessibility testing
- **Lighthouse**: Google's accessibility auditing
- **Pa11y**: Command-line accessibility testing

### Manual Testing Methods

#### Keyboard Testing
1. **Tab navigation**: Can you reach all interactive elements?
2. **Enter/Space activation**: Do buttons and links work?
3. **Arrow key navigation**: Works in menus and lists?
4. **Escape key**: Closes modals and menus?

#### Screen Reader Testing
1. **VoiceOver** (Mac): System Preferences → Accessibility → VoiceOver
2. **NVDA** (Windows): Free screen reader for testing
3. **JAWS** (Windows): Professional screen reader
4. **TalkBack** (Android): Built-in Android screen reader

#### Visual Testing
1. **Zoom to 200%**: Content should remain usable
2. **Grayscale mode**: Information still accessible?
3. **High contrast mode**: Text and UI still visible?
4. **Color blindness simulation**: Information still clear?

### User Testing

#### Include Users with Disabilities
- **Recruit diverse participants**: Different disabilities and assistive technologies
- **Test with real users**: Automated tools can't catch everything
- **Observe natural usage**: Don't guide too much during testing
- **Iterate based on feedback**: Accessibility is an ongoing process

#### Testing Scenarios
- **First-time usage**: Can new users complete key tasks?
- **Error recovery**: What happens when things go wrong?
- **Complex workflows**: Multi-step processes accessible?
- **Different contexts**: Various devices, environments, capabilities

## Implementation Guidelines

### Designer Handoff

#### Accessibility Annotations
- **Alt text specifications**: Document all image alt text
- **Focus order notes**: Specify tab sequence where non-obvious
- **Heading levels**: Mark proper heading hierarchy
- **Color contrast values**: Include specific contrast ratios
- **Interactive states**: Document all hover/focus/active states

#### Component Documentation
- **Accessibility features**: Built-in accessibility considerations
- **Usage guidelines**: When and how to use accessibly
- **ARIA patterns**: Required ARIA attributes and roles
- **Keyboard interactions**: Expected keyboard behavior

### Design System Integration

#### Accessible Components
- **Design once, use everywhere**: Build accessibility into components
- **Default accessibility**: Make accessible the easy choice
- **Clear documentation**: Accessibility requirements in design system
- **Regular audits**: Review and update component accessibility

#### Style Guidelines
- **Color palettes**: Pre-tested for contrast ratios
- **Typography scales**: Meet minimum size requirements
- **Spacing systems**: Ensure adequate touch targets
- **Icon libraries**: Include alt text recommendations

## Legal and Compliance

### Relevant Laws and Standards

#### United States
- **ADA** (Americans with Disabilities Act): Civil rights law
- **Section 508**: Federal agency accessibility requirements
- **WCAG 2.1**: Technical standard referenced by many laws

#### International
- **EN 301 549** (European Union): European accessibility standard
- **AODA** (Ontario): Accessibility for Ontarians with Disabilities Act
- **DDA** (Australia): Disability Discrimination Act

### Risk Mitigation
- **Legal compliance**: Following WCAG AA reduces legal risk
- **Documentation**: Keep records of accessibility efforts
- **Regular audits**: Ongoing compliance checking
- **User feedback**: Channels for reporting accessibility issues

## Resources and Tools

### Essential Resources
- **WCAG 2.1 Guidelines**: Official W3C accessibility standard
- **WebAIM**: Practical accessibility guidance and tools
- **A11y Project**: Community-driven accessibility resources
- **Inclusive Design Principles**: Microsoft's inclusive design guide

### Figma-Specific Resources
- **Figma Accessibility Guide**: Official Figma accessibility documentation
- **Accessible Design Systems**: Examples of accessible component libraries
- **Plugin Directory**: Accessibility-focused Figma plugins
- **Community Resources**: Accessibility templates and examples