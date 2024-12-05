import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import LoginButton from './LoginButton';

describe('LoginButton Component', () => {
  test('renders the login button correctly', () => {
    const { getByText } = render(<LoginButton onLogin={() => {}} />);
    const loginButton = getByText('Login');
    expect(loginButton).toBeInTheDocument();
  });

  test('calls the onLogin function when clicked', () => {
    const onLoginMock = jest.fn();

    const { getByText } = render(<LoginButton onLogin={onLoginMock} />);
    const loginButton = getByText('Login');

    fireEvent.click(loginButton);

    expect(onLoginMock).toHaveBeenCalledTimes(1);
  });
});
