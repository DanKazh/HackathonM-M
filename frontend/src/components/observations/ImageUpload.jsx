import React, { useState } from 'react';
import StatusMessage from '../common/StatusMessage';
import './ImageUpload.css';

function ImageUpload({ onCoordinatesDetected }) {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(file);

    setUploading(true);
    setMessage({ text: 'Обрабатывается изображение...', type: 'info' });

    try {
      await new Promise(resolve => setTimeout(resolve, 2000));

      const mockCoordinates = {
        date: new Date().toISOString().slice(0, 16),
        ra: parseFloat((12 + Math.random() * 2).toFixed(4)),
        dec: parseFloat((-5 + Math.random() * 10).toFixed(4))
      };

      onCoordinatesDetected(mockCoordinates);
      setMessage({ text: 'Координаты определены по изображению!', type: 'success' });
    } catch (error) {
      setMessage({ text: 'Ошибка обработки изображения', type: 'error' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="image-upload-container">
      <div 
        className="upload-area"
        onClick={() => document.getElementById('file-input').click()}
      >
        <div className="upload-icon">📷</div>
        <input
          id="file-input"
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          disabled={uploading}
        />
      </div>
      
        <h3>Загрузите изображение</h3>
        <p>Перетащите файл или кликните для выбора</p>

      {message && (
        <StatusMessage
          message={message.text}
          type={message.type}
          onClose={() => setMessage(null)}
        />
      )}

      {preview && (
        <div className="image-preview">
          <img src={preview} alt="Preview" />
        </div>
      )}
    </div>
  );
}

export default ImageUpload;
