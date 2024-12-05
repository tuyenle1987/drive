
import axios from "axios";


const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

axios.defaults.withCredentials = true;

export const checkAuth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/auth/status`, { withCredentials: true });
    return response.data.isAuthenticated;
  } catch (err) {
    console.error("Error in checkAuth:", err);
    return false;
  }
};

export const logout = async () => {
  try {
    await axios.post(`${API_BASE_URL}/auth/logout`, {}, { withCredentials: true });
  } catch (err) {
    console.error("Error in checkAuth:", err);
    return false;
  }
};


export const fetchFiles = async () => {
  const response = await axios.get(`${API_BASE_URL}/files`);
  return response.data.files;
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  await axios.post(`${API_BASE_URL}/files/upload`, formData);
};

export const downloadFile = (id) => {
  window.open(`${API_BASE_URL}/files/download/${id}`);
};

export const deleteFile = async (id) => {
  await axios.delete(`${API_BASE_URL}/files/delete/${id}`);
};
