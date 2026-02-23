# Physical AI & Humanoid Robotics Textbook 🤖

**An Interactive Learning Platform for Next-Gen Robotics**

A comprehensive, interactive textbook on Physical AI and Humanoid Robotics with modern UI/UX, animated neural network backgrounds, and scroll-triggered animations.

---

## 🎯 Features

### 📚 Textbook Content
- **Module 1**: ROS 2 for Humanoid Robotics
- **Module 2**: Digital Twin Technology
- **Module 3**: NVIDIA Isaac Sim
- **Module 4**: Vision-Language Actions (VLA)
- **Hardware Setup Guide**
- **Constitution & Ethics**

### ✨ Modern UI/UX Features
- **Animated Neural Network Hero**: Glowing orbs with neural connections
- **Scroll-Triggered Animations**: Cards animate as you scroll
- **Responsive Design**: Mobile-first, works on all devices
- **Dark/Light Mode**: Automatic theme switching
- **Smooth Transitions**: Bouncy, elastic animations

---

## 🚀 Quick Start

### Prerequisites
- Node.js 20.x
- Python 3.13+ (for chatbot backend)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/physical-ai-textbook.git
cd physical-ai-textbook
```

### 2. Install Frontend Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm start
```

Frontend runs at **http://localhost:3000**

---

## 🎨 Homepage Features

### Hero Section
- **Neural Network Animation**: Glowing blue/orange orbs with connections
- **Dark Navy Background**: Professional, modern look
- **Centered Content**: Title, subtitle, and CTA buttons

### Modules Section
- **4 Module Cards**: ROS2, Digital Twin, NVIDIA Isaac, VLA
- **Scroll Animation**: Cards pop in with rotation and scale effect
- **Hover Effects**: Lift and glow on hover

### Features Section
- **4 Feature Cards**: Content, Projects, Tools, Career
- **Staggered Animation**: Sequential fade-in effect
- **Icon-Based Design**: Easy visual recognition

### About Section
- **Statistics**: 4 Modules, 20+ Chapters, 100% Hands-On
- **Visual Elements**: Animated robot icon
- **Professional Layout**: Text + visual side-by-side

### CTA Section
- **Call-to-Action**: "Ready to Start Your Journey?"
- **Blue Gradient Background**: Matches hero theme
- **Get Started Button**: Direct link to first chapter

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Docusaurus Frontend             │
│  ┌─────────────────────────────────┐   │
│  │   Neural Network Animation      │   │
│  │   Scroll Animations             │   │
│  │   Responsive Components         │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
physical-ai-textbook/
├── src/
│   ├── components/
│   │   └── NeuralNetwork.tsx    # Canvas-based neural animation
│   ├── pages/
│   │   ├── index.tsx            # Homepage
│   │   └── index.module.css     # Homepage styles
│   └── theme/
│       └── Root.tsx             # Global wrapper
│
├── docs/                         # Textbook Markdown Files
├── .env                          # Environment Variables
├── .gitignore                    # Git Ignore Rules
├── docusaurus.config.ts          # Docusaurus Config
├── package.json                  # Node Dependencies
└── README.md                     # This File
```

---

## 🎨 Customization

### Change Hero Background Colors
Edit `src/pages/index.module.css`:
```css
.heroBanner {
  background: linear-gradient(135deg, #2d3a52 0%, #3a5a7a 50%, #4a6a9a 100%);
}
```

### Adjust Animation Speed
Edit `src/components/NeuralNetwork.tsx`:
```typescript
vx: (Math.random() - 0.5) * 2,  // Increase for faster movement
vy: (Math.random() - 0.5) * 2,
```

### Modify Scroll Animation Threshold
Edit `src/pages/index.tsx`:
```typescript
const isVisible = useScrollAnimation(ref, 0.1);  // Change 0.1 to adjust sensitivity
```

---

## 🛠️ Development

### Run Development Server
```bash
npm start
```

### Build for Production
```bash
npm run build
```

### Serve Production Build
```bash
npm run serve
```

### Type Check
```bash
npm run typecheck
```

---

## 🚀 Deployment

### GitHub Pages
```bash
npm run build
npm run deploy
```

### Update Config for Production
Edit `docusaurus.config.ts`:
```typescript
const config: Config = {
  baseUrl: '/physical-ai-textbook/',
  // ...
};
```

---

## 📚 Technologies Used

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Docusaurus 3** - Static site generator
- **Canvas API** - Neural network animation
- **CSS3** - Custom animations

### Animation Libraries
- **Custom Canvas** - Neural network orbs (no external deps)
- **Intersection Observer** - Scroll-triggered animations
- **CSS Transitions** - Smooth hover effects

---

## 🎬 Demo Highlights

1. **Hero Animation**: Glowing neural orbs with connections
2. **Scroll Animations**: Cards pop in as you scroll
3. **Hover Effects**: Cards lift and glow on hover
4. **Responsive Design**: Works on mobile, tablet, desktop
5. **Dark Mode**: Automatic theme switching

---

## 🔧 Troubleshooting

### Animation Not Showing
- Clear browser cache
- Check browser console for errors
- Ensure JavaScript is enabled

### Build Fails
```bash
rm -rf node_modules package-lock.json
npm install
npm start
```

### Styles Not Applying
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Clear `.docusaurus` cache folder

---

## 📖 Documentation

- **Implementation Guide**: `IMPLEMENTATION_GUIDE.md`
- **Quick Start**: `QUICKSTART.md`
- **Hackathon Summary**: `HACKATHON_SUMMARY.md`

---

## 👨‍💻 Author

**Ubaid Raza**
Physical AI & Humanoid Robotics Textbook
Panaversity Hackathon 2025

- **GitHub**: https://github.com/star-com
- **LinkedIn**: https://www.linkedin.com/in/ubaidraza/
- **Project**: https://star-com.github.io/physical-ai-textbook

---

## 📄 License

This project is built for the Panaversity Hackathon 2025.
All textbook content copyright © 2025 Ubaid Raza.

---

## 🎓 Hackathon Submission

**Built for**: Panaversity Hackathon 2025
**Category**: Interactive Learning Platform
**Tech Stack**: React + TypeScript + Docusaurus + Canvas API

### Core Features ✅
- [x] Animated neural network hero background
- [x] Scroll-triggered section animations
- [x] Responsive mobile-first design
- [x] Modern UI/UX with hover effects
- [x] Dark/light mode support
- [x] Performance optimized (60 FPS)

---

**Built with ❤️ for the future of Physical AI & Humanoid Robotics**
