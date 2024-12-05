import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import {
  checkAuth,
  logout,
  fetchFiles,
  uploadFile,
  downloadFile,
  deleteFile,
} from "./api";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

describe("API Module", () => {
  let mockAxios;

  beforeAll(() => {
    mockAxios = new MockAdapter(axios);
  });

  afterEach(() => {
    mockAxios.reset();
  });

  afterAll(() => {
    mockAxios.restore();
  });

  test("checkAuth should return true when authenticated", async () => {
    mockAxios.onGet(`${API_BASE_URL}/auth/status`).reply(200, { isAuthenticated: true });

    const result = await checkAuth();

    expect(result).toBe(true);
    expect(mockAxios.history.get.length).toBe(1);
  });

  test("checkAuth should return false when not authenticated", async () => {
    mockAxios.onGet(`${API_BASE_URL}/auth/status`).reply(401);

    const result = await checkAuth();

    expect(result).toBe(false);
    expect(mockAxios.history.get.length).toBe(1);
  });

  test("logout should call the logout endpoint", async () => {
    mockAxios.onPost(`${API_BASE_URL}/auth/logout`).reply(200);

    await logout();

    expect(mockAxios.history.post.length).toBe(1);
  });

  test("fetchFiles should return a list of files", async () => {
    const files = [{ id: "1", name: "file1.txt" }, { id: "2", name: "file2.txt" }];
    mockAxios.onGet(`${API_BASE_URL}/files`).reply(200, { files });

    const result = await fetchFiles();

    expect(result).toEqual(files);
    expect(mockAxios.history.get.length).toBe(1);
  });

  test("uploadFile should upload a file", async () => {
    const file = new File(["content"], "test.txt", { type: "text/plain" });
    mockAxios.onPost(`${API_BASE_URL}/files/upload`).reply(200);

    await uploadFile(file);

    expect(mockAxios.history.post.length).toBe(1);
    const formData = mockAxios.history.post[0].data;
    expect(formData).toBeInstanceOf(FormData);
  });

  test("downloadFile should open a new window with the correct URL", () => {
    const id = "123";
    const openSpy = jest.spyOn(window, "open").mockImplementation(() => {});
    downloadFile(id);
    expect(openSpy).toHaveBeenCalledWith(`${API_BASE_URL}/files/download/${id}`);
    openSpy.mockRestore();
  });

  test("deleteFile should call the delete endpoint with the correct id", async () => {
    const id = "123";
    mockAxios.onDelete(`${API_BASE_URL}/files/delete/${id}`).reply(200);

    await deleteFile(id);

    expect(mockAxios.history.delete.length).toBe(1);
  });
});
