import React, { useState } from 'react';
import './styles/UploadFile.scss';

const UploadFile = ({ onUpload }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setError('');
    setSuccess(false);
  };

  const handleUploadClick = async () => {
    if (!selectedFile) {
      setError('Please select a file to upload.');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess(false);

    try {
      await onUpload(selectedFile); // Pass the file to the onUpload prop
      setSuccess(true);
      setSelectedFile(null); // Reset file input after success
    } catch (err) {
      setError(err.message || 'An error occurred while uploading.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-file">
      <input
        type="file"
        onChange={handleFileChange}
        disabled={uploading}
        data-testid="file-input"
      />
      <button
        onClick={handleUploadClick}
        disabled={uploading}
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">File uploaded successfully!</p>}
    </div>
  );
};

export default UploadFile;
