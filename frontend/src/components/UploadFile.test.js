import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import UploadFile from './UploadFile';

describe('UploadFile Component', () => {
  let onUploadMock;

  beforeEach(() => {
    onUploadMock = jest.fn();
  });

  test('renders the component correctly', () => {
    render(<UploadFile onUpload={onUploadMock} />);

    expect(screen.getByTestId('file-input')).toBeInTheDocument();
    expect(screen.getByText('Upload')).toBeInTheDocument();
  });

  test('displays error when no file is selected and upload button is clicked', () => {
    render(<UploadFile onUpload={onUploadMock} />);

    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    expect(screen.getByText('Please select a file to upload.')).toBeInTheDocument();
  });

  test('allows a file to be selected and resets after successful upload', async () => {
    onUploadMock.mockResolvedValueOnce();

    render(<UploadFile onUpload={onUploadMock} />);

    const file = new File(['dummy content'], 'test_file.txt', { type: 'text/plain' });

    const fileInput = screen.getByTestId('file-input');
    fireEvent.change(fileInput, { target: { files: [file] } });

    expect(fileInput.files[0]).toBe(file);

    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => expect(onUploadMock).toHaveBeenCalledWith(file));

    expect(screen.getByText('File uploaded successfully!')).toBeInTheDocument();

    expect(fileInput.value).toBe('');
  });

  test('displays error message when upload fails', async () => {
    onUploadMock.mockRejectedValueOnce(new Error('Upload failed.'));

    render(<UploadFile onUpload={onUploadMock} />);

    const file = new File(['dummy content'], 'test_file.txt', { type: 'text/plain' });

    const fileInput = screen.getByTestId('file-input');
    fireEvent.change(fileInput, { target: { files: [file] } });

    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => expect(screen.getByText('Upload failed.')).toBeInTheDocument());
  });

  test('disables input and button during upload', async () => {
    onUploadMock.mockResolvedValueOnce();

    render(<UploadFile onUpload={onUploadMock} />);

    const file = new File(['dummy content'], 'test_file.txt', { type: 'text/plain' });

    const fileInput = screen.getByTestId('file-input');
    fireEvent.change(fileInput, { target: { files: [file] } });

    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    expect(fileInput).toBeDisabled();
    expect(uploadButton).toBeDisabled();

    await waitFor(() => expect(uploadButton).not.toBeDisabled());
  });
});
