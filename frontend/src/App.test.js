import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import App from "./App";
import { checkAuth, logout, fetchFiles, uploadFile, downloadFile, deleteFile } from "./services/api";

jest.mock("./services/api");

describe("App Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders login button if not authenticated", async () => {
    checkAuth.mockResolvedValue(false);
    render(<App />);

    const loginButton = await screen.findByText("Login");
    expect(loginButton).toBeInTheDocument();
  });

  test("renders file list after authentication", async () => {
    checkAuth.mockResolvedValue(true);
    fetchFiles.mockResolvedValue([{ id: "1", name: "test_file.txt" }]);

    render(<App />);

    await waitFor(() => screen.getByText("Google Drive Integration"));
    expect(screen.getByText("test_file.txt")).toBeInTheDocument();
    expect(screen.getByText("Logout")).toBeInTheDocument();
  });

  test("handles logout successfully", async () => {
    checkAuth.mockResolvedValue(true);
    fetchFiles.mockResolvedValue([]);
    logout.mockResolvedValue();

    render(<App />);

    const logoutButton = await screen.findByText("Logout");
    fireEvent.click(logoutButton);

    await waitFor(() => screen.getByText("Login"));
    expect(screen.getByText("Login")).toBeInTheDocument();
  });

  test("handles file upload", async () => {
    checkAuth.mockResolvedValue(true);
    fetchFiles.mockResolvedValue([]);
    uploadFile.mockResolvedValue();
    fetchFiles.mockResolvedValueOnce([{ id: "2", name: "uploaded_file.txt" }]);
  
    render(<App />);
  
    await waitFor(() => expect(screen.getByText("Google Drive Integration")).toBeInTheDocument());
  
    const fileInput = screen.getByTestId("file-input");
    const uploadButton = screen.getByText("Upload");
  
    const file = new File(["dummy content"], "uploaded_file.txt", { type: "text/plain" });
    fireEvent.change(fileInput, { target: { files: [file] } });
  
    fireEvent.click(uploadButton);
  
    await waitFor(() => expect(screen.getByText("uploaded_file.txt")).toBeInTheDocument());
  });

  test("displays error when fetching files fails", async () => {
    checkAuth.mockResolvedValue(true);
    fetchFiles.mockRejectedValue(new Error("Failed to fetch files"));

    render(<App />);

    await waitFor(() => screen.getByText("Failed to fetch files."));
    expect(screen.getByText("Failed to fetch files.")).toBeInTheDocument();
  });
});
