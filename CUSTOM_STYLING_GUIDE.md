# 🎨 Custom Styling Guide

## Overview

We've added comprehensive custom CSS to enhance Bootstrap's default styling, making the Study Organizer more modern, polished, and visually appealing.

## 📁 File Location

**`static/css/custom.css`** - Main custom stylesheet (1000+ lines)

Linked in `templates/base.html`:

```html
<link
  rel="stylesheet"
  href="{{ url_for('static', filename='css/custom.css') }}"
/>
```

## ✨ What's Enhanced

### 1. **Modern Design System** 🎯

#### CSS Variables (Theme Support)

- **Primary Colors**: Gradient-based color scheme
- **Neutral Colors**: Comprehensive gray scale
- **Spacing System**: Consistent spacing (xs, sm, md, lg, xl)
- **Border Radius**: Unified radius system
- **Shadows**: 4-level shadow system (sm, md, lg, xl)
- **Transitions**: Timing functions (fast, base, slow)

#### Dark Theme Support

All variables automatically adapt to dark theme:

```css
:root {
  /* Light theme */
}
[data-theme="dark"] {
  /* Dark theme overrides */
}
```

### 2. **Enhanced Components** 🧩

#### Cards

- **Hover Effects**: Lift animation, increased shadow
- **Border Radius**: Rounded corners (12px)
- **Transitions**: Smooth 200ms animations
- **Gradient Headers**: Subtle gradient backgrounds
- **No Borders**: Clean, modern look with shadows

**Features:**

```css
.card {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
```

#### Buttons

- **Gradient Backgrounds**: Primary, Success, Info, Warning, Danger
- **Ripple Effect**: Material Design-inspired click animation
- **Hover States**: Lift effect, enhanced shadow
- **Smooth Transitions**: 150ms cubic-bezier
- **Outline Variants**: Hover fill with gradients

**Special Effects:**

- Ripple animation on click
- 1px lift on hover
- Shadow depth changes

#### Forms

- **Rounded Inputs**: 8px border radius
- **Focus States**: Blue border + soft glow
- **2px Borders**: More prominent boundaries
- **Better Padding**: Comfortable input spacing
- **Label Styling**: Semi-bold, proper spacing

#### Badges

- **Rounded**: 8px border radius
- **Better Padding**: 0.375rem × 0.75rem
- **Letter Spacing**: 0.025em for readability
- **Font Weight**: 500 (medium)

### 3. **Collaboration-Specific Styles** 🤝

#### Share Interface

```css
.share-interface {
  background: linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
}
```

#### Permission Badges

- **Viewer**: Blue gradient
- **Editor**: Orange gradient
- **Admin**: Red gradient
- **Hover Effect**: Scale 1.05

```css
.permission-viewer {
  background: linear-gradient(135deg, #4299e1, #3182ce);
}
```

#### User Avatars

- **Circle Shape**: Perfect 40px circles
- **Border**: 2px white border
- **Hover**: Scale 1.1, enhanced shadow
- **Transitions**: Smooth 150ms

#### Study Group Cards

- **Top Border Animation**: Gradient line appears on hover
- **Lift Effect**: 4px translateY on hover
- **Icon Styling**: 56px rounded squares with gradients
- **Glass Effect Overlay**: Subtle white gradient on hover

#### Comment Cards

- **Left Border**: 4px colored accent
- **Hover Animation**: Slides right 4px
- **Author Styling**: Bold text, metadata in gray
- **Spacing**: Comfortable padding

#### Notifications

- **Badge Animation**: Pulse effect (2s infinite)
- **Bell Container**: Circular 40px background
- **Item Hover**: Slide right, border color change
- **Unread State**: Gradient background, left border

### 4. **Enhanced Tables** 📊

- **Rounded Corners**: Overflow hidden
- **Gradient Header**: Gray gradient background
- **Uppercase Headers**: Small caps, letter spacing
- **Row Hover**: Background change, subtle scale
- **Better Borders**: 2px bottom border on headers

### 5. **List Groups** 📋

- **Rounded Items**: 8px radius per item
- **Spacing**: 4px margin between items
- **Hover Animation**: Slide right 4px
- **Border Transition**: Color changes on hover
- **Dark Mode**: Subtle background in dark theme

### 6. **Alerts** 🚨

- **Rounded**: 12px border radius
- **No Borders**: Shadow-based depth
- **Gradient Backgrounds**: Subtle color gradients
- **Type Colors**:
  - Info: Blue gradient
  - Success: Green gradient
  - Warning: Orange gradient
  - Danger: Red gradient

### 7. **Modals** 🪟

- **Extra Rounded**: 16px border radius
- **Large Shadow**: XL shadow depth
- **Gradient Header**: Top gradient effect
- **Footer Background**: Light gray background
- **No Borders**: Clean separation

### 8. **Dropdowns** ⬇️

- **Rounded Menu**: 12px border radius
- **Large Shadow**: Enhanced depth
- **Padding**: 8px around menu
- **Item Hover**: Gradient background, slide right
- **Item Spacing**: 2px gap between items

### 9. **Utility Classes** 🛠️

#### Text Gradient

```css
.text-gradient {
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

#### Glass Effect

```css
.glass-effect {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
}
```

#### Hover Lift

```css
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
```

### 10. **Loading States** ⏳

```css
.loading-spinner {
  border: 3px solid rgba(102, 126, 234, 0.3);
  border-top-color: #667eea;
  animation: spin 0.8s linear infinite;
}
```

### 11. **Empty States** 📭

```css
.empty-state {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--gray-500);
}

.empty-state-icon {
  font-size: 4rem;
  color: var(--gray-300);
}
```

## 🎨 Color Palette

### Primary Gradient

```css
linear-gradient(135deg, #667eea 0%, #764ba2 100%)
```

### Success Gradient

```css
linear-gradient(135deg, #48bb78 0%, #38a169 100%)
```

### Info Gradient

```css
linear-gradient(135deg, #4299e1 0%, #3182ce 100%)
```

### Warning Gradient

```css
linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)
```

### Danger Gradient

```css
linear-gradient(135deg, #fc8181 0%, #f56565 100%)
```

## 📱 Responsive Design

### Mobile Breakpoints

#### Tablet (≤ 768px)

- Reduced padding on section cards
- Smaller group/collection icons (48px)
- Smaller avatars (32px)

#### Mobile (≤ 576px)

- Further reduced padding
- Smaller button text (0.875rem)
- Compact button padding

### Example:

```css
@media (max-width: 768px) {
  .section-card {
    padding: var(--spacing-lg);
  }

  .group-icon {
    width: 48px;
    height: 48px;
  }
}
```

## ♿ Accessibility Features

### Focus Visible

```css
.focus-visible:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### ARIA Support

All interactive elements maintain proper focus states and keyboard navigation.

## 🖨️ Print Styles

```css
@media print {
  .btn,
  .navbar,
  footer,
  .notification-bell {
    display: none !important;
  }

  .card,
  .section-card {
    box-shadow: none !important;
    border: 1px solid #ddd !important;
  }
}
```

## 🎯 Key Improvements Over Default Bootstrap

### 1. **Visual Hierarchy**

- ✅ Stronger shadows for depth
- ✅ Gradient backgrounds for emphasis
- ✅ Consistent spacing system
- ✅ Better border radius values

### 2. **Interactivity**

- ✅ Hover effects on all interactive elements
- ✅ Smooth transitions (150-300ms)
- ✅ Ripple effect on buttons
- ✅ Lift animations

### 3. **Modern Aesthetics**

- ✅ Gradient-based color scheme
- ✅ Rounded corners everywhere
- ✅ Glass morphism effects
- ✅ Subtle animations

### 4. **Dark Theme**

- ✅ Full dark mode support
- ✅ Automatic variable switching
- ✅ Maintains contrast ratios
- ✅ Preserves accessibility

### 5. **Consistency**

- ✅ Unified design tokens (CSS variables)
- ✅ Predictable spacing
- ✅ Consistent timing functions
- ✅ Standardized shadows

## 📊 Statistics

- **Total Lines**: 1000+ lines of CSS
- **CSS Variables**: 30+ custom properties
- **Components Styled**: 20+ Bootstrap components
- **Responsive Breakpoints**: 3 levels
- **Animation Keyframes**: 2 (spin, pulse)
- **Color Gradients**: 5 primary gradients
- **Shadow Levels**: 4 depth levels

## 🚀 Performance

### Optimizations

- ✅ CSS variables for theme switching (no JavaScript)
- ✅ Hardware-accelerated transforms
- ✅ Efficient selectors
- ✅ Minimal specificity conflicts
- ✅ No !important overuse

### Loading

- ✅ Single CSS file
- ✅ Minification-ready
- ✅ No external dependencies
- ✅ ~40KB unminified

## 🎓 Using Custom Styles

### In Templates

#### Apply Section Card

```html
<div class="section-card">
  <h4 class="section-title">Your Title</h4>
  <!-- Content -->
</div>
```

#### Use Gradient Text

```html
<h1 class="text-gradient">Study Organizer</h1>
```

#### Glass Effect

```html
<div class="glass-effect p-4">
  <!-- Content with glass morphism -->
</div>
```

#### Hover Lift

```html
<div class="card hover-lift">
  <!-- Card content -->
</div>
```

### Custom Classes

#### Permission Badges

```html
<span class="permission-badge permission-viewer">
  <i class="bi bi-eye"></i> Viewer
</span>
```

#### User Avatar

```html
<img src="..." class="user-avatar" alt="User" />
```

#### Group/Collection Icon

```html
<div class="group-icon" data-color="#667eea">
  <i class="bi bi-people-fill"></i>
</div>
```

#### Comment Card

```html
<div class="comment-card">
  <div class="comment-author">John Doe</div>
  <div class="comment-content">Great notes!</div>
  <div class="comment-meta">2 hours ago</div>
</div>
```

## 💡 Best Practices

### DO ✅

- Use CSS variables for consistency
- Apply hover effects for interactivity
- Maintain spacing system
- Follow border radius standards
- Use gradient backgrounds for emphasis

### DON'T ❌

- Override with inline styles
- Use arbitrary spacing values
- Mix shadow depths inconsistently
- Ignore dark theme variables
- Skip transition properties

## 🔮 Future Enhancements

### Potential Additions

1. **More Animations**: Fade-in, slide-up effects
2. **Custom Scrollbars**: Styled scrollbar design
3. **Skeleton Loaders**: Loading state improvements
4. **Micro-interactions**: Subtle feedback animations
5. **Color Themes**: Multiple theme options
6. **Component Variants**: More style variations

## 📚 Documentation

### Quick Reference

#### Spacing

- `--spacing-xs`: 0.25rem (4px)
- `--spacing-sm`: 0.5rem (8px)
- `--spacing-md`: 1rem (16px)
- `--spacing-lg`: 1.5rem (24px)
- `--spacing-xl`: 2rem (32px)

#### Border Radius

- `--radius-sm`: 0.375rem (6px)
- `--radius-md`: 0.5rem (8px)
- `--radius-lg`: 0.75rem (12px)
- `--radius-xl`: 1rem (16px)

#### Shadows

- `--shadow-sm`: Subtle shadow
- `--shadow-md`: Medium shadow
- `--shadow-lg`: Large shadow
- `--shadow-xl`: Extra large shadow

#### Transitions

- `--transition-fast`: 150ms
- `--transition-base`: 200ms
- `--transition-slow`: 300ms

## 🎉 Conclusion

The custom CSS enhances Bootstrap with:

- ✅ Modern, polished design
- ✅ Consistent design system
- ✅ Smooth animations
- ✅ Dark theme support
- ✅ Better accessibility
- ✅ Mobile responsive
- ✅ Performance optimized

**Result**: A professional, modern UI that enhances user experience and makes your final year project stand out visually!

---

**Created**: October 2025  
**File**: `static/css/custom.css`  
**Size**: ~40KB (unminified)  
**Compatibility**: Bootstrap 5.3+, Modern browsers
