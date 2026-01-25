# Design Patterns & Component Best Practices

Comprehensive guide to UI patterns, component design, and design system best practices for Figma.

## Component Architecture

### Atomic Design Principles

#### Atoms (Basic Elements)
- **Buttons**: Primary, secondary, ghost, icon buttons
- **Form inputs**: Text fields, selectors, checkboxes, radio buttons
- **Typography**: Headings, body text, captions, labels
- **Icons**: Consistent icon library with standardized sizing
- **Avatars**: User profile images with fallback states

**Best Practices:**
- Use auto-layout for flexible resizing
- Create consistent hover/focus/disabled states
- Establish clear naming conventions
- Include component documentation

#### Molecules (Simple Combinations)
- **Form groups**: Label + input + validation message
- **Navigation items**: Icon + text + badge
- **Card headers**: Title + subtitle + actions
- **Search bars**: Input + search icon + clear button

**Best Practices:**
- Combine atoms logically and purposefully
- Maintain single responsibility principle
- Use component properties for variations
- Test across different content lengths

#### Organisms (Complex Combinations)
- **Navigation bars**: Logo + menu + user profile + search
- **Data tables**: Headers + rows + pagination + actions
- **Product cards**: Image + title + price + actions
- **Forms**: Multiple form groups + buttons + validation

**Best Practices:**
- Design for responsive behavior
- Consider loading and error states
- Plan for empty states and edge cases
- Optimize for accessibility

### Component Naming Conventions

#### Hierarchical Structure
```
Component Name / Variant / State
Examples:
- Button / Primary / Default
- Button / Primary / Hover
- Button / Secondary / Disabled
- Input / Text / Error
- Card / Product / Loading
```

#### Descriptive Naming
- Use descriptive, action-oriented names
- Avoid technical jargon in user-facing names
- Be consistent across similar components
- Include size/type indicators when helpful

## Layout Patterns

### Grid Systems

#### Standard Grid Configurations
- **12-column grid**: Most versatile, works for web and mobile
- **8-column grid**: Good for tablet layouts
- **4-column grid**: Mobile-friendly, simple layouts
- **Custom grids**: Match specific brand requirements

**Grid Properties:**
- Consistent gutters (16px, 20px, 24px common)
- Responsive breakpoints (320px, 768px, 1024px, 1440px)
- Maximum content width (1200px-1440px typical)

#### Auto-Layout Best Practices
- Use auto-layout for all flexible components
- Set appropriate resizing constraints
- Consider padding vs margin usage
- Test with varying content lengths

### Common Layout Patterns

#### Header Patterns
1. **Simple header**: Logo + navigation + CTA
2. **Mega menu**: Logo + dropdown navigation + search + account
3. **Mobile header**: Hamburger + logo + account/cart
4. **Dashboard header**: Breadcrumbs + title + actions

#### Content Layouts
1. **Single column**: Simple, focused content flow
2. **Two column**: Main content + sidebar
3. **Three column**: Sidebar + main + secondary sidebar
4. **Card grid**: Responsive card layouts
5. **Masonry**: Pinterest-style irregular grid

#### Footer Patterns
1. **Simple footer**: Copyright + key links
2. **Rich footer**: Multiple link columns + social + newsletter
3. **Sticky footer**: Always at bottom of viewport
4. **Fat footer**: Extensive links + contact info + sitemap

## Interface Patterns

### Navigation Patterns

#### Primary Navigation
- **Horizontal nav**: Works well for 3-7 main sections
- **Vertical sidebar**: Good for 8+ items or complex hierarchies
- **Tab navigation**: For equal-importance sections
- **Breadcrumbs**: Show hierarchy and allow backtracking

#### Secondary Navigation
- **Dropdown menus**: Organize related sub-items
- **Contextual sidebars**: Show relevant options for current content
- **Floating action buttons**: Promote primary actions
- **Bottom navigation**: Mobile-friendly for core functions

### Form Patterns

#### Form Layout
- **Single column**: Easier to scan and complete
- **Label placement**: Above fields for better readability
- **Required indicators**: Use asterisks or "(required)" text
- **Help text**: Provide when needed, but don't overdo

#### Input Patterns
- **Progressive disclosure**: Show additional fields as needed
- **Smart defaults**: Pre-fill when possible
- **Inline validation**: Real-time feedback on field completion
- **Clear error states**: Specific, actionable error messages

#### Form Actions
- **Primary/secondary buttons**: Clear visual hierarchy
- **Save states**: Show progress and confirmation
- **Cancel behavior**: Ask about unsaved changes
- **Multi-step forms**: Show progress and allow navigation

### Data Display Patterns

#### Tables
- **Sortable headers**: Allow data organization
- **Pagination**: Handle large datasets
- **Row actions**: Edit, delete, view details
- **Selection**: Bulk operations capability
- **Responsive behavior**: Stack or hide columns on mobile

#### Cards
- **Consistent structure**: Image + title + metadata + actions
- **Hover states**: Show additional information or actions
- **Loading states**: Skeleton screens or progress indicators
- **Empty states**: Helpful guidance when no content exists

#### Lists
- **Simple lists**: Basic text with optional icons
- **Rich lists**: Multiple lines of information
- **Interactive lists**: Drag-and-drop, selection
- **Infinite scroll**: Load more content seamlessly

## Responsive Design Patterns

### Breakpoint Strategy

#### Common Breakpoints
- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1023px  
- **Desktop**: 1024px - 1439px
- **Large desktop**: 1440px+

#### Content Strategy
- **Mobile first**: Design for constraints, enhance for larger screens
- **Progressive enhancement**: Add features as screen size allows
- **Content parity**: Ensure feature availability across devices
- **Touch targets**: Minimum 44px for mobile interactions

### Adaptive Techniques

#### Navigation Adaptation
- **Collapsible menu**: Hamburger pattern for mobile
- **Priority navigation**: Show most important items first
- **Overflow menus**: "More" option for secondary items
- **Tab bar**: Bottom navigation for mobile apps

#### Content Adaptation
- **Stacking**: Single column on mobile, multiple on desktop
- **Content reduction**: Progressive disclosure on smaller screens
- **Image scaling**: Responsive images with appropriate crops
- **Typography scaling**: Larger text on mobile for readability

## Accessibility Patterns

### Color and Contrast
- **4.5:1 contrast ratio**: Minimum for normal text (WCAG AA)
- **3:1 contrast ratio**: Minimum for large text and UI components
- **Don't rely on color alone**: Use icons, text, or patterns too
- **Color blind considerations**: Test with color vision simulators

### Interaction Patterns
- **Focus indicators**: Clear visual focus for keyboard navigation
- **Touch targets**: Minimum 44x44px for touch interfaces
- **Click/tap areas**: Generous padding around interactive elements
- **Hover states**: Clear feedback for interactive elements

### Content Patterns
- **Alt text**: Descriptive text for images and icons
- **Heading hierarchy**: Proper H1-H6 structure
- **Link text**: Descriptive, avoid "click here"
- **Form labels**: Clear, descriptive labels for all inputs

## Animation and Microinteractions

### Animation Principles
- **Purposeful motion**: Animation should serve a function
- **Consistent timing**: Use consistent easing and duration
- **Respect preferences**: Honor reduced motion preferences
- **Performance**: Smooth 60fps animations

### Common Microinteractions
- **Button feedback**: Subtle scale or color change on press
- **Loading indicators**: Skeleton screens or spinners
- **Success confirmations**: Checkmarks or brief messaging
- **Error handling**: Gentle shake or color change for errors
- **Page transitions**: Smooth movement between states

### Transition Patterns
- **Slide transitions**: Natural for sequential content
- **Fade transitions**: Good for overlays and modals
- **Scale transitions**: Effective for showing/hiding elements
- **Morphing transitions**: Transform one element into another

## Design System Organization

### File Structure
```
Design System/
├── Foundation/
│   ├── Colors
│   ├── Typography
│   ├── Spacing
│   ├── Grid
│   └── Iconography
├── Components/
│   ├── Atoms/
│   ├── Molecules/
│   └── Organisms/
├── Patterns/
│   ├── Navigation
│   ├── Forms
│   ├── Data Display
│   └── Feedback
└── Templates/
    ├── Landing Pages
    ├── Dashboard
    └── Content Pages
```

### Documentation Standards
- **Component purpose**: What problem does it solve?
- **Usage guidelines**: When and how to use
- **Do's and don'ts**: Clear examples of proper usage
- **Accessibility notes**: ARIA patterns, keyboard behavior
- **Implementation notes**: Technical considerations

### Maintenance Practices
- **Regular audits**: Review and update components quarterly
- **Usage tracking**: Monitor which components are actually used
- **Feedback loops**: Collect input from designers and developers
- **Version control**: Clear versioning and change logs
- **Testing**: Validate components across different contexts

## Mobile-Specific Patterns

### Touch Interactions
- **Tap**: Primary interaction method
- **Long press**: Secondary actions, context menus
- **Swipe**: Navigation, dismissal actions
- **Pinch**: Zoom functionality
- **Pull to refresh**: Common mobile pattern

### Mobile Navigation
- **Tab bar**: 3-5 primary sections
- **Hamburger menu**: Secondary navigation
- **Segmented control**: Filter or view switching
- **Bottom sheet**: Contextual actions and options

### Mobile Content
- **Card-based layouts**: Easy to scan and interact with
- **Thumb-friendly zones**: Important actions in easy reach
- **Generous whitespace**: Improve readability and touch accuracy
- **Clear hierarchy**: Bold typography and visual separation