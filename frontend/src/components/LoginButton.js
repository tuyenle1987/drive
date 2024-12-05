
import React from 'react';
import './styles/LoginButton.scss';

const LoginButton = ({ onLogin }) => (
  <button className="login-button" onClick={onLogin}>
    Login
  </button>
);

export default LoginButton;
