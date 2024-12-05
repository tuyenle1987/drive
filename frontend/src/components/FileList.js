import React from 'react';
import './styles/FileList.scss';

const FileList = ({ files, onDownload, onDelete }) => (
  <div className="file-list">
    {files.map((file, index) => (
      <div key={index} className="file-list-item">
        <span>{file.name}</span>
        <button onClick={() => onDownload(file.id)}>Download</button>
        <button className="delete-button" onClick={() => onDelete(file.id)}>Delete</button>
      </div>
    ))}
  </div>
);

export default FileList;
