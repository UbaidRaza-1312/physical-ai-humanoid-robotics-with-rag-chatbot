import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Bridging the gap between digital AI and physical humanoid robots',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://github.com/UbaidRaza-1312/physical-ai-humanoid-robotics-with-rag-chatbot',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  customFields: {
    back_end_url: 'https://ubaidraza1565-physical-ai-backend.hf.space/chat',
    backend_url: 'https://ubaidraza1565-physical-ai-backend.hf.space',
  },

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'star-com', // Usually your GitHub org/user name.
  projectName: 'physical-ai-textbook', // Usually your repo name.

  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/star-com/physical-ai-textbook/tree/master/',
        },
        blog: false, // Disable blog completely
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Register the Root wrapper for chat widget
    wrapper: {
      enabled: true,
    },
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: '',
      hideOnScroll: false,
      items: [
        {
          type: 'html',
          position: 'left',
          value: '<div class="navbar-brand"><span class="navbar-brand-icon">🤖</span><span class="navbar-brand-text"><strong>Physical AI Book</strong><span class="navbar-brand-subtitle">by Ubaid Raza</span></span></div>',
        },
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Tutorial',
        },
        {
          href: 'https://github.com/UbaidRaza-1312/physical-ai-humanoid-robotics-with-rag-chatbot',
          label: 'GitHub',
          position: 'right',
          className: 'header-github-link',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {
              label: 'Getting Started',
              to: '/docs/intro',
            },
            {
              label: 'ROS2 Fundamentals',
              to: '/docs/module1-ros2/ros2-fundamentals',
            },
            {
              label: 'Digital Twin',
              to: '/docs/module2-digital-twin/simulation-basics',
            },
            {
              label: 'NVIDIA Isaac',
              to: '/docs/module3-nvidia-isaac/isaac-perception',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Documentation',
              to: '/docs/intro',
            },
            {
              label: 'API Reference',
              href: '#',
            },
            {
              label: 'Examples',
              href: '#',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/UbaidRaza-1312',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/in/ubaid-raza-831666300/',
            },
            {
              label: 'Instagram',
              href: 'https://www.instagram.com/ubaidraza_1565/',
            },
            
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
