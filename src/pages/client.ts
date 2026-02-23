/**
 * Docusaurus Client Module
 * Injects the RAG Chat Widget globally across all pages
 * 
 * This file runs on the client-side and loads the chat widget
 * when the Docusaurus app initializes.
 */

import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

// Only run on client-side (not during SSR build)
if (ExecutionEnvironment.canUseDOM) {
  // Dynamic import to avoid SSR issues
  import('../components/ChatWidget/ChatWidget').then(({ ChatWidget }) => {
    // Create container for chat widget
    const containerId = 'panaversity-chat-widget-root';
    
    // Check if container already exists
    if (document.getElementById(containerId)) {
      return;
    }
    
    const container = document.createElement('div');
    container.id = containerId;
    document.body.appendChild(container);
    
    // Import React and ReactDOM dynamically
    Promise.all([
      import('react'),
      import('react-dom/client'),
    ]).then(([React, ReactDOM]) => {
      // Create React root
      const root = ReactDOM.createRoot(container);
      
      // Get backend URL from Docusaurus config or use default
      const backendUrl = (window as any).gtag?.config?.backend_url 
        || process.env.DOCUSAURUS_BACKEND_URL 
        || 'http://localhost:8000';
      
      // Render chat widget
      root.render(
        React.createElement(ChatWidget, {
          backendUrl: backendUrl,
          position: 'bottom-right',
        })
      );
    }).catch((error) => {
      console.error('Failed to load chat widget:', error);
    });
  });
}

// Export empty object (required for Docusaurus client modules)
export default {};
