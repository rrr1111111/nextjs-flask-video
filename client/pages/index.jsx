import { useState } from 'react';

export default function Home() {
  const [detectionMode, setDetectionMode] = useState(null); // null initially
  const [reloadKey, setReloadKey] = useState(Date.now());   // Force reload key

  const handleDetectionChange = (mode) => {
    setDetectionMode(mode);
    setReloadKey(Date.now()); // Update reloadKey to force reload
  };

  return (
    <div style={{
      backgroundColor: '#1B2241',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 20,
    }}>
      <h1 style={{ color: 'white', fontSize: '2rem', marginBottom: '20px' }}>
        {detectionMode ? 'Live Detection' : 'Select Detection Mode'}
      </h1>

      {!detectionMode && (
        <div style={{
          display: 'flex',
          gap: '20px',
          marginTop: '10px'
        }}>
          <button
            onClick={() => handleDetectionChange('barcode')}
            style={{
              backgroundColor: '#2D63B3',
              color: 'white',
              padding: '10px 30px',
              borderRadius: '20px',
              fontSize: '1rem',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            Barcode
          </button>

          <button
            onClick={() => handleDetectionChange('qrcode')}
            style={{
              backgroundColor: '#2D63B3',
              color: 'white',
              padding: '10px 30px',
              borderRadius: '20px',
              fontSize: '1rem',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            QR Code
          </button>
        </div>
      )}

      {detectionMode && (
        <>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '20px',
            padding: '10px',
            width: '80%',
            maxWidth: '800px',
            height: '350px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '30px',
            marginTop: '20px'
          }}>
            <img
              src={`http://localhost:5001/video_feed?detection_mode=${detectionMode}&key=${reloadKey}`}
              alt="Video Stream"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                borderRadius: '20px'
              }}
            />
          </div>

          <div style={{
            display: 'flex',
            gap: '20px',
            marginTop: '10px'
          }}>
            <button
              onClick={() => handleDetectionChange('barcode')}
              style={{
                backgroundColor: detectionMode === 'barcode' ? '#4A90E2' : '#2D63B3',
                color: 'white',
                padding: '10px 30px',
                borderRadius: '20px',
                fontSize: '1rem',
                border: 'none',
                cursor: 'pointer'
              }}
            >
              Barcode
            </button>

            <button
              onClick={() => handleDetectionChange('qrcode')}
              style={{
                backgroundColor: detectionMode === 'qrcode' ? '#4A90E2' : '#2D63B3',
                color: 'white',
                padding: '10px 30px',
                borderRadius: '20px',
                fontSize: '1rem',
                border: 'none',
                cursor: 'pointer'
              }}
            >
              QR Code
            </button>
          </div>
        </>
      )}
    </div>
  );
}

