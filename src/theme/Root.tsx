/**
 * Root Wrapper Component
 * Wraps the entire Docusaurus app to inject the Chat Widget globally
 * 
 * This is the recommended way to add global components in Docusaurus
 */

import React from 'react';
import { ChatWidget } from '@site/src/components/ChatWidget';
import type {WrapperProps} from '@docusaurus/types';

type RootWrapperProps = WrapperProps & {
  children: React.ReactNode;
};

export default function RootWrapper({children}: RootWrapperProps): JSX.Element {
  // Get backend URL from Docusaurus customFields or use default
  const backendUrl = 
    (typeof window !== 'undefined' && (window as any).siteConfig?.customFields?.backend_url) ||
    'https://ubaidraza1565-physical-ai-backend.hf.space';

  return (
    <>
      {/* Render the original app children */}
      {children}
      
      {/* Render chat widget globally */}
      <ChatWidget 
        backendUrl={backendUrl} 
        position="bottom-right" 
      />
    </>
  );
}
