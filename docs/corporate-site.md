# On The Edge コーポレートサイト

> 会社コーポレートサイト。React + Vite SPA、Framer Motion、Tailwind CSS v4

*最終更新: 2026-02-28 19:21*

**パス**: `/Users/apple/Projects/on-the-edge-corporate-v2`
**ブランチ**: `master`

---
## README.md

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


---
## 技術スタック

### Dependencies

| Package | Version |
|---------|---------|
| framer-motion | ^12.34.3 |
| lucide-react | ^0.575.0 |
| react | ^19.2.0 |
| react-dom | ^19.2.0 |
| react-router-dom | ^7.13.1 |

### Dev Dependencies

| Package | Version |
|---------|---------|
| @eslint/js | ^9.39.1 |
| @tailwindcss/postcss | ^4.2.0 |
| @tailwindcss/vite | ^4.2.0 |
| @types/react | ^19.2.7 |
| @types/react-dom | ^19.2.3 |
| @vitejs/plugin-react | ^5.1.1 |
| autoprefixer | ^10.4.24 |
| eslint | ^9.39.1 |
| eslint-plugin-react-hooks | ^7.0.1 |
| eslint-plugin-react-refresh | ^0.4.24 |
| globals | ^16.5.0 |
| postcss | ^8.5.6 |
| tailwindcss | ^4.2.0 |
| vite | ^7.3.1 |

### Scripts

```json
{
  "dev": "vite",
  "build": "vite build",
  "lint": "eslint .",
  "preview": "vite preview"
}
```

---
## ディレクトリ構成

```
├── public/
│   ├── _redirects
│   ├── logo.png
│   └── vite.svg
├── src/
│   ├── assets/
│   │   ├── crm-hero.png
│   │   ├── logo.png
│   │   ├── react.svg
│   │   ├── sns-hero.png
│   │   └── webdesign-hero.png
│   ├── components/
│   │   ├── BackgroundVideo.jsx
│   │   ├── CompanySection.jsx
│   │   ├── ContactCTA.jsx
│   │   ├── ContactForm.jsx
│   │   ├── Footer.jsx
│   │   ├── HeroSection.jsx
│   │   ├── Layout.jsx
│   │   ├── Navbar.jsx
│   │   ├── PageHero.jsx
│   │   └── ServiceCard.jsx
│   ├── pages/
│   │   ├── Contact.jsx
│   │   ├── CrmDevelopment.jsx
│   │   ├── Home.jsx
│   │   ├── Philosophy.jsx
│   │   ├── ServicePage.jsx
│   │   ├── SnsMarketing.jsx
│   │   └── WebDesign.jsx
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── .gitignore
├── README.md
├── eslint.config.js
├── index.html
├── package.json
├── render.yaml
└── vite.config.js
```

---
## デプロイ設定 (render.yaml)

```yaml
services:
  - type: web
    name: on-the-edge-corporate-v2
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html

```

---
## 最近の変更 (git log)

```
2f48e7d CRM highlights: PC-only line break 業界特化で汎用CRMが / 解決できない課題に対応
feb9ba8 CRM highlights: fix overlap - nowrap only when explicit, increase gap
aa550d0 Hero EN: 4 lines for mobile (eliminate→L3, extract→L4)
b37cc4b Hero: add line break after 複雑なノイズを削ぎ落とし / eliminate complex noise
b66326a SNS 1-line fix + Hero font + JA/EN typewriter
fa40d4c SNS intro: 最適投稿時間の分析→最適投稿時間分析 for 1-line on mobile
320fab8 SNS intro: shorten for 1-line fit (remove commas)
80eb3aa SNS + ServicePage: 1-line fixes + intro font size revert
8262fa0 SNS Marketing: 1-line fit for PC + mobile
f578126 SNS Marketing: intro/highlights line breaks + shorten for 1-line fit
```
