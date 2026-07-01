import React, { useState } from "react";

const LoginPage = ({ onLogin }) => {
  const [isSignup, setIsSignup] = useState(false);

  return (
    <div className="auth-page">
      <div className="auth-container">

        {/* Logo */}
        <div className="auth-logo-section">
          <div className="auth-logo-box">
            ✎
          </div>

          <div>
            <h2>NoteAI</h2>
            <span>SMART LEARNING</span>
          </div>
        </div>

        <p className="auth-subtitle">
          {isSignup
            ? "Start learning smarter today."
            : "Welcome back! Sign in to continue."}
        </p>

        {/* Card */}
        <div className="auth-card">

          {/* Tabs */}
          <div className="auth-tabs">
            <button
              className={!isSignup ? "active" : ""}
              onClick={() => setIsSignup(false)}
            >
              Sign in
            </button>

            <button
              className={isSignup ? "active" : ""}
              onClick={() => setIsSignup(true)}
            >
              Sign up
            </button>
          </div>

          {/* Signup Form */}
          {isSignup ? (
            <>
              <div className="form-group">
                <label>FULL NAME</label>

                <input
                  type="text"
                  placeholder="Jane Smith"
                />
              </div>

              <div className="form-group">
                <label>EMAIL</label>

                <input
                  type="email"
                  placeholder="you@example.com"
                />
              </div>

              <div className="form-group">
                <label>PASSWORD</label>

                <input
                  type="password"
                  placeholder="••••••••"
                />

                <small>
                  Must be at least 8 characters.
                </small>
              </div>

              <button className="primary-btn">
                Create my account →
              </button>
            </>
          ) : (
            <>
              <div className="form-group">
                <label>EMAIL</label>

                <input
                  type="email"
                  placeholder="you@example.com"
                />
              </div>

              <div className="form-group">
                <div className="password-row">
                  <label>PASSWORD</label>

                  <span>Forgot?</span>
                </div>

                <input
                  type="password"
                  placeholder="••••••••"
                />
              </div>

              <button
                className="primary-btn"
                onClick={onLogin}
              >
                Sign in to NoteAI →
              </button>

              <div className="divider">
                <span>or</span>
              </div>

              <button className="google-btn">
                <img
                  src="https://www.svgrepo.com/show/475656/google-color.svg"
                  alt="google"
                />

                Continue with Google
              </button>
            </>
          )}
        </div>

        {/* Bottom Pills */}
        <div className="auth-tags">
          <span>✦ AI Notes</span>
          <span>✦ Smart Tutor</span>
          <span>✦ Free to start</span>
        </div>

      </div>
    </div>
  );
};

export default LoginPage;