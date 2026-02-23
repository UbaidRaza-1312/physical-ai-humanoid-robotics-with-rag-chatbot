import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import NeuralNetwork from '../components/NeuralNetwork';
import {useEffect, useRef, useState} from 'react';

import styles from './index.module.css';

// Hook for scroll-triggered animations (repeats on every scroll)
function useScrollAnimation(ref: React.RefObject<HTMLElement>, threshold = 0.1) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsVisible(entry.isIntersecting);
      },
      {threshold}
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [ref, threshold]);

  return isVisible;
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      {/* Animated Neural Network Background */}
      <div className={styles.heroParticles}>
        <NeuralNetwork />
      </div>
      
      {/* Dark overlay for better text readability */}
      <div className={styles.heroOverlay}></div>
      
      <div className="container">
        <div className={styles.heroContent}>
          <h1 className={clsx('hero__title', styles.heroTitle)}>
            Physical AI & Humanoid Robotics
          </h1>
          <p className={clsx('hero__subtitle', styles.heroSubtitle)}>
            Bridging the gap between intelligent algorithms and real-world robotic systems.
            Master ROS2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action models.
          </p>
          <div className={styles.heroButtons}>
            <Link
              className={clsx('button button--primary button--lg', styles.heroButton)}
              to="/docs/intro">
              <span className={styles.buttonIcon}>📚</span>
              Start Learning
            </Link>
            <Link
              className={clsx('button button--secondary button--lg', styles.heroButton)}
              to="/docs/module1-ros2/ros2-fundamentals">
              <span className={styles.buttonIcon}>⚙️</span>
              Explore Modules
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

type ModuleCardProps = {
  title: string;
  description: ReactNode;
  link: string;
  icon: string;
  idx: number;
};

const ModuleList: ModuleCardProps[] = [
  {
    title: 'ROS2 Fundamentals',
    description: (
      <>
        Master the Robot Operating System 2 (ROS2) with core concepts, tools, and best practices for modern robotic development. Learn nodes, topics, services, and actions.
      </>
    ),
    link: '/docs/module1-ros2/ros2-fundamentals',
    icon: '⚙️',
  },
  {
    title: 'Digital Twin Simulations',
    description: (
      <>
        Explore the power of digital twins and simulation environments for testing and validating AI and robotics systems before real-world deployment.
      </>
    ),
    link: '/docs/module2-digital-twin/simulation-basics',
    icon: '🔮',
  },
  {
    title: 'NVIDIA Isaac Integration',
    description: (
      <>
        Learn to integrate NVIDIA Isaac Sim for advanced robotics simulation, perception, and AI model training with cutting-edge GPU acceleration.
      </>
    ),
    link: '/docs/module3-nvidia-isaac/isaac-perception',
    icon: '🎮',
  },
  {
    title: 'VLA Capstone Project',
    description: (
      <>
        Apply your knowledge in a comprehensive capstone project, integrating Vision-Language-Action models into a physical humanoid robot system.
      </>
    ),
    link: '/docs/module4-vla-capstone/vla-integration',
    icon: '🚀',
  },
];

function ModuleCard({title, description, link, icon, idx}: ModuleCardProps) {
  return (
    <Link to={link} className={styles.moduleCard}>
      <div className={styles.moduleCardHeader}>
        <span className={styles.moduleIcon}>{icon}</span>
        <div className={styles.moduleCardTitleContainer}>
          <span className={styles.moduleNumber}>Module {idx + 1}</span>
          <h3 className={styles.moduleCardTitle}>{title}</h3>
        </div>
      </div>
      <div className={styles.moduleCardBody}>
        <p>{description}</p>
      </div>
      <div className={styles.moduleCardFooter}>
        <span className={styles.learnMore}>
          Learn More
          <svg className={styles.arrowIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </span>
      </div>
    </Link>
  );
}

function ModulesSection() {
  const ref = useRef<HTMLElement>(null);
  const isVisible = useScrollAnimation(ref, 0.1);

  return (
    <section ref={ref} className={`${styles.modulesSection} ${isVisible ? styles.visible : ''}`}>
      <div className="container">
        <div className={`${styles.sectionHeader} ${isVisible ? styles.animateIn : ''}`}>
          <span className={styles.sectionLabel}>Curriculum</span>
          <h2 className={styles.sectionTitle}>Explore Our Modules</h2>
          <p className={styles.sectionSubtitle}>
            Four comprehensive modules designed to take you from fundamentals to advanced humanoid robotics
          </p>
        </div>
        <div className={styles.modulesList}>
          {ModuleList.map((props, idx) => (
            <div
              key={idx}
              className={`${styles.moduleCardWrapper} ${isVisible ? styles.animateIn : ''}`}
              style={{animationDelay: `${0.1 + idx * 0.1}s`}}
            >
              <ModuleCard idx={idx} {...props} />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  const ref = useRef<HTMLElement>(null);
  const isVisible = useScrollAnimation(ref, 0.1);

  const features = [
    {
      icon: '📖',
      title: 'Comprehensive Content',
      description: 'From ROS2 basics to advanced VLA models, covering everything you need for humanoid robotics.',
    },
    {
      icon: '🛠️',
      title: 'Hands-On Projects',
      description: 'Practical exercises and real-world projects to reinforce your learning at every step.',
    },
    {
      icon: '🌐',
      title: 'Industry Tools',
      description: 'Learn with industry-standard tools like NVIDIA Isaac Sim, ROS2, and modern AI frameworks.',
    },
    {
      icon: '🎯',
      title: 'Career Ready',
      description: 'Gain skills that are in high demand for robotics engineering positions worldwide.',
    },
  ];

  return (
    <section ref={ref} className={`${styles.featuresSection} ${isVisible ? styles.visible : ''}`}>
      <div className="container">
        <div className={`${styles.sectionHeader} ${isVisible ? styles.animateIn : ''}`}>
          <span className={styles.sectionLabel}>Why This Course</span>
          <h2 className={styles.sectionTitle}>Built for Future Robotics Engineers</h2>
        </div>
        <div className={styles.featuresList}>
          {features.map((feature, idx) => (
            <div
              key={idx}
              className={`${styles.featureCardWrapper} ${isVisible ? styles.animateIn : ''}`}
              style={{animationDelay: `${0.15 + idx * 0.1}s`}}
            >
              <div className={styles.featureCard}>
                <div className={styles.featureIcon}>{feature.icon}</div>
                <h3 className={styles.featureTitle}>{feature.title}</h3>
                <p className={styles.featureDescription}>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function AboutSection() {
  return (
    <section className={styles.aboutSection}>
      <div className="container">
        <div className={styles.aboutContent}>
          <div className={styles.aboutText}>
            <span className={styles.sectionLabel}>About Physical AI</span>
            <h2 className={styles.aboutTitle}>
              The Future of Intelligence is Physical
            </h2>
            <p className={styles.aboutDescription}>
              Physical AI represents the convergence of artificial intelligence with robotics,
              enabling machines to perceive, reason, and act intelligently within dynamic
              physical environments. This textbook provides comprehensive resources for
              understanding and developing cutting-edge humanoid robot systems.
            </p>
            <div className={styles.aboutStats}>
              <div className={styles.stat}>
                <span className={styles.statNumber}>4</span>
                <span className={styles.statLabel}>Modules</span>
              </div>
              <div className={styles.stat}>
                <span className={styles.statNumber}>20+</span>
                <span className={styles.statLabel}>Chapters</span>
              </div>
              <div className={styles.stat}>
                <span className={styles.statNumber}>100%</span>
                <span className={styles.statLabel}>Hands-On</span>
              </div>
            </div>
          </div>
          <div className={styles.aboutVisual}>
            <div className={styles.visualContent}>
              <span className={styles.visualEmoji}>🤖</span>
              <div className={styles.visualBadge}>
                <span>Physical AI</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.ctaSection}>
      <div className="container">
        <div className={styles.ctaContent}>
          <h2 className={styles.ctaTitle}>Ready to Start Your Journey?</h2>
          <p className={styles.ctaSubtitle}>
            Begin learning Physical AI and Humanoid Robotics today with our comprehensive textbook.
          </p>
          <Link
            className={clsx('button button--primary button--lg', styles.ctaButton)}
            to="/docs/intro">
            Get Started Now
            <svg className={styles.arrowIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Explore the world of Physical AI and Humanoid Robotics.">
      <HomepageHeader />
      <main>
        <ModulesSection />
        <FeaturesSection />
        <AboutSection />
        <CTASection />
      </main>
    </Layout>
  );
}
