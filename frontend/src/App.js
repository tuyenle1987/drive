import React, { useState, useEffect } from "react";
import { checkAuth, logout, fetchFiles, uploadFile, downloadFile, deleteFile } from "./services/api";
import FileList from "./components/FileList";
import UploadFile from "./components/UploadFile";
import LoginButton from "./components/LoginButton";
import "./styles/App.scss";

const App = () => {
  const [files, setFiles] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [fileLoading, setFileLoading] = useState(false);

  useEffect(() => {
    const initAuth = async () => {
      try {
        const authStatus = await checkAuth();
        setIsAuthenticated(authStatus);
        if (authStatus) {
          await handleFetchFiles();
        }
      } catch (err) {
        console.error("Error during authentication:", err);
        setError("Failed to check authentication status.");
      } finally {
        setLoading(false);
      }
    };
    initAuth();
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      setIsAuthenticated(false);
      setFiles([]);
      setError("");
    } catch (err) {
      console.error("Error during logout:", err);
      setError("Failed to log out.");
    }
  };

  const handleFetchFiles = async () => {
    try {
      setFileLoading(true);
      const fileList = await fetchFiles();
      setFiles(fileList);
    } catch (err) {
      console.error("Error fetching files:", err);
      setError("Failed to fetch files.");
    } finally {
      setFileLoading(false);
    }
  };

  const handleUpload = async (file) => {
    try {
      setFileLoading(true);
      await uploadFile(file);
      await handleFetchFiles();
    } catch (err) {
      console.error("Error uploading file:", err);
      setError("Failed to upload file.");
    } finally {
      setFileLoading(false);
    }
  };

  const handleDownload = async (id) => {
    try {
      await downloadFile(id);
    } catch (err) {
      console.error("Error downloading file:", err);
      setError("Failed to download file.");
    }
  };

  const handleDelete = async (id) => {
    try {
      setFileLoading(true);
      await deleteFile(id);
      await handleFetchFiles();
    } catch (err) {
      console.error("Error deleting file:", err);
      setError("Failed to delete file.");
    } finally {
      setFileLoading(false);
    }
  };

  const dismissError = () => setError("");

  if (loading) {
    return <div className="app-loading">Loading...</div>;
  }

  if (!isAuthenticated) {
    return (
      <div className="login-container">
        <LoginButton onLogin={() => (window.location.href = `${process.env.REACT_APP_API_BASE_URL}/auth/login`)} />
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Google Drive Integration</h1>
        <button className="btn-logout" onClick={handleLogout}>
          Logout
        </button>
      </header>
      {error && (
        <div className="error-message">
          {error} <button onClick={dismissError}>&times;</button>
        </div>
      )}
      <main>
        <UploadFile onUpload={handleUpload} />
        <button className="btn-list-files" onClick={handleFetchFiles} disabled={fileLoading}>
          {fileLoading ? "Loading..." : "List Files"}
        </button>
        {files.length > 0 ? (
          <FileList files={files} onDownload={handleDownload} onDelete={handleDelete} />
        ) : (
          <p className="no-files-message">No files available. Please upload a file.</p>
        )}
      </main>
    </div>
  );
};

export default App;
