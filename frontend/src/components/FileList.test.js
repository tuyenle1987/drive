import React from 'react';
import { render, screen } from '@testing-library/react';
import FileList from './FileList';

describe('FileList Component', () => {
  test('renders an empty file list when no files are provided', () => {
    render(<FileList files={[]} />);
    const fileListItems = screen.queryAllByRole('listitem');
    expect(fileListItems).toHaveLength(0);
  });

  test('renders a list of files correctly', () => {
    const files = [
      { name: 'file1.txt' },
      { name: 'file2.pdf' },
    ];

    render(<FileList files={files} />);
    const fileListItems = screen.getAllByText(/file/i);
    expect(fileListItems).toHaveLength(2);
    expect(fileListItems[0]).toHaveTextContent('file1.txt');
    expect(fileListItems[1]).toHaveTextContent('file2.pdf');
  });

  test('renders a download button for each file', () => {
    const files = [
      { name: 'file1.txt' },
      { name: 'file2.pdf' },
    ];

    render(<FileList files={files} />);
    const downloadButtons = screen.getAllByText('Download');
    expect(downloadButtons).toHaveLength(2);
  });
});
