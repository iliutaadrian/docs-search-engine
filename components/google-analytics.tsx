import React from 'react';
import Script from 'next/script';

const GoogleAnalytics = () => {
  return (
    <>
      <Script
        defer
        src="http://192.168.100.69:3017/script.js"
        data-website-id="eb4d12ed-c8c9-45fe-9a1c-c1afed80d32c"
      />
    </>
  );
};

export default GoogleAnalytics;
